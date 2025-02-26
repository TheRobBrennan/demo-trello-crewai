import os

import requests
from dotenv import load_dotenv

# Adjust the path to your .env file
env_path = os.path.join(os.path.dirname(__file__), "../../../.env")
load_dotenv(dotenv_path=env_path)


class TrelloUtils:

    def __init__(self):
        self.api_key = os.getenv("TRELLO_API_KEY")
        self.token = os.getenv("TRELLO_API_TOKEN")

        # Debug logging for credentials
        print("Initializing TrelloUtils...")
        print(f"API Key loaded (first 4 chars): {self.api_key[:4] if self.api_key else 'None'}")
        print(f"Token loaded (first 4 chars): {self.token[:4] if self.token else 'None'}")

        if not self.api_key or not self.token:
            raise ValueError("TRELLO_API_KEY and TRELLO_API_TOKEN must be set.")
            
        # Verify API access
        self.verify_api_access()

    def verify_api_access(self):
        """
        Verifies that the API credentials have proper access.
        """
        url = "https://api.trello.com/1/members/me"
        query = {"key": self.api_key, "token": self.token}
        
        print("Verifying Trello API access...")
        try:
            response = requests.get(url, params=query)
            print(f"API access check status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Authenticated as user: {data.get('username', 'unknown')}")
                print(f"Full name: {data.get('fullName', 'unknown')}")
                
                # Get boards the user has access to
                boards_url = f"https://api.trello.com/1/members/me/boards"
                boards_response = requests.get(boards_url, params=query)
                if boards_response.status_code == 200:
                    boards = boards_response.json()
                    print(f"Number of accessible boards: {len(boards)}")
                    for board in boards:
                        print(f"Board: {board.get('name')} (ID: {board.get('id')})")
            else:
                print(f"API access verification failed: {response.status_code} - {response.text}")
                raise ValueError("Failed to verify Trello API access")
        except requests.RequestException as e:
            print(f"API access verification error: {e}")
            raise ValueError(f"Failed to connect to Trello API: {e}")

    def get_full_board_id(self, short_board_id):
        """
        Fetches the full board ID for the given short board ID from Trello API.

        Args:
            short_board_id (str): The short ID of the Trello board.

        Returns:
            str: The full board ID or an error message if the request fails.
        """
        url = f"https://api.trello.com/1/boards/{short_board_id}"
        query = {"key": self.api_key, "token": self.token}

        try:
            response = requests.get(url, params=query)
            if response.status_code == 200:
                board_data = response.json()
                return board_data.get(
                    "id", "Error: Full board ID not found in response."
                )
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.RequestException as e:
            return f"Error: Unable to connect to Trello API. {e}"

    def get_board_lists(self, board_id):
        """
        Fetches all lists for the given board ID from Trello API.

        Args:
            board_id (str): The ID of the Trello board.

        Returns:
            list: A list of dictionaries containing list details or an error message if the request fails.
        """
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        query = {"key": self.api_key, "token": self.token}

        try:
            response = requests.get(url, params=query)
            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.RequestException as e:
            return f"Error: Unable to connect to Trello API. {e}"

    def verify_list(self, list_id):
        """
        Verifies that a list exists and returns its details.
        
        Args:
            list_id (str): The ID of the Trello list.
            
        Returns:
            dict: The list details if found, or an error message if not found.
        """
        url = f"https://api.trello.com/1/lists/{list_id}"
        query = {"key": self.api_key, "token": self.token}
        
        print(f"Verifying list ID: {list_id}")
        
        try:
            response = requests.get(url, params=query)
            print(f"List verification response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"List details: {data}")
                return data
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                print(f"List verification error: {error_msg}")
                return error_msg
        except requests.RequestException as e:
            error_msg = f"Error: Unable to verify list. {e}"
            print(f"List verification exception: {error_msg}")
            return error_msg

    def verify_board_access(self, board_id):
        """
        Verifies access to a specific board and returns its details.
        
        Args:
            board_id (str): The ID of the Trello board.
            
        Returns:
            dict: The board details if accessible, or raises an error if not.
        """
        url = f"https://api.trello.com/1/boards/{board_id}"
        query = {
            "key": self.api_key,
            "token": self.token,
            "fields": "name,url,idOrganization",
            "lists": "open"
        }
        
        print(f"\nVerifying access to board: {board_id}")
        try:
            response = requests.get(url, params=query)
            print(f"Board access check status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Board name: {data.get('name')}")
                print(f"Board URL: {data.get('url')}")
                if 'lists' in data:
                    print("Lists in board:")
                    for lst in data['lists']:
                        print(f"  - {lst.get('name')} (ID: {lst.get('id')})")
                return data
            else:
                error_msg = f"Error accessing board: {response.status_code} - {response.text}"
                print(error_msg)
                raise ValueError(error_msg)
        except requests.RequestException as e:
            error_msg = f"Error connecting to board: {e}"
            print(error_msg)
            raise ValueError(error_msg)

    def get_cards_in_list(self, list_id):
        """
        Fetches all cards from the specified list ID in Trello.

        Args:
            list_id (str): The ID of the Trello list.

        Returns:
            list: A list of dictionaries containing card details or an error message if the request fails.
        """
        if not list_id:
            return "Error: List ID must be provided."

        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        query = {"key": self.api_key, "token": self.token}
        
        print(f"Making request to Trello API: {url}")
        print(f"Using list_id: {list_id}")

        try:
            response = requests.get(url, params=query)
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Raw response data: {data}")
                cards = [{"id": card["id"], "name": card["name"]} for card in data]
                print(f"Processed cards: {cards}")
                return cards
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                print(f"API error: {error_msg}")
                return error_msg
        except requests.RequestException as e:
            error_msg = f"Error: Unable to connect to Trello API. {e}"
            print(f"Request exception: {error_msg}")
            return error_msg


if __name__ == "__main__":
    # Replace with your Trello short board ID

    # trello_utils = TrelloUtils()
    # short_board_id = "rCXL4ZCJ"
    # result = trello_utils.get_full_board_id(short_board_id)
    # print("Result:", result)

    # trello_utils = TrelloUtils()
    # board_id = os.getenv("TRELLO_BOARD_ID")
    # lists = trello_utils.get_board_lists(board_id)
    # print("Lists:", lists)

    trello_utils = TrelloUtils()
    list_id = os.getenv("TRELLO_TOOD_LIST_ID")
    cards = trello_utils.get_cards_in_list(list_id)
    print("Cards:", cards)

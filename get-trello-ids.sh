#!/bin/bash
set -e

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found. Please run 'npm run setup' first."
  exit 1
fi

# Load environment variables from .env
source .env

# Check if Trello API key and token are set
if [ -z "$TRELLO_API_KEY" ] || [ -z "$TRELLO_API_TOKEN" ]; then
  echo "Error: TRELLO_API_KEY and TRELLO_API_TOKEN must be set in your .env file."
  echo "Please edit your .env file and add these values."
  exit 1
fi

# Check if short board ID is provided
if [ -z "$TRELLO_SHORT_BOARD_ID" ]; then
  echo "Error: TRELLO_SHORT_BOARD_ID is not set in your .env file."
  echo "Please edit your .env file and add this value."
  echo "You can find it in your Trello board URL: https://trello.com/b/XXXXXXXX/board-name"
  exit 1
fi

echo "Fetching full board ID for short ID: $TRELLO_SHORT_BOARD_ID"
BOARD_RESPONSE=$(curl -s "https://api.trello.com/1/boards/$TRELLO_SHORT_BOARD_ID?key=$TRELLO_API_KEY&token=$TRELLO_API_TOKEN")

# Check if the response contains an error
if [[ $BOARD_RESPONSE == *"\"error\""* ]]; then
  echo "Error fetching board information:"
  echo "$BOARD_RESPONSE"
  exit 1
fi

# Extract the full board ID
FULL_BOARD_ID=$(echo "$BOARD_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$FULL_BOARD_ID" ]; then
  echo "Error: Could not extract full board ID from response."
  exit 1
fi

echo "Full board ID: $FULL_BOARD_ID"
echo "You should set this as TRELLO_BOARD_ID in your .env file."
echo ""

echo "Fetching lists for board ID: $FULL_BOARD_ID"
LISTS_RESPONSE=$(curl -s "https://api.trello.com/1/boards/$FULL_BOARD_ID/lists?key=$TRELLO_API_KEY&token=$TRELLO_API_TOKEN")

# Check if the response contains an error
if [[ $LISTS_RESPONSE == *"\"error\""* ]]; then
  echo "Error fetching lists:"
  echo "$LISTS_RESPONSE"
  exit 1
fi

echo "Lists on your board:"

# Use a more reliable method to parse the JSON response
# This extracts each list object and processes them one by one
echo "$LISTS_RESPONSE" | sed 's/\[{/\n{/g' | sed 's/},{/\n{/g' | sed 's/}]/\n}/g' | while read -r list_obj; do
  if [[ -n "$list_obj" && "$list_obj" != "]" ]]; then
    NAME=$(echo "$list_obj" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    ID=$(echo "$list_obj" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    if [[ -n "$NAME" && -n "$ID" ]]; then
      echo "- $NAME: $ID"
    fi
  fi
done

echo ""
echo "Copy the appropriate list IDs to your .env file:"
echo "TRELLO_TOOD_LIST_ID=... (ID of your 'To Do' list)"
echo "TRELLO_DOING_LIST_ID=... (ID of your 'Doing' list)" 
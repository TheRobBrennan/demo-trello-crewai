import os
import unittest
from unittest.mock import patch, MagicMock

from pro_tools.crew import ProTools


class TestNoCardsHandling(unittest.TestCase):
    """Test the handling of scenarios where no cards are found in the TODO list."""

    @patch('pro_tools.utils.trello_utils.TrelloUtils')
    def test_no_cards_raises_value_error(self, mock_trello_utils):
        """Test that a ValueError is raised when no cards are found."""
        # Setup mock
        mock_instance = MagicMock()
        mock_trello_utils.return_value = mock_instance
        
        # Mock verify_board_access to return a valid board
        mock_instance.verify_board_access.return_value = {
            'lists': [{'id': 'mock_list_id', 'name': 'TODO'}]
        }
        
        # Mock verify_list to return a valid list
        mock_instance.verify_list.return_value = {'id': 'mock_list_id', 'name': 'TODO'}
        
        # Mock get_cards_in_list to return an empty list (no cards)
        mock_instance.get_cards_in_list.return_value = []
        
        # Set environment variables
        os.environ['TRELLO_BOARD_ID'] = 'mock_board_id'
        os.environ['TRELLO_TOOD_LIST_ID'] = 'mock_list_id'
        
        # Create ProTools instance
        pro_tools = ProTools()
        
        # Test that prepare_inputs raises ValueError when no cards are found
        with self.assertRaises(ValueError) as context:
            pro_tools.prepare_inputs({})
        
        # Verify the error message
        self.assertIn("No cards found in the TODO list", str(context.exception))


if __name__ == '__main__':
    unittest.main() 
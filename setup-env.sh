#!/bin/bash
set -e

# Check if .env file already exists
if [ -f .env ]; then
  echo "An .env file already exists."
  read -p "Do you want to overwrite it? (y/n): " overwrite
  if [[ $overwrite != "y" && $overwrite != "Y" ]]; then
    echo "Operation cancelled. Your .env file remains unchanged."
    exit 0
  fi
fi

# Check if .env.example exists
if [ ! -f .env.example ]; then
  echo "Error: .env.example file not found."
  exit 1
fi

# Copy .env.example to .env
cp .env.example .env
echo ".env file created successfully from .env.example."
echo ""
echo "Please edit the .env file to add your API keys and configuration:"
echo "  - OPENAI_API_KEY"
echo "  - TRELLO_API_KEY"
echo "  - TRELLO_API_TOKEN"
echo "  - TRELLO_SHORT_BOARD_ID"
echo "  - TRELLO_BOARD_ID"
echo "  - TRELLO_TOOD_LIST_ID"
echo "  - TRELLO_DOING_LIST_ID"
echo "  - TAVILY_API_KEY"
echo ""
echo "After editing the .env file, you can run the application with:"
echo "  npm start" 
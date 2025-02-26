#!/bin/bash
set -e

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found. Please run 'npm run setup' first."
  exit 1
fi

echo "Checking .env file for missing values..."

# Define required environment variables
REQUIRED_VARS=(
  "OPENAI_API_KEY"
  "TRELLO_API_KEY"
  "TRELLO_API_TOKEN"
  "TRELLO_SHORT_BOARD_ID"
  "TRELLO_BOARD_ID"
  "TRELLO_TOOD_LIST_ID"
  "TRELLO_DOING_LIST_ID"
  "TAVILY_API_KEY"
)

# Load the .env file
source .env

# Check if any required variables are empty
EMPTY_VARS=()
for VAR in "${REQUIRED_VARS[@]}"; do
  VALUE="${!VAR}"
  if [[ -z "$VALUE" ]]; then
    EMPTY_VARS+=("$VAR")
  fi
done

# If any required variables are empty, print a warning
if [ ${#EMPTY_VARS[@]} -gt 0 ]; then
  echo "Warning: The following environment variables are empty:"
  for VAR in "${EMPTY_VARS[@]}"; do
    echo "  - $VAR"
  done
  echo ""
  echo "Please edit the .env file to add your API keys and configuration."
  exit 1
else
  echo "All environment variables appear to be properly set."
fi 
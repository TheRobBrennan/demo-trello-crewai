#!/bin/bash
set -e

echo "Starting docker-entrypoint.sh script..."

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

echo "Checking required environment variables..."

# Check if all required environment variables are set
MISSING_VARS=()
for VAR in "${REQUIRED_VARS[@]}"; do
  echo "Checking $VAR..."
  if [ -z "${!VAR}" ]; then
    echo "  - $VAR is missing or empty"
    MISSING_VARS+=("$VAR")
  else
    echo "  - $VAR is set"
  fi
done

# If any required variables are missing, print an error message and exit
if [ ${#MISSING_VARS[@]} -gt 0 ]; then
  echo "Error: The following required environment variables are not set:"
  for VAR in "${MISSING_VARS[@]}"; do
    echo "  - $VAR"
  done
  echo ""
  echo "Please set these variables in your .env file or pass them when running the container."
  echo "Example:"
  echo "  docker run --env-file .env pro-tools"
  echo "  or"
  echo "  docker run -e OPENAI_API_KEY=your_key -e TRELLO_API_KEY=your_key ... pro-tools"
  exit 1
fi

echo "All required environment variables are set."
echo "Running command: python -m pro_tools.main $@"

# If all required variables are set, run the command
exec python -m pro_tools.main "$@" 
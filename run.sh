#!/bin/bash
set -e

# Create output directory if it doesn't exist
mkdir -p output

# Check if .env file exists
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    echo "Error: .env file not found. Please create one based on .env.example"
    echo "You can run: npm run setup"
    exit 1
  else
    echo "Error: Neither .env nor .env.example files found."
    exit 1
  fi
fi

# Check if environment variables are properly set
if [ -f check-env.sh ]; then
  chmod +x check-env.sh
  if ! ./check-env.sh > /dev/null 2>&1; then
    echo "Warning: Some required environment variables are not set."
    echo "You can check which ones by running: npm run check"
    read -p "Do you want to continue anyway? (y/n): " continue_anyway
    if [[ $continue_anyway != "y" && $continue_anyway != "Y" ]]; then
      echo "Operation cancelled."
      exit 1
    fi
    echo "Continuing with empty environment variables..."
  fi
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Error: Docker is not installed. Please install Docker Desktop."
  echo "Visit https://www.docker.com/products/docker-desktop/ to download and install."
  exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker Desktop."
  exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
  echo "Error: docker-compose is not installed."
  echo "It should be included with Docker Desktop. Please check your installation."
  exit 1
fi

# Build and run the Docker container
echo "Building and starting the Pro Tools container..."
docker-compose up --build "$@" 
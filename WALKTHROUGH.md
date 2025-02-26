# ProTools Crew Walkthrough Guide

This guide will walk you through the complete setup and usage of the ProTools Crew application, which automates research and content creation for AI-related topics using Trello for task management.

## Prerequisites

Before you begin, you'll need:

- Docker Desktop installed on your machine
- A Trello account
- A Tavily API key
- An OpenAI API key

## Step 1: Setting Up Your Trello Board

The application uses Trello to manage the workflow of researching and writing about AI topics. Let's set up a Trello board with the appropriate structure:

1. **Create a New Trello Board**:
   - Log in to your Trello account at [trello.com](https://trello.com)
   - Click the "+" button in the header and select "Create Board"
   - Name your board (e.g., "AI Research Topics")
   - Choose a background color and click "Create"

2. **Set Up Required Lists**:
   - Your board should have at least two lists:
     - "To Do" - Where you'll add cards for topics to research
     - "Doing" - Where cards will be moved after processing
   - You can also add additional lists like "Done" if desired

3. **Add Sample Cards**:
   - In the "To Do" list, create a few cards with AI topics you'd like to research
   - For example: "GPT-4 Latest Features", "AI in Healthcare", "Stable Diffusion Updates"

## Step 2: Getting Your Trello API Credentials

To allow the application to interact with your Trello board, you'll need to obtain API credentials through Trello's Power-Up system:

1. **Create a Trello Power-Up**:
   - Visit [https://trello.com/power-ups/admin/](https://trello.com/power-ups/admin/)
   - Click "New" or "Create New Power-Up"
   - Fill in the required fields:
     - Name: "ProTools Integration" (or any name you prefer)
     - Contact Email: Your email address
     - Author: Your name
     - Overview: "Integration for ProTools Crew application"
     - For other fields, you can use placeholder information
   - Save the Power-Up

2. **Get Your API Key**:
   - After creating the Power-Up, you'll be taken to its settings page
   - Look for the "API Key" field - this is your Trello API Key
   - Copy this key for later use in your `.env` file

3. **Generate a Token**:
   - Using your API Key, visit the following URL (replace YOUR_API_KEY with your actual API key):
     `https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&name=ProTools%20Integration&key=YOUR_API_KEY`
   - You'll be asked to authorize the token generation
   - Grant permission to your account
   - Copy the generated token for later use in your `.env` file

4. **Get Your Board and List IDs**:
   - Open your Trello board in the browser
   - The URL will look like: `https://trello.com/b/XXXXXXXX/board-name`
   - The part after `/b/` and before `/board-name` is your short board ID (e.g., `XXXXXXXX`)
   - Add this short board ID to your `.env` file as `TRELLO_SHORT_BOARD_ID`
   - Then use our helper script to get the full board ID and list IDs:

     ```bash
     npm run trello
     ```

   - This script will:
     - Fetch the full board ID based on your short board ID
     - List all the lists on your board with their IDs
     - Provide instructions for adding these IDs to your `.env` file

## Step 3: Getting Your Tavily API Key

The application uses Tavily for research capabilities:

1. **Sign Up for Tavily**:
   - Visit [https://tavily.com/](https://tavily.com/)
   - Sign up for an account
   - Navigate to the API section or dashboard

2. **Generate an API Key**:
   - Follow Tavily's instructions to generate an API key
   - Copy this key for later use

## Step 4: Getting Your OpenAI API Key

The AI agents in the application are powered by OpenAI:

1. **Sign Up for OpenAI**:
   - Visit [https://platform.openai.com/](https://platform.openai.com/)
   - Sign up for an account or log in

2. **Generate an API Key**:
   - Navigate to the API keys section
   - Create a new secret key
   - Copy this key for later use

## Step 5: Setting Up the Application

Now that you have all the necessary credentials, let's set up the application:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/demo-trello-crewai.git
   cd demo-trello-crewai
   ```

2. **Set Up Environment Variables**:

   ```bash
   npm run setup
   ```

   This will create a `.env` file from the template.

3. **Edit the `.env` File**:
   Open the `.env` file in your favorite text editor and add your API keys and Trello information:

   ```shell
   MODEL=gpt-4o
   
   # Add your OpenAI API key below
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Add your Trello credentials below
   TRELLO_API_KEY=your_trello_api_key_here
   TRELLO_API_TOKEN=your_trello_token_here
   TRELLO_SHORT_BOARD_ID=your_short_board_id_here
   TRELLO_BOARD_ID=your_full_board_id_here
   
   # Add your Trello list IDs below
   TRELLO_TOOD_LIST_ID=your_todo_list_id_here
   TRELLO_DOING_LIST_ID=your_doing_list_id_here
   
   # Add your Tavily API key below
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

4. **Get Trello Board and List IDs**:
   After adding your Trello API key, token, and short board ID to the `.env` file, run:

   ```bash
   npm run trello
   ```

   This will help you get the full board ID and list IDs to complete your `.env` file.

5. **Verify Your Configuration**:

   ```bash
   npm run check
   ```

   This will check if all required environment variables are set.

## Step 6: Running the Application

With everything set up, you can now run the application:

1. **Start the Application**:

   ```bash
   npm start
   ```

   This will:
   - Build the Docker container
   - Start the application
   - Process all cards in your "To Do" list
   - Generate research and articles
   - Add the articles as comments to the cards
   - Move the cards to the "Doing" list

2. **Check the Results**:
   - Go to your Trello board
   - You should see that cards have been moved from "To Do" to "Doing"
   - Each card should have a comment with a detailed article about the topic

## Troubleshooting

If you encounter issues:

1. **Check Environment Variables**:
   - Ensure all API keys and IDs in your `.env` file are correct
   - Run `npm run check` to verify

2. **Docker Issues**:
   - Ensure Docker Desktop is running
   - Try rebuilding the container with `npm run start:build`

3. **API Limits**:
   - Check if you've hit rate limits on OpenAI or Tavily
   - Consider upgrading your API plans if needed

4. **Trello Permissions**:
   - Ensure your Trello token has write permissions
   - Try regenerating your token

## Next Steps

- Add more cards to your "To Do" list for new research topics
- Customize the agents and tasks in the configuration files
- Explore the crewAI documentation for advanced features

Happy researching!

# ProTools Crew

Welcome to the ProTools Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## 🗣️ Shout out

This example was originally developed by [Brandon Hancock](https://github.com/bhancockio) as part of our AI Developer Accelerator group in the [noob-vs-pro-tools](https://github.com/bhancockio/noob-vs-pro-tools) repo on GitHub.

## 📋 Getting Started

For a comprehensive step-by-step guide on setting up and using this application, please see the [WALKTHROUGH.md](WALKTHROUGH.md) file. This guide includes:

- Setting up your Trello board with the required structure
- Obtaining all necessary API keys and credentials
- Configuring the environment variables
- Running the application and verifying the results

## Installation

### Option 1: Local Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:

```bash
crewai install
```

### Option 2: Docker Installation (Recommended)

This project can be run entirely in Docker without installing any dependencies locally. You only need:

- Docker Desktop (for macOS)
- A `.env` file with your API keys

To get started:

1. Set up your environment file:

   ```bash
   npm run setup
   ```

   This will create a `.env` file from the `.env.example` template.

2. Edit the `.env` file to add your API keys and configuration.

3. Verify your environment configuration:

   ```bash
   npm run check
   ```

   This will check if all required environment variables are set.

4. Run the application:

   ```bash
   npm start
   ```

The Docker setup will automatically check for required environment variables and provide helpful error messages if any are missing.

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/pro_tools/config/agents.yaml` to define your agents
- Modify `src/pro_tools/config/tasks.yaml` to define your tasks
- Modify `src/pro_tools/crew.py` to add your own logic, tools and specific args
- Modify `src/pro_tools/main.py` to add custom inputs for your agents and tasks

## Running the Project

### Using Docker (Recommended)

```bash
# Set up your environment file
npm run setup

# Check if your environment is properly configured
npm run check

# Start the application
npm start

# Start in detached mode (run in background)
npm run start:detached

# Force rebuild the Docker image
npm run start:build

# Run training with Docker
npm run start:train

# Replay a specific task with Docker
npm run start:replay
```

### Using Local Python

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the pro-tools Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Important Resources To Connect Your Crew to Trello

- <https://www.merge.dev/blog/trello-api-key>
- <https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-lists-get>
- <https://docs.tavily.com/docs/python-sdk/tavily-search/getting-started>

## Testing GitHub Actions Locally

We recommend using [act](https://github.com/nektos/act) to test GitHub Actions workflows locally before pushing changes if you are developing on a Mac.

Prerequisites for macOS:

- Homebrew
- Docker Desktop (must be running)

```sh
# Install act using Homebrew
brew install act

# Verify installation
act --version # Should show 0.2.74 or higher
```

### Running Tests

The following test scripts are available:

```bash
# Run all workflow tests
npm run test:workflows

# Test semantic PR checks
npm run test:workflows:semantic
npm run test:workflows:semantic:major
npm run test:workflows:semantic:minor
npm run test:workflows:semantic:patch
npm run test:workflows:semantic:invalid

# Test version bump workflow
npm run test:workflows:version

# Test merge workflow
npm run test:workflows:merge
```

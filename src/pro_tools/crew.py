import os
from typing import Any, Dict

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, before_kickoff, crew, task

from pro_tools.models.article import Article
from pro_tools.models.research import Research
from pro_tools.tools.RedditSearchTool import RedditSerpApiSearchTool
from pro_tools.tools.TrelloAddCardCommentTool import TrelloAddCardCommentTool
from pro_tools.tools.TrelloUpdateCardTool import TrelloUpdateCardTool
from pro_tools.utils.trello_utils import TrelloUtils


@CrewBase
class ProTools:
    """ProTools crew"""

    def __init__(self):
        # Get the directory containing this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set config paths relative to this file
        self.agents_config = os.path.join(base_dir, "config", "agents.yaml")
        self.tasks_config = os.path.join(base_dir, "config", "tasks.yaml")
        
        # Verify config files exist
        if not os.path.exists(self.agents_config):
            raise ValueError(f"Agents config file not found: {self.agents_config}")
        if not os.path.exists(self.tasks_config):
            raise ValueError(f"Tasks config file not found: {self.tasks_config}")
            
        print(f"\nUsing config files:")
        print(f"Agents config: {self.agents_config}")
        print(f"Tasks config: {self.tasks_config}")

    @before_kickoff
    def prepare_inputs(self, inputs: Dict[str, Any]):
        inputs = inputs or {}
        trello_utils = TrelloUtils()

        print("\nStarting to prepare inputs...")
        
        # Get board ID
        board_id = os.getenv("TRELLO_BOARD_ID")
        if board_id is None:
            raise ValueError("Environment variable 'TRELLO_BOARD_ID' is not set.")
            
        # Verify board access and get lists
        print("\nVerifying board access...")
        board_details = trello_utils.verify_board_access(board_id)
        
        # Get TODO list ID
        trello_todo_list_id = os.getenv("TRELLO_TOOD_LIST_ID")
        if trello_todo_list_id is None:
            raise ValueError("Environment variable 'TRELLO_TOOD_LIST_ID' is not set.")
            
        # Verify list exists in board
        if 'lists' in board_details:
            list_ids = [lst.get('id') for lst in board_details['lists']]
            if trello_todo_list_id not in list_ids:
                raise ValueError(f"List ID {trello_todo_list_id} not found in board {board_id}")
            
        print(f"\nVerifying list exists...")
        list_details = trello_utils.verify_list(trello_todo_list_id)
        if isinstance(list_details, str) and list_details.startswith("Error"):
            raise ValueError(f"Invalid list ID: {list_details}")
            
        print(f"\nFetching cards from list ID: {trello_todo_list_id}")
        cards = trello_utils.get_cards_in_list(trello_todo_list_id)
        print(f"Retrieved cards: {cards}")
        
        if isinstance(cards, str) and cards.startswith("Error"):
            raise ValueError(f"Failed to fetch cards: {cards}")
            
        if not cards:
            print("No cards found in the TODO list.")
            # Instead of continuing with empty inputs, raise an exception to stop the process
            raise ValueError("No cards found in the TODO list. Nothing to process.")
            
        inputs["trello_cards"] = cards
        print(f"\nFinal inputs prepared: {inputs}")
        return inputs

    # Define agents
    @agent
    def researcher(self) -> Agent:
        """
        Creates the 'researcher' agent.
        Responsible for researching AI topics and gathering actionable insights.
        """
        return Agent(
            config=self.agents_config["researcher"],
            tools=[RedditSerpApiSearchTool()],
            verbose=True,
        )

    @agent
    def writer(self) -> Agent:
        """
        Creates the 'writer' agent.
        Responsible for crafting actionable articles based on research findings.
        """
        return Agent(config=self.agents_config["writer"], verbose=True)

    @agent
    def trello_manager(self) -> Agent:
        """
        Creates the 'trello_manager' agent.
        Responsible for saving articles as Trello comments and moving cards.
        """
        return Agent(
            config=self.agents_config["trello_manager"],
            tools=[TrelloAddCardCommentTool(), TrelloUpdateCardTool()],
            verbose=True,
        )

    # Define tasks
    @task
    def research_task(self) -> Task:
        """
        Creates the 'research_task'.
        Responsible for gathering actionable insights on AI topics.
        """
        return Task(
            config=self.tasks_config["research_task"],
            output_file="research.txt",
            output_pydantic=Research,
        )

    @task
    def article_task(self) -> Task:
        """
        Creates the 'article_task'.
        Responsible for turning research findings into concise and actionable articles.
        """
        return Task(
            config=self.tasks_config["article_task"],
            output_file="article.txt",
            output_pydantic=Article,
        )

    @task
    def trello_update_task(self) -> Task:
        """
        Creates the 'trello_update_task'.
        Responsible for saving articles as comments on Trello cards and moving them to the next column.
        """
        return Task(config=self.tasks_config["trello_update_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the ProTools crew"""
        print("\nInitializing agents...")
        try:
            agents = self.agents
            print(f"Created {len(agents)} agents successfully")
            for agent in agents:
                print(f"- {agent.role}")
        except Exception as e:
            print(f"Error creating agents: {e}")
            raise
            
        print("\nInitializing tasks...")
        try:
            tasks = self.tasks
            print(f"Created {len(tasks)} tasks successfully")
            for task in tasks:
                print(f"- {task.description[:50]}...")
        except Exception as e:
            print(f"Error creating tasks: {e}")
            raise
            
        print("\nCreating crew...")
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

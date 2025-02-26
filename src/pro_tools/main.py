#!/usr/bin/env python
import sys
import warnings

print("=== Starting pro_tools.main ===")

try:
    from pro_tools.crew import ProTools
    print("Successfully imported ProTools")
except Exception as e:
    print(f"Error importing ProTools: {str(e)}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    try:
        print("\nInitializing ProTools...")
        pro_tools = ProTools()
        print("Creating crew...")
        crew = pro_tools.crew()
        print("Starting crew execution...")
        crew.kickoff()
    except Exception as e:
        print(f"\nError during execution: {str(e)}")
        import traceback
        print("\nFull error trace:")
        print(traceback.format_exc())
        sys.exit(1)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        ProTools().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ProTools().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        ProTools().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == "__main__":
    print("Entering main block")
    if len(sys.argv) < 2:
        print("No command provided")
        sys.exit(1)
        
    command = sys.argv[1]
    print(f"Received command: {command}")
    
    if command == "run":
        print("Starting run command...")
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


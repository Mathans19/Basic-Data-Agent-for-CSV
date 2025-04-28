# test_agent.py
import os
import sys
from basic_data_agent import CustomCSVDataAgent

def interactive_test(csv_path):
    """Interactive testing of the CustomCSVDataAgent"""
    # Initialize the agent
    agent = CustomCSVDataAgent()
    print(f"CSV Data Agent initialized")
    
    # Load the CSV file
    load_result = agent.load_csv(csv_path)
    print(load_result)
    print("-" * 50)
    
    # Get the filename without path for display
    file_name = os.path.basename(csv_path)
    
    print(f"Ask questions about the {file_name} dataset. Type 'exit' to quit.")
    print("Example questions:")
    print("  - How many rows are in this dataset?")
    print("  - What columns are available?")
    print("  - Show me the distribution of [column name]")
    print("  - What's the average [column name]?")
    print("-" * 50)
    
    # Enter interactive mode
    while True:
        try:
            # Get user input
            user_query = input("\nEnter your question: ")
            
            # Check if the user wants to exit
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("Exiting...")
                break
            
            # Process the query
            if user_query.strip():  # Check if not empty
                print("-" * 50)
                response = agent.process_query(user_query)
                print(f"Response:\n{response}")
                print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Get the CSV file path from command line argument or use default
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        print("No CSV file specified. Please provide a path to a CSV file.")
        print("Usage: python test_agent.py path/to/your/file.csv")
        sys.exit(1)
    
    # Check if file exists
    if not os.path.isfile(csv_path):
        print(f"Error: File '{csv_path}' not found.")
        sys.exit(1)
    
    # Run interactive test
    interactive_test(csv_path)
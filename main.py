```python
import os
import json
from dotenv import load_dotenv
from utils.file_analyzer import analyze_files
from utils.code_parser import parse_codebase
from utils.static_analyzer import map_relationships
from utils.visualization import generate_visualizations
from utils.documentation_generator import generate_documentation
from utils.progress_tracker import ProgressTracker
from cli.cli_parser import parse_cli_arguments
from api.dashboard_api import start_dashboard
from api.query_api import handle_query

# Load environment variables
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_API_KEY')

# Load configuration
with open('config.json', 'r') as config_file:
    CONFIG = json.load(config_file)

# Initialize progress tracker
progress_tracker = ProgressTracker()

def main():
    # Parse CLI arguments
    args = parse_cli_arguments()

    # Start the dashboard if the dashboard flag is set
    if args.dashboard:
        start_dashboard()

    # Analyze the codebase
    file_metadata = analyze_files(CONFIG['codebase_path'], progress_tracker)

    # Parse the codebase to get ASTs
    asts = parse_codebase(file_metadata, progress_tracker)

    # Map call relationships
    call_graph = map_relationships(asts, progress_tracker)

    # Generate visualizations
    generate_visualizations(call_graph, CONFIG['visualization_path'])

    # Generate documentation
    generate_documentation(file_metadata, asts, call_graph, API_KEY, CONFIG['documentation_path'])

    # Handle on-demand queries
    if args.query:
        handle_query(args.query)

if __name__ == "__main__":
    main()
```
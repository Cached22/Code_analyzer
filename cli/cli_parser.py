```python
import argparse
import json
import sys
from utils.file_analyzer import analyze_codebase
from utils.documentation_generator import generate_documentation
from utils.visualization import generate_visualization
from utils.progress_tracker import ProgressTracker
from utils.static_analyzer import map_call_relationships

def main():
    parser = argparse.ArgumentParser(description='Codebase Documentation Generator CLI')
    parser.add_argument('path', type=str, help='Path to the codebase directory')
    parser.add_argument('--format', type=str, choices=['md', 'html', 'json'], default='md', help='Output format for the documentation')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations for the codebase')
    parser.add_argument('--config', type=str, default='config.json', help='Path to the configuration file')

    args = parser.parse_args()

    # Load configuration settings
    try:
        with open(args.config, 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file {args.config} not found.", file=sys.stderr)
        sys.exit(1)

    # Initialize progress tracker
    progress_tracker = ProgressTracker()

    # Analyze the codebase
    file_metadata, analysis_results = analyze_codebase(args.path, config, progress_tracker)

    # Map call relationships
    call_graph = map_call_relationships(analysis_results)

    # Generate documentation
    documentation_data = generate_documentation(file_metadata, analysis_results, call_graph, args.format, config)

    # Generate visualizations if requested
    if args.visualize:
        generate_visualization(call_graph)

    # Output the documentation
    output_path = f'data/documentation_data.{args.format}'
    with open(output_path, 'w') as output_file:
        if args.format == 'json':
            json.dump(documentation_data, output_file, indent=4)
        else:
            output_file.write(documentation_data)

    print(f"Documentation has been generated at {output_path}")

if __name__ == '__main__':
    main()
```
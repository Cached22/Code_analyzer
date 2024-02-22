```python
import argparse
import sys
from utils.file_analyzer import analyze_codebase
from utils.documentation_generator import generate_documentation
from utils.visualization import generate_visualization
from utils.progress_tracker import ProgressTracker
from config import CONFIG

def main():
    parser = argparse.ArgumentParser(description='Codebase Documentation Generator CLI')
    parser.add_argument('action', choices=['analyze', 'generate-docs', 'visualize', 'progress'], help='Action to perform')
    parser.add_argument('--path', help='Path to the codebase directory', default=CONFIG['default_path'])
    parser.add_argument('--depth', type=int, help='Depth for recursive directory traversal', default=CONFIG['default_depth'])
    parser.add_argument('--output', help='Output format for documentation', choices=['md', 'html', 'json'], default=CONFIG['default_output'])
    parser.add_argument('--file', help='Specific file for on-demand visualization')
    args = parser.parse_args()

    progress_tracker = ProgressTracker()

    if args.action == 'analyze':
        progress_tracker.start()
        analyze_codebase(args.path, args.depth, progress_tracker)
        progress_tracker.complete()

    elif args.action == 'generate-docs':
        generate_documentation(args.path, args.output)

    elif args.action == 'visualize':
        if args.file:
            generate_visualization(args.file, single_file=True)
        else:
            generate_visualization(args.path, single_file=False)

    elif args.action == 'progress':
        progress = progress_tracker.get_progress()
        print(f"Current progress: {progress}%")

if __name__ == '__main__':
    main()
```
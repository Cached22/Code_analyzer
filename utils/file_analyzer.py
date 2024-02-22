```python
import os
import json
from utils.progress_tracker import track_progress

# Define the maximum depth for directory traversal
MAX_DEPTH = 5

def extract_metadata(file_path):
    """
    Extract metadata from a file such as name, size, and type.
    """
    try:
        file_stats = os.stat(file_path)
        file_metadata = {
            'name': os.path.basename(file_path),
            'size': file_stats.st_size,
            'type': 'directory' if os.path.isdir(file_path) else 'file'
        }
        return file_metadata
    except OSError as e:
        print(f"Error extracting metadata for {file_path}: {e}")
        return None

def traverse_directory(directory_path, depth=0):
    """
    Recursively traverse the directory tree up to a specified depth and extract metadata.
    """
    if depth > MAX_DEPTH:
        return []

    file_list = []
    try:
        with os.scandir(directory_path) as it:
            for entry in it:
                if entry.is_file():
                    file_metadata = extract_metadata(entry.path)
                    if file_metadata:
                        file_list.append(file_metadata)
                elif entry.is_dir():
                    file_list.extend(traverse_directory(entry.path, depth + 1))
    except OSError as e:
        print(f"Error traversing {directory_path}: {e}")

    return file_list

def analyze_codebase(start_path):
    """
    Analyze the entire codebase starting from the given path.
    """
    if not os.path.exists(start_path):
        print(f"The path {start_path} does not exist.")
        return []

    file_metadata_list = traverse_directory(start_path)
    total_files = len(file_metadata_list)
    for index, file_metadata in enumerate(file_metadata_list):
        # Placeholder for further analysis like parsing code, generating descriptions, etc.
        # This will be implemented in other utility modules like code_parser.py, etc.
        track_progress(index + 1, total_files)

    return file_metadata_list

def save_metadata_to_file(metadata, output_file='data/file_metadata.json'):
    """
    Save the extracted metadata to a JSON file.
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=4)
    except IOError as e:
        print(f"Error saving metadata to {output_file}: {e}")

if __name__ == "__main__":
    # Example usage:
    # Start the analysis from the current directory or a specified start path
    start_path = '.'
    metadata = analyze_codebase(start_path)
    save_metadata_to_file(metadata)
```
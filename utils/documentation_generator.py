```python
import os
import json
import openai
from utils.file_analyzer import extract_metadata
from utils.code_parser import parse_code
from utils.static_analyzer import map_call_relationships
from utils.visualization import generate_visualization
from utils.progress_tracker import track_progress
from data.file_metadata import FILE_METADATA_SCHEMA
from data.analysis_results import ANALYSIS_RESULTS_SCHEMA

# Load the OpenAI API key from an environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

# Function to generate file descriptions using OpenAI
def generate_description(file_content):
    openai.api_key = API_KEY
    response = openai.Completion.create(
        engine="gpt-4-0125-preview",
        prompt=f"Describe the following code:\n\n{file_content}\n",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to format documentation in Markdown, HTML, JSON
def format_documentation(file_metadata, file_descriptions, file_relationships, output_format):
    if output_format == 'markdown':
        return generate_markdown_documentation(file_metadata, file_descriptions, file_relationships)
    elif output_format == 'html':
        return generate_html_documentation(file_metadata, file_descriptions, file_relationships)
    elif output_format == 'json':
        return json.dumps({
            'metadata': file_metadata,
            'descriptions': file_descriptions,
            'relationships': file_relationships
        }, indent=4)
    else:
        raise ValueError("Unsupported output format")

# Helper function to generate Markdown documentation
def generate_markdown_documentation(file_metadata, file_descriptions, file_relationships):
    markdown_content = "# Codebase Documentation\n\n"
    for file, metadata in file_metadata.items():
        markdown_content += f"## {file}\n"
        markdown_content += f"**Description:** {file_descriptions[file]}\n\n"
        markdown_content += f"**Size:** {metadata['size']} bytes\n"
        markdown_content += f"**Type:** {metadata['type']}\n"
        markdown_content += f"**Calls:** {', '.join(file_relationships.get(file, []))}\n\n"
    return markdown_content

# Helper function to generate HTML documentation
def generate_html_documentation(file_metadata, file_descriptions, file_relationships):
    html_content = "<html><head><title>Codebase Documentation</title></head><body>"
    html_content += "<h1>Codebase Documentation</h1>"
    for file, metadata in file_metadata.items():
        html_content += f"<h2>{file}</h2>"
        html_content += f"<p><strong>Description:</strong> {file_descriptions[file]}</p>"
        html_content += f"<p><strong>Size:</strong> {metadata['size']} bytes</p>"
        html_content += f"<p><strong>Type:</strong> {metadata['type']}</p>"
        html_content += f"<p><strong>Calls:</strong> {', '.join(file_relationships.get(file, []))}</p>"
    html_content += "</body></html>"
    return html_content

# Main function to generate documentation for a codebase
def generate_documentation(codebase_path, output_format='markdown'):
    file_metadata = {}
    file_descriptions = {}
    file_relationships = {}
    total_files = sum([len(files) for r, d, files in os.walk(codebase_path)])
    analyzed_files = 0

    for root, dirs, files in os.walk(codebase_path):
        for file in files:
            file_path = os.path.join(root, file)
            metadata = extract_metadata(file_path)
            file_metadata[file_path] = metadata
            with open(file_path, 'r') as f:
                content = f.read()
            ast = parse_code(content)
            descriptions = generate_description(content)
            file_descriptions[file_path] = descriptions
            relationships = map_call_relationships(ast)
            file_relationships[file_path] = relationships
            analyzed_files += 1
            track_progress(analyzed_files, total_files)

    documentation = format_documentation(file_metadata, file_descriptions, file_relationships, output_format)
    return documentation

# Save the documentation to a file
def save_documentation(documentation, output_path, output_format):
    if output_format == 'markdown':
        extension = '.md'
    elif output_format == 'html':
        extension = '.html'
    elif output_format == 'json':
        extension = '.json'
    else:
        raise ValueError("Unsupported output format")

    with open(os.path.join(output_path, f"documentation{extension}"), 'w') as f:
        f.write(documentation)

# Example usage
if __name__ == "__main__":
    codebase_path = 'path/to/codebase'
    documentation = generate_documentation(codebase_path)
    save_documentation(documentation, 'path/to/output', 'markdown')
```
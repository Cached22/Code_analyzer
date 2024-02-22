```python
from flask import Flask, request, jsonify
from utils.file_analyzer import extract_metadata
from utils.code_parser import parse_code
from utils.static_analyzer import map_call_relationships
from utils.documentation_generator import format_documentation
from utils.visualization import generate_visualization
from utils.progress_tracker import get_progress
from config import API_KEY, CONFIG
import openai

app = Flask(__name__)

@app.route('/query/metadata', methods=['GET'])
def query_metadata():
    file_path = request.args.get('file_path', '')
    if file_path:
        metadata = extract_metadata(file_path)
        return jsonify(metadata)
    else:
        return jsonify({"error": "No file path provided"}), 400

@app.route('/query/parse_code', methods=['GET'])
def query_parse_code():
    file_path = request.args.get('file_path', '')
    if file_path:
        ast = parse_code(file_path)
        return jsonify(ast)
    else:
        return jsonify({"error": "No file path provided"}), 400

@app.route('/query/call_relationships', methods=['GET'])
def query_call_relationships():
    file_path = request.args.get('file_path', '')
    if file_path:
        relationships = map_call_relationships(file_path)
        return jsonify(relationships)
    else:
        return jsonify({"error": "No file path provided"}), 400

@app.route('/query/generate_description', methods=['GET'])
def query_generate_description():
    file_path = request.args.get('file_path', '')
    if file_path:
        metadata = extract_metadata(file_path)
        ast = parse_code(file_path)
        openai.api_key = API_KEY
        response = openai.Completion.create(
            engine="gpt-4-0125-preview",
            prompt=f"Describe the following file based on its metadata and AST: {metadata} {ast}",
            max_tokens=150
        )
        return jsonify({"description": response.choices[0].text})
    else:
        return jsonify({"error": "No file path provided"}), 400

@app.route('/query/generate_visualization', methods=['GET'])
def query_generate_visualization():
    file_path = request.args.get('file_path', '')
    if file_path:
        visualization = generate_visualization(file_path)
        return jsonify({"visualization": visualization})
    else:
        return jsonify({"error": "No file path provided"}), 400

@app.route('/query/documentation', methods=['GET'])
def query_documentation():
    file_path = request.args.get('file_path', '')
    doc_format = request.args.get('format', 'json')
    if file_path:
        documentation = format_documentation(file_path, doc_format)
        return jsonify({"documentation": documentation})
    else:
        return jsonify({"error": "No file path provided"}), 400

@app.route('/query/progress', methods=['GET'])
def query_progress():
    progress = get_progress()
    return jsonify({"progress": progress})

if __name__ == '__main__':
    app.run(debug=CONFIG['debug'], host=CONFIG['host'], port=CONFIG['port'])
```
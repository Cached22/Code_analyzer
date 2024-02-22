```python
import os
import json
from tree_sitter import Language, Parser

# Load shared dependencies from config
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    LANGUAGE_SO_PATH = config.get('LANGUAGE_SO_PATH', './tree-sitter-languages.so')
    LANGUAGE_NAME = config.get('LANGUAGE_NAME', 'python')

# Load the language shared library
Language.build_library(
    # Store the library in the `build` directory
    LANGUAGE_SO_PATH,
    # Include one or more languages
    [
        'tree-sitter-python',
    ]
)

PYTHON_LANGUAGE = Language(LANGUAGE_SO_PATH, LANGUAGE_NAME)
parser = Parser()
parser.set_language(PYTHON_LANGUAGE)

def parse_code(file_path):
    """
    Parse the code at the given file path using tree-sitter and return the AST.
    """
    try:
        with open(file_path, 'r') as code_file:
            code = code_file.read()
        
        tree = parser.parse(bytes(code, "utf8"))
        return tree.root_node
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return None

def get_functions_and_classes_from_ast(ast):
    """
    Given an AST, extract and return a list of functions and classes.
    """
    functions = []
    classes = []
    if ast:
        for node in ast.walk():
            if node.type == 'function_definition':
                functions.append(node)
            elif node.type == 'class_definition':
                classes.append(node)
    return functions, classes

def analyze_file(file_path):
    """
    Analyze a single file to extract functions, classes and their relationships.
    """
    ast = parse_code(file_path)
    functions, classes = get_functions_and_classes_from_ast(ast)
    return {
        'functions': [func.text for func in functions],
        'classes': [cls.text for cls in classes]
    }

if __name__ == "__main__":
    # Example usage
    file_analysis = analyze_file('example.py')
    print(json.dumps(file_analysis, indent=2))
```
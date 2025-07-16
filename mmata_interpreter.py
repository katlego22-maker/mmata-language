import json
import sys
import os

# Global variable store
variables = {}

def load_dictionary(language_code):
    """Load language-specific keyword dictionary."""
    path = f"languages/{language_code}.json"
    if not os.path.exists(path):
        print(f"[Language pack not found: {language_code}]")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_line(line, dictionary):
    """Determine the action and content from a line."""
    for keyword, command in dictionary.items():
        if line.startswith(keyword):
            return command, line[len(keyword):].strip()
    return None, None

def handle_declare(content):
    try:
        var, value = content.split("=")
        var, value = var.strip(), value.strip()
        value = int(value) if value.isdigit() else variables.get(value, value)
        variables[var] = value
    except ValueError:
        print(f"[Invalid declare syntax: {content}]")

def handle_update(content):
    handle_declare(content)  # same logic as declare

def handle_input(content):
    var = content.strip()
    user_input = input(f"{var} => ")
    variables[var] = user_input

def handle_print(content):
    if "+" in content:
        text, var = content.split("+", 1)
        text, var = text.strip().strip('"'), var.strip()
        print(text + str(variables.get(var, f"[{var} not found]")))
    else:
        if content.startswith('"') and content.endswith('"'):
            print(content.strip('"'))
        else:
            print(variables.get(content, f"[{content} not found]"))

# Action dispatch table
handlers = {
    "declare": handle_declare,
    "update": handle_update,
    "input": handle_input,
    "print": handle_print
}

def run_program(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    language = "english"

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Language detection
        if line.startswith("#lang:"):
            language = line.replace("#lang:", "").strip()
            dictionary = load_dictionary(language)
            continue

        if line.startswith("mmata") or line.endswith("."):
            line = line.replace("mmata", "").strip().rstrip(".")

        if not line:
            continue

        action, content = parse_line(line, dictionary)
        if action in handlers:
            handlers[action](content)
        else:
            print(f"[Unknown command: {line}]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mata.py program.ml")
        sys.exit(1)

    run_program(sys.argv[1])

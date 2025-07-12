import json

# Load the dictionary
with open("dictionary.json", "r", encoding="utf-8") as dict_file:
    dictionary = json.load(dict_file)

# Store variables
variables = {}

# Load the .ml code
with open("program.ml", "r", encoding="utf-8") as ml_file:
    lines = ml_file.readlines()

for line in lines:
    line = line.strip()

    if line == "" or line.startswith("mmata"):
        continue

    if line.endswith("."):
        line = line[:-1]

    # Find keyword in any language
    for keyword, command in dictionary.items():
        if line.startswith(keyword):
            action = command
            content = line[len(keyword):].strip()
            break
    else:
        print(f"[Unknown command in line: {line}]")
        continue

    # DECLARE
    if action == "declare":
        var, value = content.split("=")
        var = var.strip()
        value = value.strip()
        if value.isdigit():
            value = int(value)
        elif value in variables:
            value = variables[value]
        variables[var] = value

    # UPDATE
    elif action == "update":
        var, value = content.split("=")
        var = var.strip()
        value = value.strip()
        if value.isdigit():
            value = int(value)
        elif value in variables:
            value = variables[value]
        variables[var] = value

    # PRINT
    elif action == "print":
        if "+" in content:
            text, var = content.split("+", 1)
            text = text.strip().strip('"')
            var = var.strip()
            print(text + str(variables.get(var, f"[{var} not found]")))
        else:
            if content.startswith('"') and content.endswith('"'):
                print(content.strip('"'))
            elif content in variables:
                print(variables[content])
            else:
                print(f"[{content} not found]")

    # INPUT
    elif action == "input":
        var = content.strip()
        user_input = input(f"{var} => ")
        variables[var] = user_input

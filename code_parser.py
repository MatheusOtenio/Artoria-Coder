import os
import ast

def analyze_project(project_path):
    structure = {"files": []}
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    try:
                        tree = ast.parse(content)
                        functions = [
                            node.name 
                            for node in ast.walk(tree) 
                            if isinstance(node, ast.FunctionDef)
                        ]
                        structure["files"].append({
                            "path": file_path,
                            "functions": functions,
                            "content": content[:2000]  # Limita o conteúdo
                        })
                    except:
                        pass
    return structure
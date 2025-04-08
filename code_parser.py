import os
import ast
from tree_sitter import Language, Parser
from pathlib import Path

# Configurar parsers do Tree-sitter
LANGUAGES = {
    'python': 'vendors/tree-sitter-python',
    'javascript': 'vendors/tree-sitter-javascript',
    'java': 'vendors/tree-sitter-java'
}

# Baixar parsers (executar uma vez)
def setup_parsers():
    for lang, repo in LANGUAGES.items():
        Language.build_library(
            f'vendors/{lang}.so',
            [repo]
        )
        
def analyze_project(self, project_path):
    return self.analyze_project(project_path)
class CodeParser:
    def __init__(self):
        self.parsers = {}
        for lang in LANGUAGES:
            self.parsers[lang] = Parser()
            self.parsers[lang].set_language(
                Language(f'vendors/{lang}.so', lang)
            )
        
        self.file_types = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java'
        }

    def parse_file(self, file_path):
        file_type = self.file_types.get(Path(file_path).suffix)
        if not file_type:
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            tree = self.parsers[file_type].parse(bytes(content, 'utf8'))
            return self._extract_structure(tree, file_type, content)
        except Exception as e:
            return {'error': str(e)}

    def _extract_structure(self, tree, lang, content):
        # Implementar para cada linguagem
        if lang == 'python':
            return self._parse_python(content)
        elif lang == 'javascript':
            return self._parse_javascript(tree)
        # ...

    def _parse_python(self, content):
        # Usar AST tradicional para Python
        parsed = {
            'functions': [],
            'classes': [],
            'imports': []
        }
        try:
            module = ast.parse(content)
            for node in module.body:
                if isinstance(node, ast.FunctionDef):
                    parsed['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    parsed['classes'].append(node.name)
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    parsed['imports'].append(ast.unparse(node))
        except:
            pass
        return parsed

    def analyze_project(self, project_path):
        structure = {'languages': {}, 'files': []}
        for root, _, files in os.walk(project_path):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_types):
                    file_path = os.path.join(root, file)
                    file_data = self.parse_file(file_path)
                    if file_data:
                        structure['files'].append({
                            'path': file_path,
                            'type': Path(file_path).suffix[1:],
                            'data': file_data
                        })
                        lang = self.file_types[Path(file_path).suffix]
                        structure['languages'][lang] = structure['languages'].get(lang, 0) + 1
        return structure
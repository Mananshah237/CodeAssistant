import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.variables = {}  # Tracks variable assignments and uses
        self.issues = []     # Stores detected problems

    def visit_Assign(self, node):
        # Track variables being assigned
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables[target.id] = {"assigned": True, "used": False}
        self.generic_visit(node)

    def visit_Name(self, node):
        # Mark variables as used when referenced
        if node.id in self.variables and isinstance(node.ctx, (ast.Load)):
            self.variables[node.id]["used"] = True
        self.generic_visit(node)

    def report(self):
        # Find unused variables
        for var, info in self.variables.items():
            if info["assigned"] and not info["used"]:
                self.issues.append(f"Variable '{var}' assigned but never used")
        return self.issues

def analyze_code(code):
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    issues = analyzer.report()
    return "\n".join(issues) if issues else "No issues found"

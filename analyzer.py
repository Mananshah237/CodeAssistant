import ast
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.variables = {}
        self.issues = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables[target.id] = {"assigned": True, "used": False}
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in self.variables and isinstance(node.ctx, (ast.Load)):
            self.variables[node.id]["used"] = True
        self.generic_visit(node)

    def report(self):
        for var, info in self.variables.items():
            if info["assigned"] and not info["used"]:
                self.issues.append(f"Variable '{var}' assigned but never used")
        return self.issues

# Load a lightweight code model (e.g., CodeT5, but we'll start simple)
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-small")

import ast
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-small")

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.variables = {}
        self.issues = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables[target.id] = {"assigned": True, "used": False}
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in self.variables and isinstance(node.ctx, (ast.Load)):
            self.variables[node.id]["used"] = True
        self.generic_visit(node)

    def report(self):
        for var, info in self.variables.items():
            if info["assigned"] and not info["used"]:
                self.issues.append(f"Variable '{var}' assigned but never used")
        return self.issues

import ast
from transformers import AutoTokenizer, LlamaForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/CodeLlama-7b-hf")
model = LlamaForCausalLM.from_pretrained("meta-llama/CodeLlama-7b-hf")

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.variables = {}
        self.issues = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables[target.id] = {"assigned": True, "used": False}
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in self.variables and isinstance(node.ctx, ast.Load):
            self.variables[node.id]["used"] = True
        self.generic_visit(node)

    def report(self):
        for var, info in self.variables.items():
            if info["assigned"] and not info["used"]:
                self.issues.append(f"Variable '{var}' assigned but never used")
        return self.issues

def analyze_code(code):
    # AST analysis
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    issues = analyzer.report()
    ast_result = "\n".join(issues) if issues else "No issues found"

    # CodeLlama suggestion
    prompt = f"Python code:\n{code}\nIssue: {ast_result}\nSuggest a fix:\n"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,  # Focus on new tokens, not total length
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )
    suggestion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Clean up suggestion
    if suggestion.startswith(prompt):
        suggestion = suggestion[len(prompt):].strip()

    return f"{ast_result}\nAI Suggestion: {suggestion}"
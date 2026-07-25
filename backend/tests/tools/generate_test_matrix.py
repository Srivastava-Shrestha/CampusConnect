import ast
import json
from pathlib import Path

RESULTS_PATH = "tests/reports/results_log.json"
OUTPUT_PATH = "tests/test-cases/api-test-matrix.md"


def extract_docstrings(test_file):
    source = Path(test_file).read_text()
    tree = ast.parse(source)
    result = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)) and node.name.startswith("test_"):
            result[node.name] = ast.get_docstring(node) or ""
    return result


def extract_test_details(test_file, func_name):
    source = Path(test_file).read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)) and node.name == func_name:
            api = None
            inputs = None
            expected_parts = []
            local_vars = {}

            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Assign):
                    try:
                        value = ast.literal_eval(stmt.value)
                        if isinstance(value, dict):
                            for target in stmt.targets:
                                if isinstance(target, ast.Name):
                                    local_vars[target.id] = value
                    except Exception:
                        pass

            # look for HTTP calls first (integration tests)
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Attribute):
                    if stmt.func.attr in ("post", "get", "put", "delete", "patch"):
                        method = stmt.func.attr.upper()
                        if stmt.args:
                            try:
                                url = ast.literal_eval(stmt.args[0])
                                api = f"{method} {url}"
                            except Exception:
                                pass
                        for kw in stmt.keywords:
                            if kw.arg == "json":
                                if isinstance(kw.value, ast.Name) and kw.value.id in local_vars:
                                    inputs = json.dumps(local_vars[kw.value.id])
                                else:
                                    try:
                                        inputs = json.dumps(ast.literal_eval(kw.value))
                                    except Exception:
                                        inputs = "see test code"

                if isinstance(stmt, ast.Assert):
                    try:
                        expected_parts.append(ast.unparse(stmt.test))
                    except Exception:
                        pass
                if isinstance(stmt, ast.With):
                    for item in stmt.items:
                        call = item.context_expr
                        if isinstance(call, ast.Call) and getattr(call.func, "attr", "") == "raises":
                            exc_name = ast.unparse(call.args[0]) if call.args else "Exception"
                            expected_parts.append(f"raises {exc_name}")

            # if no HTTP call found, look for a plain function call instead (unit tests)
            if api is None:
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Name):
                        func_called = stmt.func.id
                        if func_called.startswith("test_"):
                            continue
                        try:
                            args_repr = ", ".join(ast.unparse(a) for a in stmt.args)
                            api = f"{func_called}()"
                            inputs = args_repr if args_repr else "no arguments"
                        except Exception:
                            api = f"{func_called}()"
                            inputs = "see test code"

            expected = " AND ".join(expected_parts) if expected_parts else "see test code"
            return api or "N/A", inputs or "N/A", expected
    return "N/A", "N/A", "see test code"


def load_results(results_path):
    with open(results_path) as f:
        return json.load(f)


def build_table(results):
    lines = ["# API Test Case Matrix", ""]
    lines.append("| Test Case ID | API | Inputs | Expected Output | Actual Output | Result |")
    lines.append("|---|---|---|---|---|---|")

    docstring_cache = {}

    for i, r in enumerate(results, start=1):
        node_id = r["test"]
        test_file, func_name = node_id.split("::")
        outcome = r["outcome"]

        if test_file not in docstring_cache:
            docstring_cache[test_file] = extract_docstrings(test_file)
        raw_doc = docstring_cache[test_file].get(func_name, func_name.replace("_", " "))
        doc = raw_doc.replace("|", "-").strip()

        api, inputs, expected = extract_test_details(test_file, func_name)

        if outcome == "passed":
            actual = expected
            result = "Success"
        else:
            raw_error = r["error"] or "Failed"
            actual = raw_error.replace("\n", " ").replace("|", "-").strip()
            result = "Fail"

        if "unit" in test_file:
            prefix = "UT"
        elif "integration" in test_file:
            prefix = "IT"
        else:
            prefix = "TC"

        case_id = f"{prefix}-{i:03d}"
        lines.append(f"| {case_id} | {api} | `{inputs}` | `{expected}` ({doc}) | `{actual}` | {result} |")

    return "\n".join(lines)


if __name__ == "__main__":
    results = load_results(RESULTS_PATH)
    table = build_table(results)

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text(table)
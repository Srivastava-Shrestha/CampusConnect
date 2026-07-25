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
        if isinstance(node, ast.AsyncFunctionDef) and node.name.startswith("test_"):
            result[node.name] = ast.get_docstring(node) or ""
    return result


def extract_test_details(test_file, func_name):
    source = Path(test_file).read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == func_name:
            api = "?"
            inputs = "?"
            expected_parts = []
            local_vars = {}

            # first pass: capture any variable = {...} assignments in this test
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

            # second pass: find the actual API call
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

            expected = " AND ".join(expected_parts) if expected_parts else "?"
            return api, inputs, expected
    return "?", "?", "?"


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
        doc = raw_doc.replace("|", "-").strip()  # sanitize pipes

        api, inputs, expected = extract_test_details(test_file, func_name)

        if outcome == "passed":
            actual = expected
            result = "Success"
        else:
            raw_error = r["error"] or "Failed"
            actual = raw_error.replace("\n", " ").replace("|", "-").strip()
            result = "Fail"

        case_id = f"TC-{i:03d}"
        lines.append(f"| {case_id} | {api} | `{inputs}` | `{expected}` ({doc}) | `{actual}` | {result} |")

    return "\n".join(lines)


if __name__ == "__main__":
    results = load_results(RESULTS_PATH)
    table = build_table(results)

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text(table)
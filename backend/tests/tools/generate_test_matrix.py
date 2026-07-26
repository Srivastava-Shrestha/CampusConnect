import ast
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_PATH = ROOT_DIR / "tests/reports/results_log.json"
OUTPUT_PATH = ROOT_DIR / "tests/test-cases/api-test-matrix.md"


def extract_docstrings(test_file):
    source = (ROOT_DIR / test_file).read_text()
    tree = ast.parse(source)
    result = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)) and node.name.startswith("test_"):
            result[node.name] = ast.get_docstring(node) or ""
    return result


def extract_test_details(test_file, func_name):
    source = (ROOT_DIR / test_file).read_text()
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


def simplify_expected(expected_parts):
    simplified = []
    has_access_token = False
    has_refresh_token = False
    for part in expected_parts:
        if "status_code ==" in part:
            try:
                code = part.split("==")[1].strip()
                simplified.append(f"Status: `{code}`")
            except Exception:
                simplified.append(part)
        elif "status_code in" in part:
            try:
                opts = part.split("in")[1].strip()
                simplified.append(f"Status: `{opts}`")
            except Exception:
                simplified.append(part)
        elif "message' ==" in part or 'message" ==' in part or "message] ==" in part:
            try:
                msg = part.split("==")[1].strip()
                simplified.append(f"Message: {msg}")
            except Exception:
                simplified.append(part)
        elif "access_token" in part:
            has_access_token = True
        elif "refresh_token" in part:
            has_refresh_token = True
        elif part.startswith("raises "):
            simplified.append(part)
        else:
            if "==" in part:
                try:
                    left, right = part.split("==", 1)
                    left = left.strip()
                    right = right.strip()
                    if "body[" in left:
                        key = left.split("body[")[1].split("]")[0].strip("'\"")
                        simplified.append(f"{key.capitalize()}: {right}")
                    else:
                        simplified.append(f"`{part}`")
                except Exception:
                    simplified.append(f"`{part}`")
            else:
                simplified.append(f"`{part}`")

    if has_access_token or has_refresh_token:
        tokens = []
        if has_access_token:
            tokens.append("access_token")
        if has_refresh_token:
            tokens.append("refresh_token")
        simplified.append(f"Tokens: {', '.join(tokens)}")

    return "<br>".join(simplified)


def extract_actual_error(raw_error: str) -> str:
    """
    Pull the real assertion message out of a stored pytest error string.

    conftest.py stores errors as str(call.excinfo.value), e.g.:
        assert ' knit' == 'knit'

          - knit
          +  knit
          ? +

    This is the raw exception message, NOT pytest's terminal-rendered
    traceback -- it has no "E " prefixes (those are added by pytest's
    terminal reporter only when printing to the console, and are not
    part of the exception string itself). The FIRST line is always the
    actual assertion/exception message; every line after that is the
    diff renderer's context (blank lines, "-", "+", "?" markers) and
    must not be used as a substitute for the real message.
    """
    lines_err = [l for l in raw_error.split("\n") if l.strip()]
    return lines_err[0].strip() if lines_err else "Failed"


def load_results(results_path):
    with open(results_path) as f:
        return json.load(f)


def build_table(results):
    lines = ["# API Test Case Matrix", ""]

    def get_category_name(test_file):
        path = Path(test_file)
        is_unit = "unit" in path.parts
        module_name = path.stem.replace("test_", "").replace("_", " ").title()
        test_type = "Unit Tests" if is_unit else "Integration Tests"
        return f"{module_name} {test_type}"

    grouped_results = {}
    for r in results:
        node_id = r["test"]
        test_file, _ = node_id.split("::")
        cat = get_category_name(test_file)
        if cat not in grouped_results:
            grouped_results[cat] = []
        grouped_results[cat].append(r)

    docstring_cache = {}
    test_count = 1

    # Group categories dynamically (Integration first, then Unit)
    integration_cats = sorted([c for c in grouped_results.keys() if "Integration Tests" in c])
    unit_cats = sorted([c for c in grouped_results.keys() if "Unit Tests" in c])
    other_cats = sorted([c for c in grouped_results.keys() if c not in integration_cats and c not in unit_cats])

    all_cats = integration_cats + unit_cats + other_cats

    for cat in all_cats:
        lines.append(f"## {cat}")
        lines.append("")
        lines.append("| Test ID | Description | API / Function | Inputs | Expected Output | Actual Output | Result |")
        lines.append("|---|---|---|---|---|---|---|")

        for r in grouped_results[cat]:
            node_id = r["test"]
            test_file, func_name = node_id.split("::")
            outcome = r["outcome"]

            if test_file not in docstring_cache:
                docstring_cache[test_file] = extract_docstrings(test_file)
            raw_doc = docstring_cache[test_file].get(func_name, func_name.replace("_", " "))
            doc = raw_doc.replace("|", "-").strip()

            api, inputs, expected_raw = extract_test_details(test_file, func_name)

            expected_parts = [p.strip() for p in expected_raw.split(" AND ") if p.strip()]
            expected = simplify_expected(expected_parts)

            if outcome == "passed":
                actual = expected
                result = "Success"
            else:
                raw_error = r["error"] or "Failed"
                assert_err = extract_actual_error(raw_error)
                actual = f"<code>{assert_err}</code>"
                result = "Fail"

            if "unit" in test_file:
                prefix = "UT"
            else:
                prefix = "IT"
            case_id = f"**{prefix}-{test_count:03d}**"
            test_count += 1

            inputs_fmt = f"`{inputs}`" if inputs != "N/A" and inputs != "see test code" else inputs
            api_fmt = f"`{api}`" if api != "N/A" else api

            lines.append(f"| {case_id} | {doc} | {api_fmt} | {inputs_fmt} | {expected} | {actual} | {result} |")

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    results = load_results(RESULTS_PATH)
    table = build_table(results)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(table)
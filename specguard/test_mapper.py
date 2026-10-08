import ast
from pathlib import Path


def find_requirement_tests(tests_directory):
    """
    Scan Python test files and map requirement IDs
    to the tests associated with them.

    Returns:
        dict: requirement ID -> list of test names
    """

    requirement_map = {}

    test_files = Path(tests_directory).glob("test_*.py")

    for test_file in test_files:

        source_code = test_file.read_text(encoding="utf-8")

        tree = ast.parse(source_code)

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                for decorator in node.decorator_list:

                    if not isinstance(decorator, ast.Call):
                        continue

                    function = decorator.func

                    if not isinstance(function, ast.Attribute):
                        continue

                    if function.attr != "requirement":
                        continue

                    if not decorator.args:
                        continue

                    argument = decorator.args[0]

                    if isinstance(argument, ast.Constant):

                        requirement_id = argument.value

                        requirement_map.setdefault(
                            requirement_id, []
                        ).append(node.name)

    return requirement_map
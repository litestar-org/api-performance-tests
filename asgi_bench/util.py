from .types import TestResult


def has_error_results(test_results: list[TestResult] | TestResult) -> bool:
    if not isinstance(test_results, list):
        test_results = [test_results]
    return any(result["req4xx"] or result["req5xx"] or result["others"] for result in test_results)

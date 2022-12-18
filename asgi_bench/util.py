from .types import TestResult


def get_error_response_count(test_result: TestResult) -> int:
    return test_result["req4xx"] + test_result["req5xx"] + test_result.get("others", 0)


def get_success_response_count(test_result: TestResult) -> int:
    return test_result["req1xx"] + test_result["req2xx"] + test_result["req3xx"]


def get_error_percentage(test_result: TestResult) -> float:
    success_count = get_success_response_count(test_result)
    error_count = get_error_response_count(test_result)
    total_count = success_count + error_count
    if not error_count:
        return 0
    return 100 * (error_count / total_count)


def has_no_responses(test_result: TestResult) -> bool:
    return not get_error_response_count(test_result) + get_success_response_count(test_result)

import json
from pathlib import Path

data_path = Path("test_data")

RESPONSE_FILE_100B = Path("test_data/100B").resolve()
RESPONSE_FILE_1K = Path("test_data/1K").resolve()
RESPONSE_FILE_50K = Path("test_data/50K").resolve()
RESPONSE_FILE_1M = Path("test_data/1M").resolve()

TEXT_6k = (data_path / "text_6k").read_text()
TEXT_70k = (data_path / "test_70k").read_text()

JSON_SIMPLE = {f"key_{i}": "value" for i in range(10)}
JSON_2K = json.loads((data_path / "random_2k.json").read_text())
JSON_10K = json.loads((data_path / "random_10k.json").read_text())
JSON_450K = json.loads((data_path / "random_450k.json").read_text())


RESPONSE_HEADERS = {f"header_{i}": "value" for i in range(10)}
RESPONSE_COOKIES = {f"cookie_{i}": "value" for i in range(10)}

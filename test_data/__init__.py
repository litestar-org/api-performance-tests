import json
from pathlib import Path

RESPONSE_HEADERS = {f"header_{i}": "value" for i in range(10)}
RESPONSE_COOKIES = {f"cookie_{i}": "value" for i in range(10)}

data_path = Path(__file__).parent

FILE_100B = (data_path / "100B").resolve()
FILE_1K = (data_path / "1K").resolve()
FILE_10K = (data_path / "10K").resolve()
FILE_100K = (data_path / "100K").resolve()
FILE_500K = (data_path / "500K").resolve()
FILE_1M = (data_path / "1M").resolve()
FILE_5M = (data_path / "5M").resolve()

TEXT_100B = (data_path / "100B.txt").read_text()
TEXT_1K = (data_path / "1K.txt").read_text()
TEXT_10K = (data_path / "10K.txt").read_text()
TEXT_100K = (data_path / "100K.txt").read_text()
TEXT_500K = (data_path / "500K.txt").read_text()
TEXT_1M = (data_path / "1M.txt").read_text()
TEXT_5M = (data_path / "5M.txt").read_text()


JSON_SIMPLE = {f"key_{i}": "value" for i in range(10)}
JSON_1K = json.loads((data_path / "1K.json").read_text())
JSON_10K = json.loads((data_path / "10K.json").read_text())
JSON_100K = json.loads((data_path / "100K.json").read_text())
JSON_500K = json.loads((data_path / "500K.json").read_text())
JSON_1M = json.loads((data_path / "1M.json").read_text())
JSON_5M = json.loads((data_path / "5M.json").read_text())

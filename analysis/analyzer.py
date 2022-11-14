import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

root_dir = Path(__file__).parent.parent
results_dir = root_dir / "results"

_test_data = []
for file in results_dir.glob("*.json"):
    _framework, _sync_async, _test_type, *_ = file.name.split("-")

    with open(file) as f:
        raw_test_data = json.load(f)
        _url, _num_requests = raw_test_data["url"], raw_test_data["2xx"]

    _benchmark_code = "/a-" if _sync_async == "async" else "/s-"
    if "/128" in _url:
        _benchmark_code += "pp"
    elif "query-param" in _url:
        _benchmark_code += "qp"
    elif "mixed-params" in _url:
        _benchmark_code += "mp"
    else:
        _benchmark_code += "np"

    _test_data.append(
        {
            "framework": _framework,
            "sync_async": _sync_async,
            "test_type": _test_type,
            "url": _url,
            "benchmark_code": _benchmark_code,
            "num_requests": _num_requests,
        }
    )

df_test_data = pd.DataFrame(_test_data)


_df_test_data = df_test_data[df_test_data["test_type"] == "plaintext"]
frameworks = df_test_data["framework"].unique()
benchmark_codes = sorted(df_test_data["benchmark_code"].unique())

fig, ax = plt.subplots(figsize=(8.2, 4.8))

sns.barplot(
    data=_df_test_data,
    x="benchmark_code",
    y="num_requests",
    hue="framework",
    hue_order=frameworks,
    order=benchmark_codes,
    palette=["#30323D", "#42577a", "#5C80BC", "#f5d23d", "#c8c9c5"],
    edgecolor="#FFFFFF",
    errorbar=None,
    width=0.7,
    ax=ax,
).set(
    title="Requests Processed - (higher is better)",
)
ax.yaxis.set_major_formatter(lambda i, pos: str(int(i / 1000)) + "k")
ax.legend(bbox_to_anchor=(1.02, 1), borderaxespad=0)
fig.tight_layout()
fig.savefig(root_dir / "result.png")

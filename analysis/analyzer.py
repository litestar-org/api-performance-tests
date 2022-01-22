from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

results_dir = Path(".").parent / "results"
df = pd.DataFrame()
for file in results_dir.iterdir():
    if file.suffix == ".json":
        json = pd.read_json(file)
        json["source"] = "fastapi" if "fastapi" in file.name else "starlite"
        df = df.append(json)


# async comparison
df2 = (
    df["url"]
    .str.contains("async-square")
    .groupby("source")
    .agg(requests_processed=("2xx"))
)
df2 = df2.reset_index()
plt.figure(figsize=(30, 10))
plt1 = sns.barplot(x="type", y="requests_processed", hue="source", data=df2)
plt.savefig("analysis/output/async_square_requests.png")

# square sync comparison
squaredf = (
    df["url"]
    .str.contains("sync-square")
    .groupby("source")
    .agg(requests_processed=("2xx"))
)
squaredf = squaredf.reset_index()
plt.figure(figsize=(30, 10))
plt2 = sns.barplot(x="type", y="requests_processed", hue="source", data=squaredf)
plt.savefig("analysis/output/sync_square_requests.png")

# text sync comparison
squaredf = (
    df["url"]
    .str.contains("plaintext")
    .groupby("source")
    .agg(requests_processed=("2xx"))
)
squaredf = squaredf.reset_index()
plt.figure(figsize=(30, 10))
plt2 = sns.barplot(x="type", y="requests_processed", hue="source", data=squaredf)
plt.savefig("analysis/output/sync_plaintext_requests.png")


# text sync comparison
squaredf = (
    df["url"].str.contains("json").groupby("source").agg(requests_processed=("2xx"))
)
squaredf = squaredf.reset_index()
plt.figure(figsize=(30, 10))
plt2 = sns.barplot(x="type", y="requests_processed", hue="source", data=squaredf)
plt.savefig("analysis/output/sync_json_requests.png")

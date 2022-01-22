import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

results_dir = Path(".").parent / "results"

df = pd.DataFrame()
for file in results_dir.iterdir():
    if file.suffix == ".json":
        json = pd.read_json(file)
        json["source"], json["type"] = file.name.split("-", 1)
        json["filename"] = file.name
        json["async"] = "async" in file.name
        df = df.append(json)

# async comparison
df2 = (
    df.loc[df["async"] == True]
    .groupby(["source", "type"])
    .agg(mean_throughput=("throughput", "mean"))
)
df2 = df2.reset_index()
plt.figure(figsize=(30, 10))
plt1 = sns.barplot(x="type", y="mean_throughput", hue="source", data=df2)
# plt1.set_xticklabels(plt1.get_xticklabels(), rotation=45)
plt.savefig("analysis/output/async_comp.png")

# square sync comparison
squaredf = (
    df.loc[(df["async"] == False) & (df["url"].str.contains("square"))]
    .groupby(["source", "type"])
    .agg(mean_throughput=("throughput", "mean"))
)
squaredf = squaredf.reset_index()
plt.figure(figsize=(30, 10))
plt2 = sns.barplot(x="type", y="mean_throughput", hue="source", data=squaredf)
# plt2.set_xticklabels(plt2.get_xticklabels(), rotation=45)
plt.savefig("analysis/output/square_sync_comp.png")

# text sync comparison
df3 = (
    df.loc[(df["async"] == False) & (~df["url"].str.contains("square"))]
    .groupby(["source", "type"])
    .agg(mean_throughput=("throughput", "mean"))
)
df3 = df3.reset_index()
plt.figure(figsize=(30, 10))
plt3 = sns.barplot(x="type", y="mean_throughput", hue="source", data=df3)
# plt3.set_xticklabels(plt3.get_xticklabels(), rotation=45)
plt.savefig("analysis/output/text_sync_comp.png")

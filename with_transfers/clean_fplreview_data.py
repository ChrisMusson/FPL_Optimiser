import pandas as pd
import sys

[in_file, start_gw, end_gw] = sys.argv[1:]

df = pd.read_csv(in_file)
df.rename(columns={x:x.lower() for x in df.columns}, inplace=True)
df.rename(columns={"bv": "buy_cost", "sv": "sale_value"}, inplace=True)
df["id"] = range(1, len(df) + 1)
df.dropna(inplace=True)
cols = [f"{i}_pts" for i in range(int(start_gw), int(end_gw) + 1)]
df = df.loc[:, ["id", "team", "pos", "name", "buy_cost", "sale_value"] + cols]

df.to_csv("cleaned_data.csv", index=False)
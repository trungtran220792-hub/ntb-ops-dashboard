import pandas as pd
import os

csv_path = "ops_gtc.csv"
out = []
if os.path.exists(csv_path):
    out.append("ops_gtc.csv exists!")
    df = pd.read_csv(csv_path)
    out.append(f"df.columns: {list(df.columns)}")
    out.append(f"dtypes:\n{df.dtypes}")
    out.append("Head of Volume and % GTC:")
    out.append(str(df[['Volume', '% GTC']].head(10)))
    out.append("Unique values of Volume:")
    out.append(str(df['Volume'].unique()[:20]))
    out.append("Unique values of % GTC:")
    out.append(str(df['% GTC'].unique()[:20]))
else:
    out.append("ops_gtc.csv does not exist!")

with open("scratch/debug_dataframe_types_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Done writing scratch/debug_dataframe_types_res.txt")

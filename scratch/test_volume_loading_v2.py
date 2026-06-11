import pandas as pd
import os

df = pd.read_csv("c:/Users/lap4all/Desktop/New folder/vols_tao_don.csv")
cols = list(df.columns)
print("CSV Columns loaded:", len(cols))

with open("c:/Users/lap4all/Desktop/New folder/scratch/volume_columns.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(cols))

print("Saved columns to scratch/volume_columns.txt")

import pandas as pd

df = pd.read_csv("tutto-csv.csv")
df.reset_index(drop=True, inplace=True)

df.to_json(r'tutto-json.json',orient='records')
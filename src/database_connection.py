import pandas as pd
from pymongo import MongoClient
from config import MongoDB_URL

# ---------- Read Excel ----------

df = pd.read_excel(
    "../output/large_cap_stocks.xlsx"
)

print("Excel data loaded.")
print(df)


# ---------- Connect MongoDB ----------

client = MongoClient(
    MongoDB_URL
)

db = client["angel_one"]

collection = db["large_cap_stocks"]


# ---------- Convert Excel to dictionaries ----------

data = df.to_dict(
    orient="records"
)
# print(data[0].keys())
# ---------- Insert into MongoDB ----------

if data:
    result = collection.insert_many(data)

    print(
        f"{len(result.inserted_ids)} records inserted."
    )
else:
    print("No data found in Excel.")


# # ---------- Close connection ----------

client.close()
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers-handbook-api")
df = pd.read_csv(ROOT / "output" / "all_years_extracted.csv", dtype=str)

print("\nRows by year:")
print(df.groupby("year").size())

print("\nRows with blank product:")
print(df[df["product"].isna() | (df["product"].str.strip() == "")])

print("\nRows with both pack_10 and pack_20 blank:")
print(df[df["pack_10"].isna() & df["pack_20"].isna()][["year","source_image","manufacturer_or_distributor","product","notes"]].head(50))

print("\nDuplicate manufacturer/product/year rows:")
dupes = df[df.duplicated(["year","manufacturer_or_distributor","product"], keep=False)]
print(dupes[["year","source_image","manufacturer_or_distributor","product","pack_10","pack_20"]].head(100))
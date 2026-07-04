from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers-handbook-api")
INFILE = ROOT / "output" / "all_years_extracted.csv"
OUTDIR = ROOT / "output" / "cleaning_lists"
OUTDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INFILE, dtype=str).fillna("")

for col in ["manufacturer_or_distributor", "product"]:
    df[col] = df[col].str.strip()

# Manufacturer list
manu = (
    df.groupby("manufacturer_or_distributor")
    .agg(
        n_rows=("product", "size"),
        first_year=("year", "min"),
        last_year=("year", "max"),
        n_products=("product", "nunique"),
    )
    .reset_index()
    .sort_values(["manufacturer_or_distributor"])
)

manu["canonical_manufacturer"] = manu["manufacturer_or_distributor"]
manu["notes"] = ""

manu.to_csv(OUTDIR / "manufacturer_master_list.csv", index=False, encoding="utf-8-sig")

# Brand/product list
brands = (
    df.groupby(["manufacturer_or_distributor", "product"])
    .agg(
        n_rows=("year", "size"),
        first_year=("year", "min"),
        last_year=("year", "max"),
        years_observed=("year", lambda x: ", ".join(sorted(set(x)))),
    )
    .reset_index()
    .sort_values(["manufacturer_or_distributor", "product"])
)

brands["canonical_manufacturer"] = brands["manufacturer_or_distributor"]
brands["canonical_product"] = brands["product"]
brands["notes"] = ""

brands.to_csv(OUTDIR / "brand_master_list.csv", index=False, encoding="utf-8-sig")

print("Saved:")
print(OUTDIR / "manufacturer_master_list.csv")
print(OUTDIR / "brand_master_list.csv")
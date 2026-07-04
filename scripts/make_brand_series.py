from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers-handbook-api")
INFILE = ROOT / "output" / "all_years_extracted.csv"
OUTDIR = ROOT / "output"

df = pd.read_csv(INFILE, dtype=str)

# clean text
for col in ["manufacturer_or_distributor", "product", "pack_10", "pack_20", "notes"]:
    df[col] = df[col].fillna("").str.strip()

# create stable brand key
df["brand_key"] = (
    df["manufacturer_or_distributor"].str.upper()
    + " | "
    + df["product"].str.upper()
)

# long file, useful for analysis
long = df[
    [
        "year",
        "source_image",
        "manufacturer_or_distributor",
        "product",
        "pack_10",
        "pack_20",
        "notes",
        "brand_key",
    ]
].copy()

long.to_csv(OUTDIR / "all_years_long_clean_start.csv", index=False, encoding="utf-8-sig")

# wide format: one row per manufacturer/product, year-pack columns
wide10 = long.pivot_table(
    index=["manufacturer_or_distributor", "product", "brand_key"],
    columns="year",
    values="pack_10",
    aggfunc=lambda x: " | ".join(sorted(set(v for v in x if v))),
)

wide20 = long.pivot_table(
    index=["manufacturer_or_distributor", "product", "brand_key"],
    columns="year",
    values="pack_20",
    aggfunc=lambda x: " | ".join(sorted(set(v for v in x if v))),
)

wide10.columns = [f"{c}_10" for c in wide10.columns]
wide20.columns = [f"{c}_20" for c in wide20.columns]

wide = pd.concat([wide10, wide20], axis=1).reset_index()

# reorder columns by year: 1951_10, 1951_20, 1952_10, 1952_20...
years = sorted(df["year"].dropna().unique())
ordered_cols = ["manufacturer_or_distributor", "product", "brand_key"]
for y in years:
    for pack in ["10", "20"]:
        col = f"{y}_{pack}"
        if col in wide.columns:
            ordered_cols.append(col)

wide = wide[ordered_cols]

wide.to_csv(OUTDIR / "brand_price_series_wide.csv", index=False, encoding="utf-8-sig")

print("Saved:")
print(OUTDIR / "all_years_long_clean_start.csv")
print(OUTDIR / "brand_price_series_wide.csv")
print(f"Rows in wide file: {len(wide)}")
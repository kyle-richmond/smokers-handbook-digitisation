from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers-handbook-api")
OUT = ROOT / "output"

files = sorted(OUT.glob("*_extracted.csv"))

dfs = []
for f in files:
    df = pd.read_csv(f, dtype=str)
    df["source_file"] = f.name
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

combined.to_csv(OUT / "all_years_extracted.csv", index=False, encoding="utf-8-sig")

print(f"Combined {len(files)} files")
print(f"Rows: {len(combined)}")
print(f"Saved: {OUT / 'all_years_extracted.csv'}")
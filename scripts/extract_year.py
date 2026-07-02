import base64
import json
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()
client = OpenAI()

ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers-handbook-api")
IMAGE_ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers_handbook_resized")

YEAR = "1955"
IMAGE_DIR = IMAGE_ROOT / YEAR / "relevant"

PROMPT = (ROOT / "prompts" / "cigarette_prices.md").read_text(encoding="utf-8")

OUT_JSON = ROOT / "output" / YEAR / "json"
OUT_JSON.mkdir(parents=True, exist_ok=True)

rows = []

for image_path in tqdm(sorted(IMAGE_DIR.glob("*.jpg"))):
    out_file = OUT_JSON / f"{image_path.stem}.json"

    if out_file.exists():
        data = json.loads(out_file.read_text(encoding="utf-8"))
    else:
        image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")

        response = client.responses.create(
            model="gpt-5.5",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": PROMPT},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{image_b64}",
                        },
                    ],
                }
            ],
        )

        data = json.loads(response.output_text)
        out_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    for r in data:
        r["year"] = YEAR
        r["source_image"] = image_path.name
        rows.append(r)

df = pd.DataFrame(rows)

df = df[
    [
        "year",
        "source_image",
        "manufacturer_or_distributor",
        "product",
        "pack_10",
        "pack_20",
        "notes",
    ]
]

out_csv = ROOT / "output" / f"{YEAR}_extracted.csv"
df.to_csv(out_csv, index=False, encoding="utf-8-sig")

print(f"Saved: {out_csv}")
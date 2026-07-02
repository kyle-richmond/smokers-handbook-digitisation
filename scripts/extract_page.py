import base64
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers-handbook-api")
IMAGE = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers_handbook\1951\relevant\1951_p009.jpg")

PROMPT = (ROOT / "prompts" / "cigarette_prices.md").read_text(encoding="utf-8")
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

image_b64 = base64.b64encode(IMAGE.read_bytes()).decode("utf-8")

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

text = response.output_text
data = json.loads(text)

out_file = OUT / f"{IMAGE.stem}.json"
out_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Saved: {out_file}")
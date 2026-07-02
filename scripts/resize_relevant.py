from pathlib import Path
from PIL import Image, ImageOps

IMAGE_ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers_handbook")
OUT_ROOT = Path(r"C:\Users\3059313\Documents\Tobacco Business History Submission\Prices\smokers_handbook_resized")

MAX_SIDE = 1600

for year_dir in sorted(IMAGE_ROOT.iterdir()):
    relevant = year_dir / "relevant"
    if not relevant.exists():
        continue

    out_dir = OUT_ROOT / year_dir.name / "relevant"
    out_dir.mkdir(parents=True, exist_ok=True)

    for img_path in sorted(relevant.glob("*.jpg")):
        out_path = out_dir / img_path.name
        if out_path.exists():
            continue

        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        img.thumbnail((MAX_SIDE, MAX_SIDE))
        img.save(out_path, "JPEG", quality=85, optimize=True)

print("Done")
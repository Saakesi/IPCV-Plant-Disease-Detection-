
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "plantdoc_yolo"

SPLITS = {
    "train": ROOT / "annotations/plant_diseases_instances_train.json",
    "val": ROOT / "annotations/plant_diseases_instances_val.json",
    "test": ROOT / "annotations/plant_diseases_instances_test.json",
}

# Build a consistent class-ID mapping across all splits.
first = json.loads(SPLITS["train"].read_text())
categories = sorted(first["categories"], key=lambda c: c["id"])
class_map = {c["id"]: i for i, c in enumerate(categories)}

for split, json_path in SPLITS.items():
    data = json.loads(json_path.read_text())
    images_out = OUTPUT / "images" / split
    labels_out = OUTPUT / "labels" / split
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    annotations = {}
    for ann in data["annotations"]:
        annotations.setdefault(ann["image_id"], []).append(ann)

    converted = 0
    missing = 0

    for image in data["images"]:
        # COCO filenames are relative to the repository root.
        source = ROOT / image["file_name"]

        if not source.exists():
            # Also try a filename relative to plant_diseases/images.
            source = ROOT / "plant_diseases/images" / Path(
                image["file_name"]
            ).name

        if not source.exists():
            print("Missing image:", image["file_name"])
            missing += 1
            continue

        image_id = image["id"]
        image_name = f"{image_id}{source.suffix.lower()}"
        target = images_out / image_name

        if not target.exists():
            try:
                target.symlink_to(source.resolve())
            except OSError:
                shutil.copy2(source, target)

        lines = []
        width = image["width"]
        height = image["height"]

        for ann in annotations.get(image_id, []):
            category_id = ann["category_id"]
            if category_id not in class_map:
                continue

            x, y, w, h = ann["bbox"]

            # COCO xywh -> YOLO normalized center-x, center-y, width, height
            cx = (x + w / 2) / width
            cy = (y + h / 2) / height
            nw = w / width
            nh = h / height

            if w <= 0 or h <= 0:
                continue

            lines.append(
                f"{class_map[category_id]} "
                f"{cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}"
            )

        (labels_out / f"{image_id}.txt").write_text(
            "\n".join(lines) + ("\n" if lines else "")
        )
        converted += 1

    print(f"{split}: converted={converted}, missing={missing}")

# Create the Ultralytics dataset configuration.
names = [c["name"] for c in categories]
yaml = [
    f"path: {OUTPUT.as_posix()}",
    "train: images/train",
    "val: images/val",
    "test: images/test",
    f"nc: {len(names)}",
    "names:",
]
yaml.extend(f"  {i}: {json.dumps(name)}" for i, name in enumerate(names))
(OUTPUT / "data.yaml").write_text("\n".join(yaml) + "\n")

print("Dataset configuration:", OUTPUT / "data.yaml")
print("Classes:", len(names))

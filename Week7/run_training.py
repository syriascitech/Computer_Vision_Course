"""
Week 7 - YOLO Emergency Vehicle Training Script
Run this script from the project root after activating the venv.
"""

import os
import random
import shutil
from pathlib import Path

os.environ["YOLO_VERBOSE"] = "False"

import torch
from ultralytics import YOLO, settings
import pandas as pd
import yaml

settings.update({"sync": False})

# ── paths ──────────────────────────────────────────────────────────────────
PRETRAINED_PATH = "models/yolo11n.pt"
DATA_YAML       = "dataset/data.yaml"

# ── device (MPS on Apple Silicon, else CPU) ─────────────────────────────────
if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = 0
else:
    DEVICE = "cpu"

print(f"PyTorch  : {torch.__version__}")
print(f"Device   : {DEVICE}")
print(f"CPU cores: {os.cpu_count()}")

# ── load class names ────────────────────────────────────────────────────────
with open(DATA_YAML) as f:
    CLASS_NAMES = yaml.safe_load(f)["names"]
print(f"Classes  : {CLASS_NAMES}")

# ── build mini dataset ──────────────────────────────────────────────────────
MINI_TRAIN_IMAGES = 100
MINI_BATCH        = 8
MINI_EPOCHS       = 5
MINI_ROOT         = Path("dataset_mini")

random.seed(7)

if MINI_ROOT.exists():
    shutil.rmtree(MINI_ROOT)

for split, n_images in [("train", MINI_TRAIN_IMAGES), ("valid", 30)]:
    src_images = sorted((Path("dataset") / split / "images").glob("*.jpg"))
    chosen     = random.sample(src_images, min(n_images, len(src_images)))

    (MINI_ROOT / split / "images").mkdir(parents=True, exist_ok=True)
    (MINI_ROOT / split / "labels").mkdir(parents=True, exist_ok=True)

    for img_path in chosen:
        lbl_path = Path("dataset") / split / "labels" / (img_path.stem + ".txt")
        shutil.copy2(img_path, MINI_ROOT / split / "images" / img_path.name)
        shutil.copy2(lbl_path, MINI_ROOT / split / "labels" / lbl_path.name)

    print(f"  {split}: copied {len(chosen)} images")

# No 'path' key — Ultralytics uses the yaml file's own directory as root.
(MINI_ROOT / "data.yaml").write_text(
    "train: train/images\n"
    "val: valid/images\n\n"
    f"nc: {len(CLASS_NAMES)}\n"
    f"names: {CLASS_NAMES}\n"
)
print(f"Mini data.yaml: {MINI_ROOT / 'data.yaml'}")

# ── train mini model ────────────────────────────────────────────────────────
print("\n=== Starting mini training ===")
mini_model = YOLO(PRETRAINED_PATH)

mini_results = mini_model.train(
    data    = str(MINI_ROOT / "data.yaml"),
    epochs  = MINI_EPOCHS,
    imgsz   = 320,
    batch   = MINI_BATCH,
    device  = DEVICE,
    workers = 0,        # 0 is required on macOS
    amp     = False,    # AMP not stable on MPS/CPU
    cache   = False,
    plots   = True,
    name    = "mini",
    exist_ok= True,
    seed    = 7,
)

MINI_RUN_DIR = Path(mini_model.trainer.save_dir)
print(f"\nMini training done. Results in: {MINI_RUN_DIR}")

# ── print final metrics ─────────────────────────────────────────────────────
history = pd.read_csv(MINI_RUN_DIR / "results.csv")
history.columns = [c.strip() for c in history.columns]
final = history.iloc[-1]

print(f"\n--- Mini run final metrics ---")
print(f"  mAP@50     : {final['metrics/mAP50(B)']:.3f}")
print(f"  mAP@50-95  : {final['metrics/mAP50-95(B)']:.3f}")
print(f"  Precision  : {final['metrics/precision(B)']:.3f}")
print(f"  Recall     : {final['metrics/recall(B)']:.3f}")

# Week 7 — YOLO Training & Fine-Tuning: Step-by-Step Guide

**Machine:** Apple Mac Air M1 (8-core CPU, Apple GPU via MPS)  
**Python:** 3.11.9  
**PyTorch:** 2.14.0 (with MPS / Metal Performance Shaders support)  
**Ultralytics:** 8.4.148  
**Task:** Fine-tune YOLO11n to detect emergency vehicles (ambulance, car, truck, bus)

---

## Overview

This week's project fine-tunes a pretrained YOLO11n model on a custom dataset of emergency vehicles sourced from Google Open Images V6/V7. The dataset has four classes: **ambulance, car, truck, bus**.

| Split | Images |
|-------|--------|
| train | 477    |
| valid | 136    |
| test  | 69     |

---

## Step 1 — Verify the Project Structure

Make sure the following layout exists before starting:

```
Week7 v2/
├── dataset/
│   ├── data.yaml          # dataset config (classes, paths)
│   ├── train/
│   │   ├── images/        # 477 .jpg files
│   │   └── labels/        # matching .txt YOLO labels
│   ├── valid/
│   │   ├── images/        # 136 .jpg files
│   │   └── labels/
│   └── test/
│       ├── images/        # 69 .jpg files
│       └── labels/
├── models/
│   └── yolo11n.pt         # pretrained weights (COCO, 80 classes)
├── failures/
│   ├── failures.csv
│   └── f1_*.jpg … f5_*.jpg
├── requirements.txt
└── week_7_training_and_finetuning.ipynb
```

---

## Step 2 — Create a Python Virtual Environment

Open a terminal, navigate to the project folder, then run:

```bash
cd "/Users/amersaw/Downloads/Week7 v2"

# Create the venv (only needed once)
python3 -m venv venv

# Activate it (do this every time you open a new terminal)
source venv/bin/activate
```

Your prompt should show `(venv)` after activation.

> **Why a venv?** It isolates the project's packages from your system Python, preventing version conflicts.

---

## Step 3 — Install Dependencies

With the venv activated, install all required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt jupyter
```

**What gets installed:**

| Package | Purpose |
|---------|---------|
| `ultralytics>=8.3` | YOLO training & inference framework |
| `torch>=2.0` | Deep learning engine (uses MPS on M1) |
| `torchvision` | Image transforms used by YOLO |
| `opencv-python` | Image reading and visualisation |
| `pandas` | Reading training logs (results.csv) |
| `matplotlib` | Plotting loss curves, predictions |
| `pyyaml` | Parsing data.yaml |
| `ipython` | Better REPL output in notebooks |
| `jupyter` | Run the `.ipynb` notebook interactively |

> **M1 note:** PyTorch 2.0+ ships with native MPS support. No special installation step needed — MPS is automatically detected.

---

## Step 4 — Verify the Installation

```bash
python -c "
import ultralytics, torch, cv2
print('ultralytics:', ultralytics.__version__)
print('torch       :', torch.__version__)
print('MPS available:', torch.backends.mps.is_available())
print('CUDA available:', torch.cuda.is_available())
"
```

Expected output on M1:
```
ultralytics: 8.4.x
torch       : 2.14.x
MPS available: True
CUDA available: False
```

---

## Step 5 — Understand the Data Format (YOLO Labels)

Each image has a paired `.txt` label file. Every line in the label file describes one bounding box:

```
<class_id>  <x_center>  <y_center>  <width>  <height>
```

All five values are **normalised** to the range `[0, 1]` (divided by image width/height).

**Class IDs for this project:**

| ID | Class |
|----|-------|
| 0  | ambulance |
| 1  | car |
| 2  | truck |
| 3  | bus |

**Example label line:**
```
0 0.512345 0.487654 0.234567 0.198765
```
This means: ambulance, centred at (51.2%, 48.8%) of the image, 23.5% wide, 19.9% tall.

**Converting pixel coordinates → YOLO format:**
```python
x_norm  = x_center_px / image_width
y_norm  = y_center_px / image_height
w_norm  = box_width_px / image_width
h_norm  = box_height_px / image_height
```

---

## Step 6 — Understand `dataset/data.yaml`

```yaml
path: .                       # root of the dataset (relative to where you run training)
train: train/images
val:   valid/images
test:  test/images

nc: 4                         # number of classes
names: ["ambulance", "car", "truck", "bus"]
```

This file tells YOLO where to find images and what classes exist.

---

## Step 7 — Choose Your Device

YOLO automatically picks the best available device. On M1 Macs:

```python
import torch

if torch.backends.mps.is_available():
    DEVICE = "mps"   # Apple Silicon GPU — fastest on M1
elif torch.cuda.is_available():
    DEVICE = 0       # NVIDIA GPU (not present on M1)
else:
    DEVICE = "cpu"   # Fallback
```

> `"mps"` gives ~2–5× speedup over CPU for YOLO training on M1 Air.

---

## Step 8 — Build the Mini Dataset

For the in-class exercise, a mini subset is used (100 train + 30 val images) to keep training under 10 minutes:

```python
import random, shutil
from pathlib import Path

random.seed(7)
MINI_ROOT = Path("dataset_mini")

for split, n in [("train", 100), ("valid", 30)]:
    src_imgs = sorted((Path("dataset") / split / "images").glob("*.jpg"))
    chosen   = random.sample(src_imgs, min(n, len(src_imgs)))

    (MINI_ROOT / split / "images").mkdir(parents=True, exist_ok=True)
    (MINI_ROOT / split / "labels").mkdir(parents=True, exist_ok=True)

    for img_path in chosen:
        lbl_path = Path("dataset") / split / "labels" / (img_path.stem + ".txt")
        shutil.copy2(img_path, MINI_ROOT / split / "images" / img_path.name)
        shutil.copy2(lbl_path, MINI_ROOT / split / "labels" / lbl_path.name)

# Write mini data.yaml with absolute path (required by ultralytics)
CLASS_NAMES = ["ambulance", "car", "truck", "bus"]
(MINI_ROOT / "data.yaml").write_text(
    f"path: {MINI_ROOT.resolve()}\n"
    "train: train/images\nval: valid/images\n\n"
    f"nc: 4\nnames: {CLASS_NAMES}\n"
)
```

> **Important:** The mini `data.yaml` uses an **absolute path** (`MINI_ROOT.resolve()`). This is required because Ultralytics resolves paths relative to the yaml file location.

---

## Step 9 — Run Mini Training (5 epochs, 320 px)

This is the main in-class training run. It completes in ~15 minutes on M1 Air.

```python
from ultralytics import YOLO

mini_model = YOLO("models/yolo11n.pt")   # load COCO pretrained weights

mini_results = mini_model.train(
    data    = "dataset_mini/data.yaml",
    epochs  = 5,          # number of full passes over the training set
    imgsz   = 320,        # resize images to 320×320 (smaller = faster)
    batch   = 8,          # images per gradient update
    device  = "mps",      # Apple Silicon GPU
    workers = 0,          # must be 0 on macOS (multiprocessing limitation)
    amp     = False,      # mixed-precision OFF (not stable on MPS)
    cache   = False,      # don't cache images to RAM
    plots   = True,       # save loss curves, confusion matrix, etc.
    name    = "mini",     # results saved under runs/detect/mini/
    exist_ok= True,       # overwrite previous mini run if it exists
    seed    = 7,          # reproducibility
)
```

**Key parameters explained:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `epochs` | 5 | Quick demo run; full training uses 60 |
| `imgsz` | 320 | Smaller images = faster; full training uses 640 |
| `batch` | 8 | Number of images processed together |
| `workers` | 0 | Required on macOS — avoids multiprocessing fork issues |
| `amp` | False | MPS doesn't support stable AMP yet; set True on NVIDIA |
| `plots` | True | Generates confusion matrix, PR curves, loss charts |

---

## Step 10 — Read Training Output

After training, results are saved to `runs/detect/mini/`:

```
runs/detect/mini/
├── weights/
│   ├── best.pt                      # best checkpoint (highest val mAP)
│   └── last.pt                      # last epoch checkpoint
├── results.csv                      # epoch-by-epoch metrics
├── results.png                      # loss + mAP curves plot
├── confusion_matrix.png             # raw confusion matrix
├── confusion_matrix_normalized.png  # normalised confusion matrix
├── BoxP_curve.png                   # Precision vs confidence
├── BoxR_curve.png                   # Recall vs confidence
├── BoxPR_curve.png                  # Precision-Recall curve
├── BoxF1_curve.png                  # F1 vs confidence
├── train_batch0.jpg                 # sample augmented training batch
├── val_batch0_labels.jpg            # ground truth on val batch
└── val_batch0_pred.jpg              # model predictions on val batch
```

**Reading the training log:**

```python
import pandas as pd

history = pd.read_csv("runs/detect/mini/results.csv")
history.columns = [c.strip() for c in history.columns]
print(history[["epoch", "metrics/mAP50(B)", "metrics/mAP50-95(B)",
               "train/box_loss", "val/box_loss"]].to_string(index=False))
```

**Actual results from this run:**

| Epoch | mAP@50 | mAP@50-95 | Train box_loss | Val box_loss |
|-------|--------|-----------|----------------|--------------|
| 1     | 0.103  | 0.082     | 0.973          | 0.938        |
| 2     | 0.150  | 0.121     | 0.991          | 0.965        |
| 3     | 0.198  | 0.154     | 1.006          | 1.059        |
| 4     | 0.198  | 0.159     | 1.036          | 1.052        |
| 5     | 0.201  | 0.175     | 1.008          | 1.040        |

> **Interpretation:** mAP@50 rising from 0.10 → 0.20 in 5 epochs shows the model is learning. Low absolute values are expected for such a short run. Full training (60 epochs, 640 px) typically reaches mAP@50 ≈ 0.70–0.80 on this dataset.

---

## Step 11 — Understanding the Metrics

### mAP@50 (main metric)
Mean Average Precision at IoU threshold 0.50. A prediction counts as correct if the predicted box overlaps the ground-truth box by at least 50%. Higher = better.

### mAP@50-95
Average of mAP computed at IoU thresholds 0.50, 0.55, 0.60, …, 0.95. Stricter — requires tighter boxes.

### Precision
Of all boxes the model predicted, what fraction were actually correct?  
`Precision = TP / (TP + FP)`

### Recall
Of all real objects in the images, what fraction did the model find?  
`Recall = TP / (TP + FN)`

### box_loss (localisation loss)
How far off are the predicted box coordinates from the ground truth. Should decrease during training.

### cls_loss (classification loss)
How confident and correct are the class predictions. Should decrease during training.

---

## Step 12 — Run the Notebook Interactively (Optional)

The notebook walks through every concept visually. To open it:

```bash
cd "/Users/amersaw/Downloads/Week7 v2"
source venv/bin/activate
jupyter notebook week_7_training_and_finetuning.ipynb
```

Then run cells in order. The notebook will:
1. Check all imports are installed
2. Load the pretrained YOLO11n model
3. Run it on the `failures/` images to show what it gets wrong
4. Explain YOLO label format with an interactive example
5. Visualise the dataset distribution and annotations
6. Show data augmentation examples
7. Build the mini dataset and run training (**Step 9 above**)
8. Plot loss curves and metrics
9. Compare pretrained vs fine-tuned on the failure images
10. Evaluate the reference fine-tuned model on the test set

---

## Step 13 — Run Training from the Command Line (Alternative)

A standalone script `run_training.py` is included in the project root. It does everything Steps 8–10 do, without needing Jupyter:

```bash
cd "/Users/amersaw/Downloads/Week7 v2"
source venv/bin/activate
python run_training.py
```

---

## Step 14 — Full Training (Optional, ~1–2 hours on M1)

The notebook includes a full training run (60 epochs, 640 px) disabled by default. To enable it, set `RUN_FULL_TRAINING = True` in Cell 18 of the notebook, or add this to `run_training.py`:

```python
full_model = YOLO("models/yolo11n.pt")
full_model.train(
    data    = "dataset/data.yaml",   # full dataset, 477 images
    epochs  = 60,
    imgsz   = 640,
    batch   = 16,
    device  = "mps",
    workers = 0,
    amp     = False,
    patience= 15,    # early stop if val mAP doesn't improve for 15 epochs
    plots   = True,
    name    = "emergency_full",
    seed    = 7,
)
```

Results are saved to `runs/detect/emergency_full/`.

---

## Step 15 — Use the Trained Model for Inference

```python
from ultralytics import YOLO

# Load the best checkpoint from the mini run
model = YOLO("runs/detect/mini/weights/best.pt")

# Run on a single image
results = model.predict(
    source="failures/f1_4815c8b2.jpg",
    conf=0.35,      # minimum confidence threshold
    device="mps",
)

# Show result
import cv2, matplotlib.pyplot as plt
img = cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB)
plt.imshow(img); plt.axis("off"); plt.show()
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'ultralytics'` | Activate the venv: `source venv/bin/activate` |
| `workers` error / DataLoader crash on macOS | Set `workers=0` in `train()` |
| Training slower than expected | Make sure `device="mps"`, not `"cpu"` |
| `amp=True` causes NaN losses on M1 | Set `amp=False` |
| Notebook kernel dies mid-training | Reduce `batch` to 4 or `imgsz` to 224 |
| `FileNotFoundError` on data.yaml | Use absolute path in mini data.yaml (done automatically in the script) |
| `runs_reference/emergency_full` is empty | That folder contains a pre-run reference result for the notebook's Section 6. Run the full training (Step 14) to populate it. |

---

## Quick-Start Cheat Sheet

```bash
# 1. Navigate to project
cd "/Users/amersaw/Downloads/Week7 v2"

# 2. Create and activate venv (first time only)
python3 -m venv venv
source venv/bin/activate

# 3. Install packages (first time only)
pip install --upgrade pip
pip install -r requirements.txt jupyter

# 4. Run training
python run_training.py

# 5. Check results
ls runs/detect/mini/
cat runs/detect/mini/results.csv

# 6. Open notebook (optional)
jupyter notebook week_7_training_and_finetuning.ipynb
```

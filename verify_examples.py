# File: verify_examples.py

import os
import sys
import numpy as np
from PIL import Image

# ─── Allow importing from srcs/ ───────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR      = os.path.join(PROJECT_ROOT, "srcs")
sys.path.insert(0, SRC_DIR)

from main import process_one_case
from image_utils import load_binary_image_to_array, save_array_to_image
from wormhole_parser import parse_wormholes_from_color_map
from game_of_life import GameOfLifeWormhole

DATA_DIR      = os.path.join(PROJECT_ROOT, "data")
OUTPUT_EX_DIR = os.path.join(PROJECT_ROOT, "output_examples")
CHECKPOINTS   = [1, 10, 100, 1000]
EX_PREFIX     = "example-"

def compare_grids(A: np.ndarray, B: np.ndarray):
    if A.shape != B.shape:
        return None, f"Shape mismatch: {A.shape} vs {B.shape}"
    diff = (A != B)
    mismatches = int(np.count_nonzero(diff))
    return (mismatches, A.size), None

os.makedirs(OUTPUT_EX_DIR, exist_ok=True)
example_folders = sorted(
    name for name in os.listdir(DATA_DIR)
    if os.path.isdir(os.path.join(DATA_DIR, name)) and name.startswith(EX_PREFIX)
)
if not example_folders:
    print("❌ No example-* folders found under data/")
    sys.exit(1)

all_good = True
for ex in example_folders:
    ex_data   = os.path.join(DATA_DIR, ex)
    ex_out    = os.path.join(OUTPUT_EX_DIR, ex)
    os.makedirs(ex_out, exist_ok=True)
    print(f"\n── Verifying {ex} ──────────────────────────────────")

    # 1) Simulate example-*
    try:
        process_one_case(ex, DATA_DIR, OUTPUT_EX_DIR)
    except Exception as e:
        print(f"  [ERROR] Simulation failed for {ex}: {e}")
        all_good = False
        continue

    # 2) Compare each checkpoint
    for cp in CHECKPOINTS:
        exp_path = os.path.join(ex_data, f"expected-{cp}.png")
        gen_path = os.path.join(ex_out,   f"{cp}.png")
        if not os.path.isfile(exp_path):
            print(f"  ● {ex}: missing expected-{cp}.png, skipping")
            all_good = False
            continue
        if not os.path.isfile(gen_path):
            print(f"  ● {ex}: missing generated {cp}.png, skipping")
            all_good = False
            continue

        # Load both as boolean grids
        exp_grid = load_binary_image_to_array(exp_path)
        gen_grid = load_binary_image_to_array(gen_path)
        (mism, total), err = compare_grids(exp_grid, gen_grid)
        if err:
            print(f"  ✘ {ex} cp={cp}: {err}")
            all_good = False
        else:
            if mism == 0:
                print(f"  ✔ {ex} cp={cp}.png: EXACT MATCH (0 / {total} pixels)")
            else:
                pct = (mism / total) * 100
                print(f"  ✘ {ex} cp={cp}.png: {mism} mismatches / {total} ({pct:.4f}%)")
                # Optionally write out a diff for visual debugging:
                diff = (exp_grid != gen_grid)
                diff_path = os.path.join(ex_out, f"diff-{cp}.png")
                save_array_to_image(diff, diff_path)
                print(f"      → wrote diff to {diff_path}")
                all_good = False

print("\n────────────────────────────────────────────────")
if all_good:
    print("🎉 All example-* outputs matched perfectly!")
else:
    print("⚠ Some example-* cases did NOT match. See details above.")
print("────────────────────────────────────────────────\n")

# File: srcs/main.py

import os
import sys
from image_utils import (
    load_binary_image_to_array,
    save_array_to_image,
    load_color_image
)
from wormhole_parser import parse_wormholes_from_color_map
from game_of_life import GameOfLifeWormhole

def process_one_case(case_name, data_dir, output_base_dir):
    """
    Process a single folder under data/ named `case_name`.
    Expects:
      - data/<case_name>/starting_position.png
      - data/<case_name>/horizontal_tunnel.png
      - data/<case_name>/vertical_tunnel.png

    Saves:
      output_base_dir/<case_name>/1.png
      output_base_dir/<case_name>/10.png
      output_base_dir/<case_name>/100.png
      output_base_dir/<case_name>/1000.png
    """
    start_path    = os.path.join(data_dir, case_name, "starting_position.png")
    h_tunnel_path = os.path.join(data_dir, case_name, "horizontal_tunnel.png")
    v_tunnel_path = os.path.join(data_dir, case_name, "vertical_tunnel.png")

    missing = [p for p in (start_path, h_tunnel_path, v_tunnel_path) if not os.path.isfile(p)]
    if missing:
        raise FileNotFoundError(f"Folder '{case_name}' is missing required files:\n  " + "\n  ".join(missing))

    out_dir = os.path.join(output_base_dir, case_name)
    os.makedirs(out_dir, exist_ok=True)

    # 1) Load the starting grid
    grid = load_binary_image_to_array(start_path)

    # 2) Load tunnel images and parse wormholes
    h_arr = load_color_image(h_tunnel_path)
    v_arr = load_color_image(v_tunnel_path)
    h_wormholes = parse_wormholes_from_color_map(h_arr)
    v_wormholes = parse_wormholes_from_color_map(v_arr)

    # 3) Initialize simulator
    gol = GameOfLifeWormhole(grid, h_wormholes, v_wormholes)

    # 4) Checkpoints: 1, 10, 100, 1000
    checkpoints = [1, 10, 100, 1000]
    prev_iter = 0
    for it in checkpoints:
        steps = it - prev_iter
        gol.simulate(steps)
        prev_iter = it

        out_path = os.path.join(out_dir, f"{it}.png")
        save_array_to_image(gol.grid, out_path)
        print(f"[{case_name}] → Saved iteration {it} at: {out_path}")

def main():
    base_dir   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir   = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "output")

    if not os.path.isdir(data_dir):
        print(f"ERROR: Could not find data/ folder at:\n  {data_dir}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Only run problem-*; skip example-* in normal runs
    for entry in sorted(os.listdir(data_dir)):
        entry_path = os.path.join(data_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        if not entry.startswith("problem-"):
            continue

        try:
            process_one_case(entry, data_dir, output_dir)
        except FileNotFoundError as err:
            print(f"Skipping '{entry}': {err}")

    print("✅ Done processing all problem-* cases.")

if __name__ == "__main__":
    main()

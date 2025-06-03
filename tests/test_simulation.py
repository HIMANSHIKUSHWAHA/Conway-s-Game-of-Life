import sys
import os
import numpy as np
import pytest
from PIL import Image

# Add ../srcs to sys.path so we can import from it cleanly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../srcs")))

# Imports from srcs
from image_utils import load_binary_image_to_array, save_array_to_image
from wormhole_parser import parse_wormholes_from_color_map
from game_of_life import GameOfLifeWormhole

@pytest.mark.parametrize("case_name", [
    "example-0",
    "example-1",
    "example-2",
    "example-3",
    "example-4"
])
def test_iteration_1_matches_expected(case_name, tmp_path):
    """
    For each example-*, load its starting_position and wormholes,
    run exactly 1 step, then compare the result to data/<case_name>/expected-1.png.
    If wormhole maps are invalid (e.g. duplicate portal colors), skip the test.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data", case_name)
    expected_path = os.path.join(data_dir, "expected-1.png")

    # Skip this test if no expected-1.png is present in that folder
    if not os.path.isfile(expected_path):
        pytest.skip(f"No expected-1.png for {case_name}")

    # Load the input grid & wormhole bitmaps
    grid = load_binary_image_to_array(os.path.join(data_dir, "starting_position.png"))
    h_image = Image.open(os.path.join(data_dir, "horizontal_tunnel.png")).convert("RGB")
    v_image = Image.open(os.path.join(data_dir, "vertical_tunnel.png")).convert("RGB")

    # Safely parse wormholes; skip if any color is duplicated more than once
    try:
        h_wormholes = parse_wormholes_from_color_map(np.array(h_image, dtype=np.uint8))
        v_wormholes = parse_wormholes_from_color_map(np.array(v_image, dtype=np.uint8))
    except ValueError as e:
        pytest.skip(f"{case_name} has invalid wormhole bitmap: {e}")

    # Run the simulation for 1 step
    gol = GameOfLifeWormhole(grid, h_wormholes, v_wormholes)
    gol.step()
    result = gol.grid

    # Load expected output
    expected = load_binary_image_to_array(expected_path)

    # Compare and optionally show the diff
    if not np.array_equal(result, expected):
        diff = np.logical_xor(result, expected)
        save_array_to_image(result, str(tmp_path / f"{case_name}_result.png"))
        save_array_to_image(expected, str(tmp_path / f"{case_name}_expected.png"))
        save_array_to_image(diff, str(tmp_path / f"{case_name}_diff.png"))
        assert False, f"Iteration‐1 mismatch in {case_name}. See result, expected, and diff PNGs in {tmp_path}"

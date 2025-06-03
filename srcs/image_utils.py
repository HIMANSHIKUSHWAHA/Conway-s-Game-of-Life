# File: srcs/image_utils.py

from PIL import Image
import numpy as np

def load_binary_image_to_array(path):
    """
    Load a black/white PNG from `path` and return a 2D boolean numpy array:
      True  = white pixel (alive)
      False = black pixel (dead)
    """
    img = Image.open(path).convert("L")  # grayscale
    arr = np.array(img, dtype=np.uint8)
    # We treat any non-zero (255=white) as True, 0 as False
    return arr > 0

def save_array_to_image(arr, path):
    """
    Given a 2D boolean numpy array `arr`, write a black/white PNG to `path`.
    True → white (255), False → black (0).
    """
    # Convert boolean to uint8 (0 or 255)
    img_arr = (arr.astype(np.uint8)) * 255
    img = Image.fromarray(img_arr, mode="L")
    img.save(path)

def load_color_image(path):
    """
    Load an RGB (color) PNG from `path` and return a numpy array of shape (H, W, 3), dtype=uint8.
    Used for wormhole parsing.
    """
    img = Image.open(path).convert("RGB")
    return np.array(img, dtype=np.uint8)

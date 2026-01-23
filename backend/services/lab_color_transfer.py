# backend/services/lab_color_transfer.py

import cv2
import numpy as np


def _image_to_lab_stats(image_path: str):
    """
    Convert image to LAB and compute mean & std per channel
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    img = img.astype(np.float32)

    l, a, b = cv2.split(img)

    stats = {
        "l_mean": np.mean(l),
        "l_std": np.std(l),
        "a_mean": np.mean(a),
        "a_std": np.std(a),
        "b_mean": np.mean(b),
        "b_std": np.std(b),
    }
    return stats


def lab_color_transfer(input_image: str, reference_image: str) -> dict:
    """
    Compute LAB-based color deltas and convert to Lightroom-safe parameters
    """

    src = _image_to_lab_stats(input_image)
    ref = _image_to_lab_stats(reference_image)

    # -------------------------
    # LUMINANCE (Exposure / Contrast)
    # -------------------------
    l_mean_diff = ref["l_mean"] - src["l_mean"]
    l_std_ratio = ref["l_std"] / max(src["l_std"], 1e-5)

    exposure = np.clip(l_mean_diff / 20.0, -1.0, 1.0)
    contrast = np.clip((l_std_ratio - 1.0) * 40, -20, 20)

    # -------------------------
    # COLOR BALANCE (WB + Tint)
    # -------------------------
    a_diff = ref["a_mean"] - src["a_mean"]   # green ↔ magenta
    b_diff = ref["b_mean"] - src["b_mean"]   # blue ↔ yellow

    temperature = np.clip(b_diff * 0.6, -20, 20)
    tint = np.clip(a_diff * 0.6, -20, 20)

    # -------------------------
    # SATURATION CONTROL
    # -------------------------
    chroma_src = (src["a_std"] + src["b_std"]) / 2
    chroma_ref = (ref["a_std"] + ref["b_std"]) / 2

    saturation = np.clip((chroma_ref - chroma_src) * 0.5, -15, 15)
    vibrance = np.clip(saturation * 0.7, -20, 20)

    return {
        # Core tonal
        "Exposure2012": round(float(exposure), 2),
        "Contrast2012": int(contrast),

        # White balance (SAFE)
        "Temperature": int(temperature),
        "Tint": int(tint),

        # Color intensity
        "Saturation": int(saturation),
        "Vibrance": int(vibrance),
    }

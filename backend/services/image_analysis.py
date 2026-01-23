import cv2
import numpy as np


def analyze_image(path: str) -> dict:
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Image not found")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ---------- LAB ----------
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    L, A, B = cv2.split(lab)

    # ---------- HSV ----------
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    H, S, V = cv2.split(hsv)

    return {
        "L_mean": float(np.mean(L)),
        "A_mean": float(np.mean(A) - 128),  # green-magenta
        "B_mean": float(np.mean(B) - 128),  # blue-yellow

        "S_mean": float(np.mean(S)),
        "V_mean": float(np.mean(V)),

        # Skin / foliage signals (rough but effective)
        "yellow_bias": float(np.mean(B[H < 30] - 128)) if np.any(H < 30) else 0,
        "green_bias": float(np.mean(A[(H > 35) & (H < 85)] - 128)) if np.any((H > 35) & (H < 85)) else 0,
    }

# backend/services/color_safety.py

SAFE_LIMITS = {
    "Temperature": (-8, 8),
    "Tint": (-6, 6),

    "Exposure2012": (-1.2, 0.8),
    "Contrast2012": (-20, 25),

    "Highlights2012": (-60, -10),
    "Shadows2012": (10, 50),
    "Whites2012": (-40, 0),
    "Blacks2012": (0, 30),

    "Vibrance": (-20, 25),
    "Saturation": (-25, 15),

    "HueAdjustmentYellow": (-8, 8),
    "HueAdjustmentGreen": (-10, 10),

    "SaturationAdjustmentYellow": (-20, 10),
    "SaturationAdjustmentGreen": (-20, 10),
}


def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)


def apply_color_safety(params: dict) -> dict:
    """
    Applies Lightroom-safe clamping + cinematic bias.
    Does NOT modify missing keys.
    """

    safe = params.copy()

    # ---- 1. CLAMP ALL DANGEROUS SLIDERS ----
    for key, (min_v, max_v) in SAFE_LIMITS.items():
        if key in safe:
            safe[key] = clamp(float(safe[key]), min_v, max_v)

    # ---- 2. TINT BIAS (cinema rule) ----
    # Prefer Tint over Temperature
    if "Temperature" in safe and "Tint" in safe:
        if abs(safe["Temperature"]) > abs(safe["Tint"]):
            safe["Temperature"] *= 0.5

    # ---- 3. SKIN-SAFE GREEN/YELLOW DAMPING ----
    for k in [
        "HueAdjustmentYellow",
        "HueAdjustmentGreen",
        "SaturationAdjustmentYellow",
        "SaturationAdjustmentGreen",
    ]:
        if k in safe:
            safe[k] *= 0.6

    return safe

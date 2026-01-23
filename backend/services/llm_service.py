import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"


def generate_lightroom_params(feature_diff: dict, retries: int = 3) -> dict:
    """
    LLM decides STYLE only
    Math decides ALL numeric values
    Lightroom-safe, frontend-safe
    """

    # ---------------- LLM PROMPT (SEMANTIC ONLY) ----------------
    prompt = f"""
You are a professional cinematic colorist.

Choose cinematic intent ONLY.

Return JSON with EXACT keys:
wb_style: ["cool", "neutral", "warm"]
contrast_style: ["soft", "balanced", "punchy"]
saturation_style: ["muted", "natural", "rich"]

Image difference data:
{feature_diff}

Return JSON only. No explanation.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # ---------------- GEMINI CALL ----------------
    for _ in range(retries):
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 503:
            time.sleep(2)
            continue

        if response.status_code != 200:
            raise Exception(response.text)

        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        ai = json.loads(text)
        break
    else:
        raise Exception("Gemini overloaded")

    # ---------------- SEMANTIC INTENT ----------------
    wb_style = ai.get("wb_style", "neutral")
    contrast_style = ai.get("contrast_style", "balanced")
    saturation_style = ai.get("saturation_style", "natural")

    # ---------------- NUMERIC PARAMS (DETERMINISTIC) ----------------
    params = {}

    # Exposure (safe range)
    params["Exposure2012"] = round(feature_diff.get("exposure", -0.3), 2)

    # Contrast
    params["Contrast2012"] = {
        "soft": 8,
        "balanced": 14,
        "punchy": 20
    }[contrast_style]

    # Saturation
    params["Saturation"] = {
        "muted": -12,
        "natural": -6,
        "rich": 6
    }[saturation_style]

    params["Vibrance"] = {
        "muted": -10,
        "natural": 0,
        "rich": 10
    }[saturation_style]

    # ---------------- WHITE BALANCE (HARD SAFE) ----------------
    if wb_style == "cool":
        params["Temperature"] = -6
        params["Tint"] = -2
    elif wb_style == "warm":
        params["Temperature"] = 6
        params["Tint"] = 3
    else:
        params["Temperature"] = 0
        params["Tint"] = 0

    # ---------------- CINEMATIC TONAL BASE ----------------
    params["Highlights2012"] = -40
    params["Shadows2012"] = 30
    params["Whites2012"] = -20
    params["Blacks2012"] = 15

    params["Texture"] = -5
    params["Clarity2012"] = -10
    params["Dehaze"] = -6

    # ---------------- HSL (SAFE & FILMIC) ----------------
    params["HueAdjustmentYellow"] = -10
    params["SaturationAdjustmentYellow"] = -8
    params["LuminanceAdjustmentYellow"] = -8

    params["HueAdjustmentGreen"] = 15
    params["SaturationAdjustmentGreen"] = -6
    params["LuminanceAdjustmentGreen"] = -12

    # ---------------- COLOR GRADING (SUBTLE) ----------------
    params["SplitToningShadowHue"] = 200
    params["SplitToningShadowSaturation"] = 8
    params["SplitToningHighlightHue"] = 45
    params["SplitToningHighlightSaturation"] = 8

    params["ColorGradeMidtoneHue"] = 35
    params["ColorGradeMidtoneSat"] = 6
    params["ColorGradeBlending"] = 50
    params["ColorGradeBalance"] = -5

    # ---------------- FILM FINISH ----------------
    params["GrainAmount"] = 10
    params["PostCropVignetteAmount"] = -10

    return params

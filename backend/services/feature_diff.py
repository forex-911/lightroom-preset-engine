def compute_feature_difference(inp: dict, ref: dict) -> dict:
    return {
        "exposure": (ref["L_mean"] - inp["L_mean"]) / 100,
        "contrast": (ref["V_mean"] - inp["V_mean"]) / 5,

        # WB direction (NOT numeric temperature)
        "wb_blue_yellow": ref["B_mean"] - inp["B_mean"],
        "wb_green_magenta": ref["A_mean"] - inp["A_mean"],

        "saturation": (ref["S_mean"] - inp["S_mean"]) / 10,

        "yellow_bias": ref["yellow_bias"] - inp["yellow_bias"],
        "green_bias": ref["green_bias"] - inp["green_bias"],
    }

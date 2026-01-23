import os
import uuid
from datetime import datetime


def clamp(v, a, b):
    return max(min(v, b), a)


def map_temperature(style):
    return {
        "cool": -25,
        "neutral": 0,
        "warm": 20
    }.get(style, 0)


def generate_xmp_preset(params: dict, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    name = f"AI_Cinematic_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    uid = str(uuid.uuid4())

    # --- Extract WB safely ---
    temperature = int(max(-20, min(20, params.get("Temperature", 0))))
    tint = int(max(-20, min(20, params.get("Tint", 0))))

    # --- Remove WB keys from loop ---
    params = params.copy()
    params.pop("Temperature", None)
    params.pop("Tint", None)

    xmp = f"""<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
   xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
   crs:PresetType="Normal"
   crs:PresetName="{name}"
   crs:UUID="{uid}"
   crs:ProcessVersion="11.0">

   <crs:WhiteBalance>Custom</crs:WhiteBalance>
"""

    # --- Write ALL non-WB params ---
    for k, v in params.items():
        xmp += f"   <crs:{k}>{v}</crs:{k}>\n"

    # --- Write WB LAST (CRITICAL) ---
    xmp += f"""
   <crs:Temperature>{temperature}</crs:Temperature>
   <crs:Tint>{tint}</crs:Tint>

   <crs:ToneCurveName2012>Custom</crs:ToneCurveName2012>
   <crs:ToneCurvePV2012>
    <rdf:Seq>
     <rdf:li>0,8</rdf:li>
     <rdf:li>32,28</rdf:li>
     <rdf:li>64,60</rdf:li>
     <rdf:li>128,130</rdf:li>
     <rdf:li>192,190</rdf:li>
     <rdf:li>255,245</rdf:li>
    </rdf:Seq>
   </crs:ToneCurvePV2012>

  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""

    path = os.path.join(output_dir, f"{name}.xmp")
    with open(path, "w", encoding="utf-8") as f:
        f.write(xmp)

    return path


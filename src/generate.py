#!/usr/bin/env python3
"""
On-Demand Dynamic Challenge File Generator — Scouts of the Northern Watch (AdwaCTF).

Environment variables:
  - FLAG: Dynamic participant-specific flag
  - USER_ID: Optional participant or team identifier
  - OUTPUT_FILENAME: Primary output file name (default: recon_dispatch.txt)
  - OUTPUT_DIR: Target directory to write to
"""

import os
import sys
import json
import hashlib
from pathlib import Path

# 64-character imperial alphabet (internal only — NOT published to players)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}"
M = len(ALPHABET)  # 64

# Vigenère key — the OSINT answer, never written to any output file
KEY = "SOLODA"


def encrypt_text(text: str, key: str) -> str:
    out = []
    for i, c in enumerate(text):
        if c in ALPHABET:
            k = key[i % len(key)]
            shift = ALPHABET.index(k)
            c_idx = ALPHABET.index(c)
            out.append(ALPHABET[(c_idx + shift) % M])
        else:
            out.append(c)
    return "".join(out)


def get_flag() -> str:
    flag = os.environ.get("FLAG", "").strip()
    if flag:
        return flag
    for c in ["flag.txt", "/app/flag.txt", "../flag.txt"]:
        if os.path.isfile(c):
            try:
                val = open(c, encoding="utf-8").read().strip()
                if val:
                    return val
            except OSError:
                pass
    return "AdwaCTF{s0l0d4_sc0u7s_sp0tt3d_b4r4t13r1_1896}"


def main():
    flag    = get_flag()
    user_id = os.environ.get("USER_ID", "scout_operative").strip()
    here    = Path(__file__).resolve().parent.parent

    output_path = os.environ.get("OUTPUT_PATH", "").strip()
    if output_path:
        target_file = Path(output_path).resolve()
        target_dir  = target_file.parent
        target_dispatch_name = target_file.name
    elif len(sys.argv) > 1 and sys.argv[1].strip():
        arg_path = Path(sys.argv[1].strip()).resolve()
        if arg_path.is_dir() or sys.argv[1].endswith("/"):
            target_dir = arg_path
            target_dispatch_name = "recon_dispatch.txt"
        else:
            target_dir = arg_path.parent
            target_dispatch_name = arg_path.name
    else:
        env_dir = os.environ.get("OUTPUT_DIR", "").strip()
        if env_dir:
            target_dir = Path(env_dir).resolve()
        elif Path("/output").is_dir():
            target_dir = Path("/output")
        else:
            target_dir = here / "output"
        target_dispatch_name = os.environ.get("OUTPUT_FILENAME", "recon_dispatch.txt").strip()

    target_dir.mkdir(parents=True, exist_ok=True)

    encrypted_wire = encrypt_text(flag, KEY)

    # -------------------------------------------------------------------------
    # recon_dispatch.txt — pure narrative intelligence report.
    # No ciphertext, no alphabet, no cipher hint, no crypto content whatsoever.
    # -------------------------------------------------------------------------
    dispatch_content = f"""===============================================================================
IMPERIAL SCOUT RECONNAISSANCE DISPATCH
HEADQUARTERS OF RAS ALULA ENGIDA & FITAWRARI GEBEYEHU
NIGHT OF 29 YEKATIT 1888 (29 FEBRUARY 1896) — ADVANCE MOUNTAIN VANTAGE
SESSION ID: {user_id}
===============================================================================

To His Imperial Majesty Menelik II, King of Kings of Ethiopia:

Our balambaras lookouts, stationed atop the northern basalt crags, relay the
following field intelligence. Enemy campfires burn across the plateau of Sauria.
At 21:00, General Baratieri's columns departed their camp — four brigades, four
roads, four fates. What follows is the last confirmed scout report before dawn.

OBSERVED ENEMY DISPOSITIONS:

  I.  NATIVE BRIGADE — Brigadier General Matteo Albertone
      Guides leading Albertone's column have taken a southern branch path
      below the true pass. His askari have crossed into the Enda Kidane
      Mehret valley and are cut off from Arimondi's flank.
      Last position: 14.1500° N, 38.8667° E (17:00 hrs)

  II. CENTRAL COLUMN — General Giuseppe Arimondi
      Arimondi advances on the Mariam Shavitu road, converging toward
      the high ravine east of our position.
      Last position: 14.1667° N, 38.9333° E (20:30 hrs)

  III. RIGHT WING — General Vittorio Dabormida
      Dabormida's brigade diverges northward along the Abbai Garima.
      Their direction of march takes them into broken ground.
      Last position: 14.1833° N, 38.9500° E (21:00 hrs)

  IV. RESERVE — General Giuseppe Ellena
      Ellena's force remains at Sauria camp, 14.1250° N, 38.8333° E.
      No movement observed as of last scout relay.

FIELD ASSESSMENT:
The Italian high command has issued a general advance trusting that the four
columns will converge before dawn. Baratieri does not know that Albertone
has already overextended. Our commander expects confusion in the enemy's
ranks before first light.

A runner has been dispatched to field headquarters with a sealed tactical
message. It was encoded at our observation post before departure.
The post's field log accompanies this dispatch.

Fitawrari Gebeyehu — Northern Watch Command
===============================================================================
"""

    # -------------------------------------------------------------------------
    # italian_field_log.json — the structural evidence.
    # Contains the ciphertext as intercepted_transmission (opaque blob).
    # Coordinates of the observation post are present — no name, no cipher hint.
    # Players must research the peak, discover the cipher scheme, decrypt.
    # -------------------------------------------------------------------------
    field_log = {
        "operation": "Operazione Adua",
        "command": "Regio Corpo Truppe Coloniali d'Eritrea",
        "commander": "Tenente Generale Oreste Baratieri",
        "date": "1896-03-01T05:30:00+03:00",
        "field_stations": [
            {
                "station_id": "NW-PRIMARY",
                "type": "observation_post",
                "latitude": 14.1750,
                "longitude": 38.8917,
                "elevation_meters": 2434,
                "description": "Twin-peaked basalt prominence. Northern gateway to Adwa."
            },
            {
                "station_id": "NW-RELAY",
                "type": "runner_relay",
                "latitude": 14.1600,
                "longitude": 38.8800,
                "elevation_meters": 2180,
                "description": "Mule-track junction, relay handoff point."
            }
        ],
        "intercepted_transmission": encrypted_wire,
        "alberto_ne_last_signal": "COLUMN ADVANCING — KIDANE MEHRET PASS — ETA DAWN",
        "baratieri_command_note": "Advance confirmed. Columns to converge at designated ridgeline.",
        "remarks": "Signal captured by field telegraph operator at NW-PRIMARY. Contents sealed."
    }
    field_log_content = json.dumps(field_log, indent=2) + "\n"

    env_dir = os.environ.get("OUTPUT_DIR", "").strip()

    dirs_to_write = {target_dir}
    if Path("/output").is_dir():
        dirs_to_write.add(Path("/output"))
    if (here / "output").is_dir() and not env_dir and not output_path and len(sys.argv) <= 1:
        dirs_to_write.add(here / "output")

    for d in dirs_to_write:
        try:
            d.mkdir(parents=True, exist_ok=True)
            dispatch_file = d / target_dispatch_name
            with open(dispatch_file, "w", encoding="utf-8") as f:
                f.write(dispatch_content)
            os.chmod(dispatch_file, 0o666)
            json_file = d / "italian_field_log.json"
            with open(json_file, "w", encoding="utf-8") as f:
                f.write(field_log_content)
            os.chmod(json_file, 0o666)
        except OSError:
            pass

    if (here / "dist").is_dir() and not env_dir and not output_path and len(sys.argv) <= 1:
        try:
            with open(here / "dist" / "recon_dispatch.txt", "w", encoding="utf-8") as f:
                f.write(dispatch_content)
            with open(here / "dist" / "italian_field_log.json", "w", encoding="utf-8") as f:
                f.write(field_log_content)
        except OSError:
            pass

    print(f"[generator] user_id={user_id}")
    print(f"[generator] target_dir={target_dir}")
    print(f"[generator] generated: {target_dispatch_name}, italian_field_log.json")


if __name__ == "__main__":
    main()

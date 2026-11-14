#!/usr/bin/env python3
"""
On-Demand Dynamic Challenge File Generator for Scouts of Mount Soloda (AdwaCTF).

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

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}"
M = len(ALPHABET)  # 64

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
    wire_hash = hashlib.sha256(flag.encode()).hexdigest()

    # NOTE: KEY is intentionally NOT included in the output files.
    # Players must research the geographic identity of the scout peak using
    # the coordinates and elevation provided in the field log.
    dispatch_content = f"""===============================================================================
IMPERIAL SCOUT RECONNAISSANCE DISPATCH
HEADQUARTERS OF RAS ALULA ENGIDA & FITAWRARI GEBEYEHU
NIGHT OF 29 YEKATIT 1888 (29 FEBRUARY 1896) - ADVANCE MOUNTAIN VANTAGE
SESSION ID: {user_id}
===============================================================================

To His Imperial Majesty Menelik II, King of Kings of Ethiopia:

Our peasant balambaras lookouts stationed on the precipitous northern cliffs
have observed the campfires of the Italian expeditionary force at Sauria.
At 21:00 hours, General Baratieri began his advance toward the passes of Adwa.

TERRAIN INTELLIGENCE & OBSERVATION POST IDENTIFICATION:
Our primary observation redoubt is established on a famous volcanic landmark
directly commanding the northern gateway to Adwa town:
  - Elevation: 2,434 meters above sea level
  - Coordinates: 14.1750° N, 38.8917° E
  - Geography: Twin-peaked basalt mountain rising abruptly from the high plateau
  - Landmark codename: [CLASSIFIED — refer to italian_field_log.json]

OBSERVED ENEMY MOVEMENTS:
1. Native Brigade (General Matteo Albertone):
   Albertone's Tigrayan guides misled his column into the southern depression.
   He has marched past the true pass into the isolated Enda Kidane Mehret
   valley (14.1500° N, 38.8667° E), separating himself from the central army!

2. Central Column (General Giuseppe Arimondi):
   Advancing toward Mount Raio (14.1667° N, 38.9333° E).

3. Right Column (General Vittorio Dabormida):
   Diverging toward the Mariam Shavitu ravine (14.1833° N, 38.9500° E).

===============================================================================
INTERCEPTED SCOUT RUNNER WIRE (SECURE DISPATCH):
To prevent Italian telegraphers from reading our tactical clearance, the runner
enciphered the royal flag token using the 64-character imperial alphabet:
ALPHABET: {ALPHABET}

The cipher type is Vigenère. The key is derived from the geographic identity
of the observation post recorded in the field log — UPPERCASE, one word.

ENCIPHERED WIRE:
{encrypted_wire}

INTELLIGENCE CHECKSUM (SHA-256):
{wire_hash}
===============================================================================
"""

    # JSON field log — coordinates present but landmark name redacted.
    # Players must resolve the coordinates externally to identify the key.
    field_log = {
        "operation": "Operazione Adua",
        "command": "Regio Corpo Truppe Coloniali d'Eritrea",
        "commander": "Tenente Generale Oreste Baratieri",
        "date": "1896-03-01T05:30:00+03:00",
        "intercepted_notes": {
            "scout_observation_peak": {
                "latitude": 14.1750,
                "longitude": 38.8917,
                "elevation_meters": 2434,
                "classification": "CLASSIFIED"
            },
            "albertone_fatal_error": "Marched past Kidane Mehret to Enda Kidane Mehret",
            "cipher_note": "Vigenere over 64-char alphabet. Key = UPPERCASE name of the peak at the coordinates above.",
            "verification_hashes": {
                "flag_sha256": wire_hash
            }
        }
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

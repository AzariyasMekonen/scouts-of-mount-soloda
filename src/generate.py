#!/usr/bin/env python3
"""
On-Demand Dynamic Challenge File Generator — Scouts of the Northern Watch (AdwaCTF).

Environment variables:
  - FLAG: Dynamic participant-specific flag (e.g. AdwaCTF{...})
  - USER_ID: Optional participant or team identifier
  - OUTPUT_FILENAME: Primary output file name (default: recon_dispatch.txt)
  - OUTPUT_DIR: Target directory to write to
"""

import os
import sys
import json
from pathlib import Path

KEY = "SOLODA"


def vigenere_encrypt(text: str, key: str) -> str:
    key = key.upper()
    res = []
    ki = 0
    for c in text:
        if "A" <= c <= "Z":
            k = ord(key[ki % len(key)]) - ord("A")
            res.append(chr((ord(c) - ord("A") + k) % 26 + ord("A")))
            ki += 1
        elif "a" <= c <= "z":
            k = ord(key[ki % len(key)]) - ord("A")
            res.append(chr((ord(c) - ord("a") + k) % 26 + ord("a")))
            ki += 1
        else:
            res.append(c)
    return "".join(res)


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
    flag = get_flag()
    user_id = os.environ.get("USER_ID", "scout_operative").strip()
    here = Path(__file__).resolve().parent.parent

    output_path = os.environ.get("OUTPUT_PATH", "").strip()
    if output_path:
        target_file = Path(output_path).resolve()
        target_dir = target_file.parent
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

    encrypted_wire = vigenere_encrypt(flag, KEY)

    # Clean narrative recon dispatch — atmospheric, concise, no spoilers
    dispatch_content = f"""===============================================================================
IMPERIAL SCOUT RECONNAISSANCE DISPATCH
HEADQUARTERS OF RAS ALULA ENGIDA & FITAWRARI GEBEYEHU
NIGHT OF 29 YEKATIT 1888 (29 FEBRUARY 1896) — ADVANCE MOUNTAIN VANTAGE
SESSION ID: {user_id}
===============================================================================

To His Imperial Majesty Menelik II, King of Kings of Ethiopia:

Our balambaras lookouts, stationed on the precipitous northern crags, report
enemy columns departing their camp at Sauria under cover of night.

OBSERVED ENEMY DISPOSITIONS:
  - Native Brigade (Albertone): 14.1500° N, 38.8667° E — Diverging into southern valley.
  - Central Column (Arimondi):  14.1667° N, 38.9333° E — Advancing toward high ravine.
  - Right Wing (Dabormida):     14.1833° N, 38.9500° E — Moving through northern gorge.
  - Reserve (Ellena):           14.1250° N, 38.8333° E — Static at Sauria perimeter.

PRIMARY OBSERVATION REDOUBT:
  - Coordinates: 14.1750° N, 38.8917° E
  - Elevation:   2,434 m

INTERCEPTED RUNNER WIRE:
{encrypted_wire}

Fitawrari Gebeyehu — Northern Watch Command
===============================================================================
"""

    field_log = {
        "operation": "Operazione Adua",
        "command": "Regio Corpo Truppe Coloniali d'Eritrea",
        "commander": "Tenente Generale Oreste Baratieri",
        "date": "1896-03-01T05:30:00+03:00",
        "observation_post": {
            "latitude": 14.1750,
            "longitude": 38.8917,
            "elevation_meters": 2434
        },
        "intercepted_transmission": encrypted_wire
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

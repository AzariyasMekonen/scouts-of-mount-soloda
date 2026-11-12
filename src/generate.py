#!/usr/bin/env python3
"""
On-Demand Dynamic Challenge File Generator for Scouts of Mount Soloda (AdwaCTF).

Environment variables:
  - FLAG: Dynamic participant-specific flag (e.g. 'AdwaCTF{...}')
  - USER_ID: Optional participant or team identifier
  - OUTPUT_FILENAME: Output file name (default: 'recon_dispatch.txt')
  - OUTPUT_DIR: Target directory to write to (default: '/output')
"""

import os
import sys
import hashlib
from pathlib import Path

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}"
M = len(ALPHABET) # 64

# Landmark key for Mount Soloda
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

    # Check candidates
    candidates = ["flag.txt", "/app/flag.txt", "../flag.txt"]
    for c in candidates:
        if os.path.isfile(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    val = f.read().strip()
                    if val:
                        return val
            except OSError:
                pass

    return "AdwaCTF{s0l0d4_sc0u7s_sp0tt3d_b4r4t13r1_1896}"

def main():
    flag = get_flag()
    user_id = os.environ.get("USER_ID", "scout_operative").strip()

    output_path = os.environ.get("OUTPUT_PATH", "").strip()
    if output_path:
        target_path = output_path
    elif len(sys.argv) > 1 and sys.argv[1].strip():
        target_path = sys.argv[1].strip()
    else:
        output_dir = os.environ.get("OUTPUT_DIR", "/output").strip()
        output_filename = os.environ.get("OUTPUT_FILENAME", "recon_dispatch.txt").strip()
        target_path = os.path.join(output_dir, output_filename)

    encrypted_wire = encrypt_text(flag, KEY)
    wire_hash = hashlib.sha256(flag.encode()).hexdigest()

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
Our primary observation redoubt is established on the famous volcanic landmark 
directly commanding the northern gateway to Adwa town:
  - Elevation: 2,434 meters above sea level
  - Coordinates: 14.1750° N, 38.8917° E
  - Geography: Twin-peaked basalt mountain rising abruptly from the high plateau
  - Historical Name: Mount Soloda (Primary Landmark Key: SOLODA)

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
To prevent Italian telegraphers from reading our sovereign tactical clearance,
the runner enciphered the royal flag token across the 64-character alphabet:
ALPHABET: {ALPHABET}

The cipher key is the uppercase landmark name of our scout observation mountain:
KEY: SOLODA

ENCIPHERED WIRE:
{encrypted_wire}

INTELLIGENCE CHECKSUM (SHA-256):
{wire_hash}
===============================================================================
"""

    paths_to_write = {os.path.abspath(target_path)}
    if os.path.isdir("/output") or target_path.startswith("/output"):
        paths_to_write.add(os.path.abspath("/output/recon_dispatch.txt"))

    for p in paths_to_write:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(dispatch_content)
            try:
                os.chmod(p, 0o666)
            except OSError:
                pass
        except OSError:
            pass

    print(f"[generator] user_id={user_id}")
    print(f"[generator] flag={flag}")
    print(f"[generator] target={target_path}")
    print(f"[generator] successfully generated recon dispatch ({len(dispatch_content)} bytes).")

if __name__ == "__main__":
    main()

# Scouts of Mount Soloda (OSINT / Dynamic Generator, Easy)

**Story:**
On the eve of March 1, 1896, Ethiopian lookouts under Ras Alula Engida and Fitawrari Gebeyehu tracked Italian troop movements from the jagged basalt crest of Mount Soloda. Their intelligence proved decisive when General Albertone's brigade took a wrong turn toward Enda Kidane Mehret, opening a critical gap in the Italian lines.

## Mechanics
- This challenge supports the platform's **On-Demand Dynamic File Generator** to generate personalized challenge files with participants' unique dynamic flags.
- Players examine `output/recon_dispatch.txt` and `output/italian_field_log.json`.
- The dispatch provides terrain intelligence for the scout observation peak:
  - Elevation: 2,434 meters
  - Coordinates: 14.1750° N, 38.8917° E
  - Geography: Twin-peaked volcanic plug commanding the northern pass to Adwa town.
  - OSINT / Geographic identification identifies the mountain as **Mount Soloda** -> Key: `SOLODA`.
- The runner enciphered the dynamic flag using a 64-symbol Vigenère cipher:
  - Alphabet: `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}`
  - Key: `SOLODA`
- Applying the key `SOLODA` decrypts `ENCIPHERED WIRE` to recover the player's dynamic flag.
- An intelligence checksum (SHA-256) is provided in the dispatch to confirm validity.

## Dynamic File Generator Settings
- **Type**: `dynamic`
- **Output Filename**: `recon_dispatch.txt`
- **Environment Variables**:
  - `FLAG`: Dynamic participant flag (e.g. `AdwaCTF{...}`)
  - `USER_ID`: Unique participant or team identifier
  - `OUTPUT_DIR`: Target directory (defaults to `/output`)
  - `OUTPUT_FILENAME`: Name of output file inside `/output/` (defaults to `recon_dispatch.txt`)

## Solution Walkthrough
1. Read `recon_dispatch.txt` and note the observation peak name `SOLODA`.
2. Extract the ciphertext under `ENCIPHERED WIRE:`.
3. Shift each character back by `shift = ALPHABET.index(key[i % len(key)])` over the 64-symbol alphabet.
4. Verify recovered flag against the provided SHA-256 checksum.

Run `solve/solve.py` to solve automatically.

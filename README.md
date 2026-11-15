# Scouts of the Northern Watch (OSINT / Dynamic Generator, Easy)

**Story:**
On the eve of March 1, 1896, Ethiopian lookouts under Ras Alula Engida and Fitawrari Gebeyehu tracked Italian troop movements from high basalt crests commanding the northern passes to Adwa. Their reconnaissance proved decisive when General Albertone's brigade took a southern branch path into an isolated valley, fracturing the Italian invasion plan before dawn broke.

## Files
Participants receive the scout field reconnaissance files:
- `output/recon_dispatch.txt`: Field dispatch describing observed troop dispositions, vantage coordinates, and an intercepted runner's wire.
- `output/italian_field_log.json`: Captured Italian signals log documenting outpost coordinates and intercepted traffic.

## Objective
Trace the scouts' primary observation vantage point using field intelligence, and recover the sealed tactical runner dispatch.

## Dynamic File Generator Settings
- **Type**: `dynamic`
- **Output Filename**: `recon_dispatch.txt`
- **Environment Variables**:
  - `FLAG`: Dynamic participant flag (e.g. `AdwaCTF{...}`)
  - `USER_ID`: Unique participant or team identifier
  - `OUTPUT_DIR`: Target directory (defaults to `/output`)
  - `OUTPUT_FILENAME`: Name of output file inside `/output/` (defaults to `recon_dispatch.txt`)

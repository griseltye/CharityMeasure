# CHARITYS_MEASURE — v13 (FastAPI blueprint)

This drop-in blueprint implements the Row 20 behavior exactly as requested:

- "POINTS SHORT OF THE GLORY OF GOD" shows **16**
- If **Y**:
  - 20A → "JESUS ADDS TO YOUR EFFORT"
  - Red header → "JESUS ADDS"
  - Number under it → `81 - current total`
  - Row 21 label → "YOUR SCORE ADDED WITH JESUS"
  - Row 21 value → **81**
- If **N**:
  - 20A → "satan multiplies your effort by"
  - Red header → "SATAN MULTIPLE"
  - Number under it → **0**
  - Row 21 label → "YOUR SCORE WITH SATAN'S ADDS"
  - Row 21 value → **0**

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000

## Deploy to Render

- Set the start command to: `uvicorn main:app --host 0.0.0.0 --port 10000`
- Make sure `index.html` sits at the project root and `static/app.js` is present.

## Notes

- Helper functions `lookup_inputs`, `e18_lookup`, and `scripture_lookup` are no-ops here so you can plug in your own lookup tables without breaking.
- The UI uses IDs like `r20_left`, `r20_header_adds`, `r20_mid`, `r20_short`, `r21_left`, `r21_mid` to mirror your spreadsheet layout.

## Render Python 3.13 build error fix
This repo includes `.python-version` (3.12.4) and `render.yaml` to pin Python 3.12.4 on Render. This avoids `pydantic-core` building from source with Rust/maturin.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import math
import os

app = FastAPI()

# Serve static files if present
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Use project root for templates (index.html at root)
templates = Jinja2Templates(directory=".")


class InputPayload(BaseModel):
    scores: List[Optional[float]]  # first 8 gate scores (rows D8..D15)
    yn: Optional[str] = ""         # 'Y' or 'N'


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Labels can be customized server-side if desired
    labels = [
        "GATE 1","GATE 2","GATE 3","GATE 4",
        "GATE 5","GATE 6","GATE 7","GATE 8"
    ]
    return templates.TemplateResponse("index.html", {"request": request, "labels": labels})


# ---------- Helpers (kept minimal so this runs standalone) ----------
def lookup_inputs(v: float):
    # Return tuple of (meaning1, meaning2, meaning3) for each gate cell if you want.
    # Keeping blank for this blueprint.
    return ("", "", "")

def e18_lookup(ratio: float) -> str:
    # Map D18 ratio to a message; left blank for now.
    return ""

def scripture_lookup(total: float) -> str:
    # Provide scripture text for D21 if needed; blank for now.
    return ""

R21_YES_REF = ""
R21_NO_REF  = ""


@app.post("/calc", response_class=JSONResponse)
async def calc(payload: InputPayload):
    # Clean first 8 scores (D8..D15)
    clean = [(v if isinstance(v, (int, float)) else None) for v in (payload.scores or [])[:8]]
    ssum = sum(v for v in clean if isinstance(v, (int, float)))
    any_val = any(isinstance(v, (int, float)) for v in clean)

    # Row 16 total (rounded up to tenths like sheet)
    d16 = math.ceil((ssum if any_val else 0) * 10) / 10

    # B17 constant (perfect with Jesus)
    b17 = 81.0

    # D18 = proportion of 81
    d18 = (d16 / b17) if any_val else 0.0

    # Y/N
    yes = (payload.yn or '').strip().lower() == 'y'

    # --- Row 20 spec ---
    points_short_glory = 16  # must display 16

    if yes:
        # "JESUS ADDS" value should bring total to 81
        d20 = max(0.0, b17 - d16)
        # Final score when Y must be exactly 81
        d21 = 81.0
        r20_banner = "JESUS ADDS TO YOUR EFFORT"
        r20_adds_label = "JESUS ADDS"
        r21_label = "YOUR SCORE ADDED WITH JESUS"
    else:
        # "SATAN MULTIPLE" value is zero and final becomes zero
        d20 = 0.0
        d21 = 0.0
        r20_banner = "satan multiplies your effort by"
        r20_adds_label = "SATAN MULTIPLE"
        r21_label = "YOUR SCORE WITH SATAN'S ADDS"

    # Lookups (safe no-ops here)
    meanings = [ (("", "", "") if (v is None) else lookup_inputs(float(v))) for v in clean ]
    e18_text = (e18_lookup(d18) if any_val else "")
    scripture = scripture_lookup(d21)

    # Row 19 message
    if (payload.yn or '') == '':
        r19_msg = ''
    elif yes:
        r19_msg = 'JESUS SAVES YOU FROM ALL YOUR SINS!'
    else:
        r19_msg = "YOU DON'T TRUST JESUS, AND ARE LOST!"

    # Row 22: Y/N dependent
    if (payload.yn or '') == '':
        row22 = {'left': '', 'right': ''}
    elif yes:
        row22 = {'left': 'CHRIST STATURED AND RAPTURED', 'right': 'WELCOME TO THE SAFE HOUSE OF THE LORD'}
    else:
        row22 = {'left': 'YOU ARE NOT WRITTEN INTO THE BOOK OF LIFE:', 'right': 'WELCOME TO ETERNAL STATE OF DAMNATION'}

    return {
        'd16': d16,
        'sum': ssum,
        'b17': b17,
        'd18': d18,
        'd20': d20,                    # goes under "JESUS ADDS" / "SATAN MULTIPLE"
        'd21': d21,                    # becomes 81 on Y, 0 on N
        'meanings': meanings,
        'e18': e18_text,
        'scripture': scripture,
        'r19_msg': r19_msg,
        'any': any_val,
        'r21_ref': (R21_YES_REF if yes else (R21_NO_REF if (payload.yn or '') != '' else '')),
        'row22': row22,
        # explicit labels for Row 20/21
        'row20': {
            'banner': r20_banner,              # 20A text
            'adds_label': r20_adds_label,      # red header: JESUS ADDS / SATAN MULTIPLE
            'points_short_glory': points_short_glory  # always 16
        },
        'row21': {
            'label': r21_label                 # "YOUR SCORE ADDED WITH JESUS" / "...SATAN'S ADDS"
        }
    }
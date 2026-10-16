# PrintTune AI

AI-assisted 3D printer tuning, starting with Klipper/Moonraker.

## Current status

Early prototype: **read-only printer discovery**. This is not yet an automatic calibration system. It does not home, heat, move, or print.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
export MOONRAKER_URL=http://your-printer-host:7125
uvicorn printtune.api:app --host 127.0.0.1 --port 8080
```

Visit http://127.0.0.1:8080/docs and call `GET /api/capabilities`. Alternatively:

```bash
printtune-scan --url http://your-printer-host:7125 --output capabilities.json
```

Do **not** publish raw printer configs or generated capability reports without reviewing them for network addresses, credentials, and other personal information.

## Planned milestones

1. Read-only discovery and capability export
2. Slicer/material profile import and standardized calibration geometry
3. Photo capture and defect analysis with confidence estimates
4. Bounded setting recommendations and second-print verification
5. Optional controlled automation, only after safety validation

Two prints per material is a target, not a guarantee of ideal settings.

## Security

Do not expose Moonraker or this development server to the public internet. Use a trusted local network, and keep heater, motor, and printer safety controls outside the AI optimizer.

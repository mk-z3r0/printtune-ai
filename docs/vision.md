# 3DBenchy vision inspection (prototype)

This implements **inference using a hosted pretrained vision model**, not a trained PrintTune-specific model. No training data or measured accuracy is claimed.

## Install and run

```bash
pip install -e .
export OPENAI_API_KEY=your_key
export PRINTTUNE_VISION_MODEL=gpt-5.5
uvicorn printtune.api:app --host 127.0.0.1 --port 8080
```

Submit 1–5 views of the **same official 3DBenchy** via multipart form:

```bash
curl -X POST http://127.0.0.1:8080/api/vision/inspect \
  -F 'views=port' -F 'images=@port.jpg' \
  -F 'views=bow' -F 'images=@bow.jpg' \
  -F 'context_json={"material":"unknown"}'
```

Accepted view names: port, starboard, bow, stern, top. Output includes defect observations, severity, confidence, visual evidence, uncertainties and suggested checks. It **never** applies settings or sends printer commands.

Use consistent lighting, a clean background and close focus. Photos are sent to the configured hosted API; obtain consent and avoid including personal information in the background. Provider usage is billed separately.

## Evaluation needed before tuning recommendations

- Collect permissioned labeled photos and known slicer/printer/material settings.
- Validate defect identification on held-out printers and materials.
- Evaluate false positives and the model's ability to abstain.
- Correlate findings with accelerometer and physical measurements.
- Only then add bounded recommendations with human approval.

Official reference: https://github.com/CreativeTools/3DBenchy/ (CC0: https://www.3dbenchy.com/license/)

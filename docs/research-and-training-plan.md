# PrintTune AI — web research and training plan

Status: research and data schema planning. **No model has been trained yet.**

## Reviewed authoritative references
- Klipper resonance compensation: https://www.klipper3d.org/Resonance_Compensation.html
- Ellis' pressure advance introduction: https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/introduction.html
- Prusa print quality troubleshooting: https://help.prusa3d.com/category/print-quality-troubleshooting_225
- Ultralytics image dataset format: https://docs.ultralytics.com/datasets/detect

## Evidence-backed principles
- Ringing requires motion/resonance context; Klipper's accelerometer data can constrain shaper recommendations.
- PA varies by filament, nozzle, temperature and toolhead; too little PA can bulge corners while too much creates gaps.
- Stringing, layer shifts, extrusion defects and warping each have multiple plausible causes; photos alone do not establish the correct numeric fix.
- Machine settings and filament-specific settings must remain separate.

## Training record (proposal)
Each labeled observation should include:
- image path, photographer permission/license, capture angle, lighting
- printer type, nozzle, hotend, material, slicer and relevant effective settings
- defect classes and region annotations, severity, human reviewer and review status
- competing diagnostic hypotheses and sensor evidence
- one controlled setting change, second-print outcome and confidence

## Model evaluation
- Hold out entire printers and materials for testing, not merely random images from the same print.
- Report per-class precision/recall and confusion matrix, calibration of confidence, and frequency of incorrect setting recommendations.
- Test abstention when images are ambiguous or printer configuration is missing.
- Only permit bounded reversible changes after user review and real-world validation.
- Respect source copyrights and licenses. Linking to web images does not confer permission to train or redistribute them.

## Next implementation
1. Build ingestion schema with provenance and license fields.
2. Add a photo annotation/review UI.
3. Collect original, permissioned benchmark images and matching settings.
4. Evaluate a baseline vision model against held-out printers.
5. Validate two-print recommendation quality before enabling any automatic printer writes.

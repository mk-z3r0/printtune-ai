# Defect diagnosis knowledge base (v0.1)

This is a **hypothesis library**, not a trained visual classifier. Each symptom has competing causes; never infer an exact numeric setting from a photo alone. No automatic writes to Klipper.

## Reference sources
- [Prusa print quality troubleshooting](https://help.prusa3d.com/category/print-quality-troubleshooting_225)
- [Ellis' pressure advance](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/introduction.html)
- [Ellis' extrusion multiplier](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html)
- [OrcaSlicer calibration guide](https://www.orcaslicer.com/wiki/calibration_guide/)
- [OrcaSlicer pressure advance](https://www.orcaslicer.com/wiki/calibration/pressure_advance_calib.html)

## Defect → observations → candidate causes → next check

| Defect | Visible evidence | Possible causes | Discriminating evidence / first action |
| --- | --- | --- | --- |
| Ringing / ghosting | Repeated fading ripples after sharp corners | Motion resonance, overly aggressive acceleration, loose hardware | Check ripple spacing/direction and existing accelerometer resonance results; inspect mechanics before proposing input-shaper/acceleration changes |
| Corner bulges | Swollen external corners or blobs after deceleration | Insufficient pressure advance, excess extrusion, cooling | Compare straight-wall flow to corners; check whether PA is set in slicer or Klipper; run bounded PA sweep only when justified |
| Corner gaps | Thin or missing material immediately after turns | Excessive PA, extrusion lag, flow limit | Inspect start-of-line vs end-of-line, compare speed/flow and current PA |
| Under-extrusion | Gaps, thin walls, intermittent missing material | Partial clog, slipping extruder, low temperature, too-high volumetric demand, incorrect flow | Determine whether defects worsen with speed; inspect extruder and hotend before changing multiplier |
| Over-extrusion | Raised top-surface ridges, thick walls | Excessive material flow, incorrect filament/nozzle assumptions | Verify extrusion calibration and slicer flow; avoid treating top-surface artifacts as definitive proof |
| Stringing | Fine strands between separated features | Wet filament, temperature, retraction, travel behavior | Check drying history, temperature, travel and retraction before modifying settings |
| Warping | Corners lift from bed | First-layer adhesion, thermal contraction, enclosure/bed conditions | Check material, bed temperature, first-layer and chamber environment |
| Layer shifts | Abrupt lateral offset above a height | Belt/pulley slip, collision, missed steps, motion limits | Mechanical inspection; do not attempt to fix via flow or PA |
| Poor bridging | Drooping strands over unsupported gaps | Cooling, bridge flow/speed, temperature, span | Compare bridge-only regions; material-specific cooling and bridge settings |
| Layer splitting | Gaps between layers or cracks | Low thermal bonding, cooling, material moisture, chamber conditions | Check material and temperature/chamber history; prioritize strength/safety over cosmetics |
| Z banding | Periodic horizontal stripes | Z mechanics, extrusion periodicity, temperature fluctuation | Measure repeat interval and correlate with lead screw pitch or extrusion components |
| First-layer gaps / ridges | Lines too far apart or heavily squashed | Z offset, bed mesh, flow, surface preparation | Inspect first layer across bed; do not conflate Z offset with material flow |

## Decision policy

1. Read printer configuration and effective slicer/material profile; capture baseline before suggesting changes.
2. Separate machine-wide motion/mechanics from material/nozzle-specific extrusion, temperature, cooling and PA.
3. For each defect, return multiple hypotheses, evidence for/against, and confidence; permit an `insufficient_evidence` result.
4. Recommend only reversible, bounded changes and preserve the old profile.
5. Two-print target: one multi-feature benchmark plus one verification print. If cause remains ambiguous, explicitly report that rather than inventing ideal settings.
6. Use consistent photos, lighting, known geometry, and physical measurements where possible. Avoid declaring numerical accuracy from uncalibrated pixels.
7. Do not scrape or redistribute third-party reference photos without licensing review. Use source links and original/permissioned sample photos for training/evaluation.

## Validation plan

Build an original labeled image dataset with: defect type, severity, printer/material/nozzle, camera view, lighting, settings, human-reviewed diagnosis, and outcome after one controlled change. Track false positives and calibration of confidence. Hold out printers and materials in evaluation to avoid leakage.

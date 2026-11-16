# SignBridge implementation phases

Scope: an offline-capable local PyTorch demo recognizing 24 static ASL alphabet signs, aligned with SDG 10 — Reduced Inequalities. J and Z require motion and are excluded. Educational prototype, not a complete sign-language translator.

- [x] Read assignment and select a feasible SDG-aligned problem.
- [x] Acquire and attribute Sign Language MNIST; record checksums.
- [x] Implement preprocessing, CNN, deterministic training and validation selection.
- [x] Train model and evaluate once on the official test split; save actual metrics.
- [x] Build accessible image-upload demo with sample inputs and top predictions.
- [x] Check preprocessing, invalid inputs, prediction API and browser workflow.
- [x] Write SRS report, 11-slide PowerPoint and reproducible setup instructions.
- [x] Package runnable source, weights, examples and results.

## Design
Indigo ink #222653, pale blue #edf3ff, white #ffffff, teal #087f82, slate #536078. Georgia display, system sans body, monospace data. A large predicted letter sits alongside the processed hand image; no decorative dashboard. Responsive two-column input/result layout collapses on mobile.

## Requirements and limits
The notice requires a 3–4 student group, a TensorFlow/PyTorch model, documented data/training/evaluation, hard-copy SRS or research report, a PowerPoint with a dedicated SDG justification slide, and executable input-to-output demonstration. Group member details must be supplied by students. The notice's report deadline was 14 November 2026; submission is not performed by this project.

## Completion evidence

- Trained PyTorch checkpoint included; 12 epochs, selected epoch 12.
- Official test accuracy: **93.03%** on **7,172** images; macro F1 **0.9222**.
- Four model/API tests passed; Chromium sample, upload, invalid-input and mobile checks passed.
- Six-page SRS and eleven-slide editable PowerPoint generated and visually checked.
- See `docs/VERIFICATION.md`, `docs/DEMO.md` and `README.md`.

## Human submission steps

Add real group names, roll numbers, institution, section and faculty; review the report and slides; print and submit them; confirm the missed 14 November deadline with faculty. Real-world sign recognition and accessibility effectiveness remain unvalidated.

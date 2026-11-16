# Verification record

Executed locally on 16 November 2026 with Python 3.12, torch 2.15.0+cpu, NumPy 2.5.5, Pillow 13.0.0 and scikit-learn 1.9.1.

## Training and evaluation

`python train.py` completed 12 epochs using seed 42. Epoch 12 was selected by lowest validation loss. The official test set was evaluated after selection. Results are measured:

- Training: 23,336 samples; validation: 4,119; official test: 7,172.
- Test accuracy: 0.9302844394868934 (93.03%).
- Macro precision: 0.9232; macro recall: 0.9271; macro F1: 0.9222.
- Selected validation accuracy: 100%. Related augmented imagery can inflate random validation results.
- Full report, history, confusion matrix and CSV SHA256 hashes: `artifacts/metrics.json`.

## Model and HTTP checks

`python -m unittest -v test_app` passed all four tests:

1. The 24-letter mapping excludes J and Z.
2. Preprocessing produces a normalized grayscale tensor of shape [1, 1, 28, 28].
3. A 28×28 example has matching training/inference preprocessing; prediction returns ordered valid classes.
4. Live HTTP workflow serves the UI, predicts sample A, returns a processed PNG, rejects malformed/empty images, and blocks access to model weights through static routes.

## Browser and artifact checks

`python browser_check.py` passed using Chromium through Playwright 1.65.2:

- Load held-out A and recognize it as A; show three prediction rows.
- Upload held-out C through the file chooser and recognize it as C.
- Submit invalid image bytes and display the API error.
- Repeat at 390-pixel viewport width with no horizontal overflow.
- No uncaught JavaScript page errors.

Desktop/mobile screenshots were visually inspected. The SRS was rendered to six pages and every page inspected. All eleven slide previews were inspected. PPTX package integrity, geometry, font policy and first-party import checks passed.

## Not established

No independent signer study, webcam evaluation, real-world accuracy, demographic fairness, probability calibration, unknown-image rejection, load test, human accessibility study, faculty acceptance or external submission. Keep the demo server bound to loopback. The deck was not opened in Microsoft PowerPoint.

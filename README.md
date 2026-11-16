# SignBridge

Local PyTorch CNN recognizing 24 static ASL alphabet signs. SDG 10 — Reduced Inequalities. Full language translation, J/Z motion recognition, hand detection, production hosting and webcam support are outside this prototype.

## Run

Python 3.12 was used. From this folder:

```sh
python3 -m venv .venv
.venv/bin/pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r requirements.txt
.venv/bin/python server.py
```

Open http://127.0.0.1:8000. Select a test example, click Load example, then Recognize sign. Or upload a PNG/JPEG of a tightly cropped upright hand on a plain background. Example labels are ground truth, not guaranteed predictions. No internet is needed after dependencies are installed. Uploads are processed in memory.

In this workspace, the ready environment is `../../work/venv/bin/python`; run `../../work/venv/bin/python server.py` without installing again.

## Retrain and verify

```sh
.venv/bin/python train.py --epochs 12
# With server.py running in another terminal:
.venv/bin/python -m unittest -v test_app
```

Retraining overwrites artifacts/model.pt, metrics.json and test examples. The supplied report/deck reflect the delivered run; update them if retraining changes results. Training uses seed 42, a stratified 85/15 split of the official training data, Adam, cross entropy and the validation-loss-selected checkpoint. The official test split is evaluated after checkpoint selection. No augmentation is added by this implementation. See artifacts/metrics.json for per-class precision, recall, F1, confusion matrix, learning history and input checksums.

## Files

- `phase.md`: completed build checklist and remaining human submission steps.
- `model.py`: CNN, preprocessing and inference.
- `train.py`: reproducible training and evaluation.
- `server.py` and `static/`: local input-to-prediction demo.
- `test_app.py`: model and HTTP checks.
- `docs/`: SRS report, editable PowerPoint and demonstration guide.
- `data/`: attributed source CSVs; `artifacts/`: weights and measured results.

## Dataset attribution and limits

Sign Language MNIST by **datamunge**: https://www.kaggle.com/datasets/datamunge/sign-language-mnist . Downloaded CSV mirror: https://github.com/Elsaraf1/sign-language (16 November 2026). Consult the upstream dataset page for licensing terms before redistribution. Checksums identify the exact downloaded files.

The dataset contains 28×28 grayscale images and augmented examples. Random validation splitting can place related augmentations in both partitions and inflate validation performance. Official test accuracy is a dataset benchmark, not signer-independent validation. Demographic coverage, accessibility outcomes and camera robustness were not evaluated. The model always chooses one of 24 letters, even for unrelated images; probabilities are uncalibrated. Never use it as an interpreter or to make consequential decisions.

## Submission

Supply actual names and roll numbers for your 3–4 member group, section and faculty. Print the SRS after reviewing it; use the PowerPoint for the practical demonstration. The notice lists 14 November 2026 as the hard-copy deadline; confirm late-submission arrangements with faculty. Nothing has been submitted externally.

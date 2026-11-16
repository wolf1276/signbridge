# Practical demonstration

1. Start the server using README instructions and open http://127.0.0.1:8000.
2. Load sample A. Explain it is a held-out test example and the label is known.
3. Recognize it. Show the 28×28 grayscale input and top-three probabilities.
4. Load another letter, then upload `static/examples/C.png` using the file chooser to demonstrate the upload path.
5. Upload a text file through the API test and explain input validation; run `python -m unittest -v test_app` while the server is running.
6. Open `model.py`: two convolution blocks, dense layer, dropout and 24 logits.
7. Open `artifacts/metrics.json`: training/validation/test counts, selected epoch, actual held-out metrics and per-class errors.
8. Explain SDG 10 and the limitations: no full language translation, J/Z, hand detector, demographic audit or real-world generalization claim.

## Viva preparation

- Why CNN? Local spatial filters learn hand-shape patterns with shared weights.
- Why cross entropy? Supervised single-label multiclass classification.
- Why dropout? Reduce overfitting during training; disabled at inference.
- Why separate validation? Checkpoint selection must not use test labels.
- Why no J/Z? Static images cannot express these motion-dependent signs.
- What does 99% probability mean? Relative softmax output among known classes, not evidence the input is a valid sign.
- Is it a complete accessibility solution? No. Validation with Deaf users, signer-separated datasets and realistic imagery remains necessary.

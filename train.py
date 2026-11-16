"""Train on training partition; select by validation loss, evaluate test once."""
import argparse
import hashlib
import json
import random
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from PIL import Image
from model import ROOT, LETTERS, SignCNN


def read(name):
    data = np.loadtxt(ROOT/'data'/name, delimiter=',', skiprows=1, dtype=np.uint8)
    labels = data[:, 0].astype(int)
    assert set(labels) == set(range(25)) - {9}
    labels = labels - (labels > 9)
    return torch.from_numpy(data[:, 1:].astype(np.float32)/255).reshape(-1,1,28,28), torch.tensor(labels)


def main(epochs):
    torch.set_num_threads(4)
    torch.manual_seed(42); np.random.seed(42); random.seed(42)
    torch.use_deterministic_algorithms(True)
    x, y = read('sign_mnist_train.csv')
    tr, va = train_test_split(np.arange(len(y)), test_size=.15, stratify=y.numpy(), random_state=42)
    loader = DataLoader(TensorDataset(x[tr], y[tr]), batch_size=128, shuffle=True)
    model = SignCNN(); optimizer = torch.optim.Adam(model.parameters(), lr=.001)
    loss_fn = torch.nn.CrossEntropyLoss(); best = float('inf'); history = []
    for epoch in range(epochs):
        model.train(); total = 0
        for inputs, labels in loader:
            optimizer.zero_grad(); loss = loss_fn(model(inputs), labels)
            loss.backward(); optimizer.step(); total += loss.item()*len(labels)
        model.eval()
        with torch.inference_mode():
            logits = torch.cat([model(batch) for batch in x[va].split(256)])
            val_loss = loss_fn(logits, y[va]).item()
            val_acc = (logits.argmax(1)==y[va]).float().mean().item()
        row = dict(epoch=epoch+1, train_loss=total/len(tr), validation_loss=val_loss, validation_accuracy=val_acc)
        history.append(row); print(row, flush=True)
        if val_loss < best:
            best = val_loss; selected = epoch+1
            torch.save(model.state_dict(), ROOT/'artifacts/model.pt')
    model.load_state_dict(torch.load(ROOT/'artifacts/model.pt', weights_only=True)); model.eval()
    tx, ty = read('sign_mnist_test.csv')
    with torch.inference_mode():
        pred = torch.cat([model(batch).argmax(1) for batch in tx.split(256)]).numpy()
    report = classification_report(ty, pred, labels=list(range(24)), target_names=list(LETTERS), output_dict=True, zero_division=0)
    metrics = dict(seed=42, train_samples=len(tr), validation_samples=len(va), test_samples=len(ty), selected_epoch=selected,
        accuracy=accuracy_score(ty,pred), report=report, confusion_matrix=confusion_matrix(ty,pred).tolist(), history=history,
        dataset_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data').glob('*.csv')})
    (ROOT/'artifacts/metrics.json').write_text(json.dumps(metrics, indent=2))
    examples = ROOT/'static/examples'; examples.mkdir(exist_ok=True)
    for i, letter in enumerate(LETTERS):
        index = int((ty==i).nonzero()[0])
        Image.fromarray((tx[index,0].numpy()*255).astype('uint8')).save(examples/f'{letter}.png')
    print('Test accuracy:', metrics['accuracy'], flush=True)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--epochs',type=int,default=12)
    args=parser.parse_args()
    if args.epochs < 1: parser.error('--epochs must be positive')
    main(args.epochs)

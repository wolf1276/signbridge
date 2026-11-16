import io
import json
import unittest
import urllib.request
import urllib.error
import numpy as np
from PIL import Image
import torch
from model import LETTERS, ROOT, load_model, predict, preprocess

class ModelTests(unittest.TestCase):
    def test_label_contract(self):
        self.assertEqual(len(LETTERS),24)
        self.assertNotIn('J',LETTERS); self.assertNotIn('Z',LETTERS)
    def test_preprocessing(self):
        x, image=preprocess(Image.new('RGB',(60,90),'white'))
        self.assertEqual(tuple(x.shape),(1,1,28,28)); self.assertEqual(float(x.min()),1.)
        self.assertEqual(image.mode,'L')
    def test_prediction_matches_training_preprocessing(self):
        image=Image.open(ROOT/'static/examples/A.png')
        x,_=preprocess(image)
        expected=torch.tensor(np.asarray(image).copy()/255,dtype=torch.float32).reshape(1,1,28,28)
        torch.testing.assert_close(x,expected)
        result,_=predict(load_model(),image)
        self.assertEqual(len(result),3)
        self.assertTrue(all(r['letter'] in LETTERS for r in result))
        self.assertGreaterEqual(result[0]['probability'],result[1]['probability'])
    def test_http_workflow(self):
        with urllib.request.urlopen('http://127.0.0.1:8000/') as r: self.assertEqual(r.status,200)
        raw=(ROOT/'static/examples/A.png').read_bytes()
        request=urllib.request.Request('http://127.0.0.1:8000/api/predict',data=raw,method='POST')
        result=json.load(urllib.request.urlopen(request))
        self.assertEqual(result['predictions'][0]['letter'],'A')
        self.assertTrue(result['processed'].startswith('data:image/png;base64,'))
        for raw in (b'not an image',b''):
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8000/api/predict',data=raw,method='POST'))
            self.assertEqual(error.exception.code,400)
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen('http://127.0.0.1:8000/artifacts/model.pt')
        self.assertEqual(error.exception.code,404)

if __name__=='__main__': unittest.main()

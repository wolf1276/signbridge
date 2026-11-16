"""Loopback-only demo; images are processed in memory and never stored."""
import base64
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from PIL import Image, UnidentifiedImageError
import torch
from model import ROOT, load_model, predict

torch.set_num_threads(2)
Image.MAX_IMAGE_PIXELS = 16_000_000
MODEL = load_model()

class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, content_type='application/json'):
        self.send_response(status); self.send_header('Content-Type', content_type)
        self.send_header('Content-Length',str(len(body))); self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/metrics':
            return self.send(200,(ROOT/'artifacts/metrics.json').read_bytes())
        if path=='/': path='/static/index.html'
        file=(ROOT/path.lstrip('/')).resolve()
        if not file.is_relative_to(ROOT/'static') or not file.is_file():
            return self.send(404,b'{"error":"Not found"}')
        self.send(200,file.read_bytes(),'text/html; charset=utf-8' if file.suffix=='.html' else 'image/png')
    def do_POST(self):
        if self.path!='/api/predict': return self.send(404,b'{"error":"Not found"}')
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=5_000_000: raise ValueError('Choose an image smaller than 5 MB.')
            raw=self.rfile.read(size)
            with Image.open(io.BytesIO(raw)) as image:
                if image.width*image.height>16_000_000: raise ValueError('Image exceeds 16 megapixels.')
                predictions, processed=predict(MODEL,image)
            output=io.BytesIO(); processed.save(output,format='PNG')
            self.send(200,json.dumps(dict(predictions=predictions,processed='data:image/png;base64,'+base64.b64encode(output.getvalue()).decode())).encode())
        except (ValueError, OSError, UnidentifiedImageError, Image.DecompressionBombError):
            self.send(400,b'{"error":"Use a valid PNG or JPEG under 5 MB and 16 megapixels."}')

if __name__=='__main__':
    print('SignBridge: http://127.0.0.1:8000',flush=True)
    # shortcut: loopback demo server only, use a production service before network deployment.
    ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()

"""Optional: pip install playwright==1.65.2; playwright install chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1280,'height':950})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8000')
    page.get_by_role('button',name='Load example').click()
    page.get_by_role('button',name='Recognize sign').click()
    page.wait_for_function("document.getElementById('status').textContent==='Prediction ready.'")
    assert page.locator('#letter').inner_text()=='A'
    assert page.locator('.rank').count()==3
    page.screenshot(path=str(ROOT/'docs/demo-desktop.png'),full_page=True)
    page.locator('#file').set_input_files(str(ROOT/'static/examples/C.png'))
    page.get_by_role('button',name='Recognize sign').click()
    page.wait_for_function("document.getElementById('status').textContent==='Prediction ready.'")
    assert page.locator('#letter').inner_text()=='C'
    page.locator('#file').set_input_files({'name':'bad.png','mimeType':'image/png','buffer':b'invalid'})
    page.get_by_role('button',name='Recognize sign').click()
    page.wait_for_function("document.getElementById('status').textContent.includes('valid PNG')")
    page.set_viewport_size({'width':390,'height':844})
    page.get_by_role('button',name='Load example').click()
    page.get_by_role('button',name='Recognize sign').click()
    page.wait_for_function("document.getElementById('status').textContent==='Prediction ready.'")
    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
    page.screenshot(path=str(ROOT/'docs/demo-mobile.png'),full_page=True)
    assert not errors,errors
    browser.close()
print('Browser checks passed: sample, upload, invalid image, mobile layout, no JavaScript errors.')

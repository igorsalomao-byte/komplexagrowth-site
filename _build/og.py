"""Gera assets/img/og.jpg (1200x630). Uso: python _build/og.py  (precisa do Chrome e do Pillow)."""
import io, os, sys, subprocess, tempfile
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import logo, ROOT

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
doc = f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Fraunces:ital,wght@1,400&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{background:#081525;color:#fff;font-family:Inter,sans-serif;position:relative}}
body::before{{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(ellipse 85% 80% at 60% 40%,#000 30%,transparent 85%)}}
body::after{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 50% 60% at 88% 18%,rgba(16,153,233,.3),transparent 70%),radial-gradient(ellipse 40% 50% at 0% 100%,rgba(22,112,195,.3),transparent 70%)}}
.w{{position:relative;z-index:2;height:100%;padding:64px 76px 60px;display:flex;flex-direction:column}}
.m{{display:flex;align-items:center;gap:14px}} .m svg{{width:46px}} .m span{{font-size:24px;letter-spacing:-.02em}} .m b{{font-weight:800}} .m i{{font-style:normal;opacity:.72;margin-left:6px}}
.o{{margin-top:auto;font-family:'JetBrains Mono',monospace;font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:#24D5FF}}
h1{{font-size:70px;font-weight:800;letter-spacing:-.045em;line-height:1.02;margin-top:20px;max-width:15ch}}
h1 em{{font-family:Fraunces,serif;font-style:italic;font-weight:400;background:linear-gradient(90deg,#1670C3,#1099E9 48%,#24D5FF);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
.r{{margin-top:30px;display:flex;align-items:center;gap:16px;font-size:17px;color:rgba(255,255,255,.7)}}
.r i{{width:90px;height:3px;border-radius:3px;background:linear-gradient(90deg,#1670C3,#1099E9 48%,#24D5FF)}}
</style></head><body><div class="w">
<div class="m">{logo('og')}<span><b>Komplexa</b><i>Growth</i></span></div>
<div class="o">Marketing e comercial para empresas de serviços</div>
<h1>Do anúncio à venda fechada, <em>numa operação só.</em></h1>
<div class="r"><i></i>komplexagrowth.com</div>
</div></body></html>'''

tmp = tempfile.mkdtemp()
hp = os.path.join(tmp, 'og.html'); png = os.path.join(tmp, 'og.png')
io.open(hp, 'w', encoding='utf-8').write(doc)
subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1200,630',
                '--virtual-time-budget=6000', f'--screenshot={png}', 'file:///' + hp.replace('\\', '/')], capture_output=True, timeout=90)
im = Image.open(png).convert('RGB')
assert im.size == (1200, 630), im.size
out = os.path.join(ROOT, 'assets', 'img', 'og.jpg')
im.save(out, 'JPEG', quality=86, optimize=True, progressive=True)
print('og.jpg', os.path.getsize(out) // 1024, 'KB')

"""sietehotel.com/menu/ sayfasını ana sayfadan (index.html) üretir.
Menü fiyatları index.html'de güncellendikten sonra bu betik yeniden çalıştırılır:
    python3 _tools/menu_sayfasi.py
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, 'bulunamadı: ' + old[:60]
    s = s.replace(old, new, count)

# görseller ve bağlantılar kökten çözülsün; başlıklar
rep('<head>', '<head>\n<base href="/">')
rep("<title>Siete Hotel Lara | Antalya Lara&#x27;da Butik Otel</title>", '<title>Menü · Siete Hotel Lara</title>')
rep('<link rel="canonical" href="https://www.sietehotel.com/">', '<link rel="canonical" href="https://www.sietehotel.com/menu/">')
rep('<meta property="og:url" content="https://www.sietehotel.com/">', '<meta property="og:url" content="https://www.sietehotel.com/menu/">')
rep("document.title=en?'Siete Hotel Lara · Boutique hotel in Lara, Antalya':tTR;", "document.title=en?'Menu · Siete Hotel Lara':tTR;")
# yalnız menü görünsün
rep('<body>', '<body class="menu-only">')
rep('id="menu" hidden', 'id="menu"')
rep('<button type="button" class="m-close" id="m-close">Menüyü kapat <span aria-hidden="true">✕</span></button>',
    '<a class="m-close" id="m-close-link" href="/" data-en="Hotel website">Otel sayfası</a><span id="m-close" hidden></span>')
CSS = '''
/* menü sayfası (sietehotel.com/menu) */
.menu-only main>*:not(.gastro){display:none!important}
.menu-only .gastro-grid{display:none!important}
.menu-only .gastro{padding-top:calc(var(--hdr-h,84px) + 12px);padding-bottom:40px}
.menu-only .menu{margin-top:0}
.menu-only a.m-close{text-decoration:none}
.menu-only .ftr-top{display:none}
'''
i = s.find('</style>')
s = s[:i] + CSS + s[i:]
# anket: bu sayfaya gelen herkes QR/menü ziyaretçisi sayılır; ana sayfaya yönlendirme yapılmaz
rep("fromQR=params.get('qr')==='menu'", "fromQR=true")
rep("if(fromQR||location.hash==='#menu')setTimeout(openMenuFromLink,300);", "")
# ana sayfadaki QR yönlendirmesi bu sayfada çalışmasın
s = s.replace("/*QR-YONLENDIR*/if(new URLSearchParams(location.search).get('qr')==='menu'||location.hash==='#menu'){location.replace('/menu/');}", '')

os.makedirs(os.path.join(ROOT, 'menu'), exist_ok=True)
open(os.path.join(ROOT, 'menu', 'index.html'), 'w', encoding='utf-8').write(s)
print('menu/index.html yazıldı', len(s))

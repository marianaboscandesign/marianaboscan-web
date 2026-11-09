#!/usr/bin/env python3
"""Lee el feed RSS de Behance y agrega a data/behance_nuevos.json los proyectos nuevos.
- Solo agrega proyectos posteriores a DESDE y que no estén ya en el sitio.
- Nunca sobrescribe una entrada existente: puedes editar a mano marca, descripción y categoría.
- Si Behance no responde, no hace nada y no rompe la publicación."""
import json, os, re, subprocess, sys, unicodedata, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

USUARIO = 'marianaboscan'
DESDE = '2026-11-01'                      # solo proyectos publicados desde esta fecha entran solos
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO = os.path.join(AQUI, 'data', 'behance_nuevos.json')
FEED = f'https://www.behance.net/feeds/user?username={USUARIO}'

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

KEY = re.compile(r'brand|identity|logo|web|ui|ux|design|social|packag|report|editorial|campaign|video|flyer|dise[ñn]o|manual', re.I)
def partir(titulo):
    p = [x.strip() for x in titulo.split('|')]
    if len(p) >= 2:
        a, b = p[0], ' | '.join(p[1:])
        if KEY.search(a) and not KEY.search(b): return b, a
        return a, b
    return titulo.strip(), ''

def categoria(t):
    t = t.lower()
    if re.search(r'packag|empaque', t): return 'packaging'
    if re.search(r'social|redes', t): return 'social'
    if re.search(r'video|campaign|campa', t): return 'video'
    if re.search(r'report|editorial|catalog|flyer|informe', t): return 'editorial'
    if re.search(r'web|ui\b|ux\b|landing|shopify', t): return 'web'
    return 'branding'

ES = [('Website & Brand Identity', 'Sitio web e identidad de marca'), ('Brand Identity', 'Identidad de marca'), ('Visual Identity', 'Identidad visual'),
      ('Web Design', 'Diseño web'), ('Social Media', 'Redes sociales'), ('Packaging Design', 'Diseño de empaques'), ('Logo Design', 'Diseño de logo'),
      ('Annual Report', 'Informe anual'), ('Brand Book', 'Manual de marca')]
def a_es(t):
    for en, es in ES: t = re.sub(en, es, t, flags=re.I)
    return t.replace(' & ', ' y ')

DIR_IMG = os.path.join(AQUI, 'data', 'imagenes')

def sacar_imagenes(pagina_url, timeout=60000):
    """Abre el proyecto en un navegador (Playwright) y devuelve [[url, alto%], ...] de las imágenes del proyecto."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('Instalando navegador (una sola vez por ejecución)…')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'playwright'], check=True)
        subprocess.run([sys.executable, '-m', 'playwright', 'install', '--with-deps', 'chromium'], check=True)
        from playwright.sync_api import sync_playwright
    js = r"""async () => {
        const html = document.documentElement.innerHTML.split('\\/').join('/').split('&amp;').join('&');
        const re = /https?:\/\/[^"'\s)\\]+\/project_modules\/[^"'\s)\\]+\.(?:png|jpe?g|webp|gif)/gi;
        const urls = [...new Set(html.match(re) || [])];
        const out = [];
        for (const u of urls) {
            const dim = await new Promise(r => { const im = new Image(); im.onload = () => r([im.naturalWidth, im.naturalHeight]); im.onerror = () => r(null); im.src = u; setTimeout(() => r(null), 8000); });
            if (dim && dim[0] >= 300) out.push([u, Math.round(dim[1] / dim[0] * 1000) / 10]);
        }
        return {titulo: document.title, urls: urls.length, imgs: out, muestra: urls.slice(0, 3)};
    }"""
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={'width': 1400, 'height': 900}, locale='en-US', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36')
        resp = pg.goto(pagina_url, timeout=timeout, wait_until='domcontentloaded')
        print('  Behance respondió:', resp.status if resp else '?', '| título:', pg.title()[:80])
        pg.wait_for_timeout(3000)
        alto = pg.evaluate('document.body.scrollHeight')
        for y in range(0, alto + 700, 600):
            pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(350)
            alto = max(alto, pg.evaluate('document.body.scrollHeight'))
        pg.wait_for_timeout(1500)
        res = pg.evaluate(js)
        print('  URLs de imágenes encontradas:', res['urls'], '| válidas:', len(res['imgs']), '| ejemplo:', res['muestra'])
        crudas = res['imgs']
        nav.close()
    vistas, salida = set(), []
    for u, pct in crudas:
        u = re.sub(r'project_modules/[^/]+/', 'project_modules/max_1200/', u)
        if u in vistas: continue
        vistas.add(u); salida.append([u, pct])
    return salida

def completar_imagenes(datos):
    """Para cada proyecto sin archivo de imágenes, intenta sacarlas de Behance. Si falla, se reintenta en la próxima ejecución."""
    os.makedirs(DIR_IMG, exist_ok=True)
    for d in datos:
        f = os.path.join(DIR_IMG, f"{d['id']}.json")
        if os.path.exists(f): continue
        try:
            imgs = sacar_imagenes(d['link'])
        except Exception as e:
            print('No se pudieron leer las imágenes de', d['marca'], '→', str(e)[:200]); continue
        if len(imgs) >= 2:
            json.dump({'imgs': imgs}, open(f, 'w', encoding='utf-8'), indent=1)
            print(f"Imágenes guardadas: {d['marca']} ({len(imgs)})")
        else:
            print('Behance no entregó imágenes para', d['marca'], '(se mantiene el enlace a Behance)')

def main():
    try:
        req = urllib.request.Request(FEED, headers={'User-Agent': 'Mozilla/5.0 (compatible; sitio-marianaboscan)'})
        xml = urllib.request.urlopen(req, timeout=30).read()
        items = ET.fromstring(xml).findall('./channel/item')
    except Exception as e:
        print('No se pudo leer el feed de Behance:', e); items = []
    datos = json.load(open(ARCHIVO, encoding='utf-8')) if os.path.exists(ARCHIVO) else []
    ids = {str(d['id']) for d in datos}
    sitio = {p['s'] for p in json.load(open(os.path.join(AQUI, 'data', 'proyectos.json'), encoding='utf-8'))['proyectos']}
    nuevos = 0
    for it in items:
        link = (it.findtext('link') or '').strip()
        m = re.search(r'/gallery/(\d+)/([^/?#]+)', link)
        if not m: continue
        pid, slug = m.group(1), m.group(2)
        if pid in ids or norm(slug) in sitio: continue
        try: fecha = parsedate_to_datetime(it.findtext('pubDate')).date().isoformat()
        except Exception: fecha = ''
        if fecha and fecha < DESDE: continue
        im = re.search(r"src='([^']+)'", it.findtext('description') or '')
        if not im: continue
        marca, desc = partir(it.findtext('title') or slug)
        datos.append(dict(id=pid, marca=marca, des=a_es(desc), den=desc, cat=categoria(marca + ' ' + desc), cover=im.group(1), link=link, fecha=fecha))
        nuevos += 1; print('Nuevo proyecto:', marca, '|', desc)
    if nuevos:
        json.dump(datos, open(ARCHIVO, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{nuevos} proyecto(s) nuevo(s).')
    completar_imagenes(datos)

if __name__ == '__main__':
    main()

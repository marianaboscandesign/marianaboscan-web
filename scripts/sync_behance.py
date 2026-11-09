#!/usr/bin/env python3
"""Lee el feed RSS de Behance y agrega a data/behance_nuevos.json los proyectos nuevos.
- Solo agrega proyectos posteriores a DESDE y que no estén ya en el sitio.
- Nunca sobrescribe una entrada existente: puedes editar a mano marca, descripción y categoría.
- Si Behance no responde, no hace nada y no rompe la publicación."""
import json, os, re, sys, unicodedata, urllib.request, xml.etree.ElementTree as ET
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

def main():
    try:
        req = urllib.request.Request(FEED, headers={'User-Agent': 'Mozilla/5.0 (compatible; sitio-marianaboscan)'})
        xml = urllib.request.urlopen(req, timeout=30).read()
        items = ET.fromstring(xml).findall('./channel/item')
    except Exception as e:
        print('No se pudo leer Behance (se deja todo como está):', e); return
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

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Genera el sitio bilingüe (ES en la raíz, EN en /en/) en ./dist
Uso:  python3 build.py
Edita los textos en CONTENIDO / UI más abajo y vuelve a ejecutarlo."""
import json, os, re, shutil, html, unicodedata
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(AQUI, os.environ.get('DIST', 'dist'))
PREVIEW = bool(os.environ.get('PREVIEW'))  # solo para ver el sitio en una vista previa sin servidor
SITIO = 'https://www.marianaboscan.com'          # dominio final (canonical, hreflang, sitemap)
ENDPOINT = os.environ.get('ENDPOINT', 'https://script.google.com/macros/s/AKfycbyPGrFhGQFpCaKIa1HACdf1oGdl0Xd4BDnkbMsJFDCkpSmVYo_t8LmkTzR0RAoNGSaRxw/exec')  # misma URL /exec del formulario de revisa-logo
MOSTRAR_SERVICIOS = False  # False = sitio de portafolio para reclutadores: sin servicios ni captación de clientes. True = vuelve todo.
FORM_LOGO = 'https://revisa.marianaboscan.com'
EMAIL = 'marianaboscandesign@gmail.com'
WHATSAPP = 'https://wa.me/573243591199'
REDES = [('TikTok', 'https://www.tiktok.com/@marianaboscandesign'),
         ('LinkedIn', 'https://www.linkedin.com/in/mariana-boscan/'),
         ('Behance', 'https://www.behance.net/marianaboscan')]

from servicios import SERVICIOS, ORDEN
from servicios_extra import EXTRA, PROMPTS, ESTILO
from briefs import BRIEFS
D = json.load(open(os.path.join(AQUI, 'data', 'proyectos.json'), encoding='utf-8'))
BASE = D['base']
# Proyectos nuevos leídos de Behance (los agrega scripts/sync_behance.py; se pueden editar a mano en data/behance_nuevos.json)
NUEVOS = []
_nf = os.path.join(AQUI, 'data', 'behance_nuevos.json')
def _norm(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')
if os.path.exists(_nf):
    NUEVOS = sorted(json.load(open(_nf, encoding='utf-8')), key=lambda e: e.get('fecha', ''), reverse=True)
def limpio(t):
    """Arregla textos con entidades HTML (&amp; → &) aunque vengan doblemente codificados."""
    for _ in range(4):
        u = html.unescape(t)
        if u == t: break
        t = u
    return t
def categorias_de(e):
    """Un proyecto puede estar en varias categorías: la principal (cat) más las que mencione su título."""
    if e.get('cats'): return list(e['cats'])
    t = (e['marca'] + ' ' + e.get('den', '') + ' ' + e.get('des', '')).lower()
    reglas = [('branding', r'brand|identity|identidad|logo|marca'), ('web', r'web|\bui\b|\bux\b|landing|shopify|sitio'),
              ('social', r'social|redes'), ('packaging', r'packag|empaque'), ('editorial', r'editorial|report|informe|catalog|flyer'),
              ('video', r'video|campaign|campa')]
    cs = [e.get('cat', 'branding')] + [c for c, rx in reglas if re.search(rx, t)]
    return list(dict.fromkeys(c for c in cs if c in CATS))
for _e in NUEVOS:
    for _k in ('marca', 'des', 'den'): _e[_k] = limpio(_e.get(_k, ''))
    _m = re.search(r'/gallery/\d+/([^/?#]+)', _e['link'])
    _e['slug'] = _norm(_m.group(1)) if _m else 'proyecto-' + str(_e['id'])
    _e['clave'] = _norm(_e['marca'])      # las imágenes pueden llamarse por ID (258152879.json) o por marca (flick.json)
    for _n in (str(_e['id']), _e['clave']):
        _fi = os.path.join(AQUI, 'data', 'imagenes', _n + '.json')
        if os.path.exists(_fi):
            _e['imgs'] = json.load(open(_fi, encoding='utf-8')).get('imgs', []); break

# slug: (marca, descriptor ES, descriptor EN, categoría)
META = {
 'disidente-studio-brand-identity': ('Disidente Studio', 'Identidad de marca', 'Brand identity', 'branding'),
 'edunova-web-design-ui': ('edunova', 'Diseño web y UI', 'Web design & UI', 'web'),
 'diseno-de-social-media-martinsburg-college': ('Martinsburg College', 'Diseño de social media', 'Social media design', 'social'),
 'chontadooroh-republic-packaging-design': ('Chontadooroh Republic', 'Diseño de empaques', 'Packaging design', 'packaging'),
 'diseno-de-logo-nevato': ('Nevato', 'Diseño de logo', 'Logo design', 'branding'),
 'huba-kindergarten-visual-identity-ad-design': ('Huba Kindergarten', 'Identidad visual y piezas publicitarias', 'Visual identity & ad design', 'branding'),
 'centro-comercial-andino-annual-report-video': ('Centro Comercial Andino', 'Video de informe anual', 'Annual report video', 'video'),
 'centro-comercial-andino-christmas-social-media': ('Centro Comercial Andino', 'Social media navideño', 'Christmas social media', 'social'),
 'kosmos-peru-logo-visual-identity': ('Kosmos Perú', 'Logo e identidad visual', 'Logo & visual identity', 'branding'),
 'usphysique-brand-book': ('USPHYSIQUE', 'Manual de marca', 'Brand book', 'branding'),
 'campana-papa-merece-lo-mejor-centro-comercial-andino': ('Centro Comercial Andino', 'Campaña «Papá merece lo mejor»', '“Dad deserves the best” campaign', 'video'),
 'rcn-radio-rate-card-editorial-tarifario-2022': ('RCN Radio', 'Rate card editorial (Tarifario 2022)', 'Editorial rate card (2022)', 'editorial'),
 'empresa-de-energia-putumayo-annual-report': ('Empresa de Energía Putumayo', 'Informe anual', 'Annual report', 'editorial'),
 'spa-magical-hands-brand-identity': ('Spa Magical Hands', 'Identidad de marca', 'Brand identity', 'branding'),
 'centro-comercial-andino-top-sale-campaign': ('Centro Comercial Andino', 'Campaña Top Sale', 'Top Sale campaign', 'video'),
 'livewire-visual-identity': ('Livewire', 'Identidad visual', 'Visual identity', 'branding'),
 'ula-flyer': ('ULA', 'Flyer', 'Flyer', 'editorial'),
}
REDES_ICO = [('TikTok', REDES[0][1], 'tiktok'), ('LinkedIn', REDES[1][1], 'linkedin'), ('Behance', REDES[2][1], 'behance'),
             ('WhatsApp', WHATSAPP, 'whatsapp'), ('Email', 'mailto:' + EMAIL, 'correo')]
HOME_NUEVOS = 3   # cuántos proyectos nuevos de Behance se muestran primero en el home
DESTACADOS = ['disidente-studio-brand-identity', 'usphysique-brand-book', 'edunova-web-design-ui',
              'chontadooroh-republic-packaging-design', 'spa-magical-hands-brand-identity', 'huba-kindergarten-visual-identity-ad-design']
CATS = {'branding': ('Branding', 'Branding'), 'web': ('Web', 'Web'), 'social': ('Social media', 'Social media'),
        'editorial': ('Editorial', 'Editorial'), 'packaging': ('Empaques', 'Packaging'), 'video': ('Video y campañas', 'Video & campaigns')}

# páginas: clave -> (ruta ES, ruta EN)
# inglés en la raíz (idioma por defecto), español bajo /es/
RUTAS = {'inicio': ('es/', ''), 'servicios': ('es/servicios/', 'services/'), 'portafolio': ('es/portafolio/', 'work/'), 'sobre': ('es/sobre-mi/', 'about/'), 'contacto': ('es/contacto/', 'contact/')}
# direcciones antiguas del portafolio de Adobe -> redirección a las nuevas
REDIRECCIONES = {'bio-2/': 'about/'}

UI = {
 'es': dict(lang='es', nav={'inicio': 'Inicio', 'servicios': 'Servicios', 'portafolio': 'Portafolio', 'sobre': 'Sobre mí', 'contacto': 'Contacto'},
  otro='EN', otro_nombre='English', skip='Saltar al contenido', menu='Navegación principal',
  titulo_sitio='Diseñadora gráfica senior en Colombia | Mariana Boscán',
  desc_sitio='Diseñadora gráfica senior en Bogotá, Colombia, con más de 8 años de experiencia. Branding y logos, tiendas online en Shopify, redes sociales, diseño web, diseño editorial y miniaturas de YouTube.',
  h1=('Mariana ', 'Boscán'), lead='Diseñadora gráfica senior con enfoque estratégico en branding, experiencias digitales y comunicación visual.',
  servicios=['Branding', 'Social media', 'Packaging', 'Editorial', 'Diseño web', 'Video'],
  foto_alt='Retrato de Mariana Boscán', idioma_aria='Cambiar idioma', tema_aria='Cambiar entre modo claro y oscuro',
  ver_portafolio='Ver portafolio', escribeme='Escríbeme', destacados='Proyectos destacados', ver_todos='Ver todos los proyectos',
  sobre_et='Sobre mí', sobre_h2='Creatividad y funcionalidad para marcas en lo digital',
  sobre_resumen='Más de 8 años creando experiencias de marca estratégicas, con sistemas visuales sólidos y comunicación clara.',
  leer_mas='Conocer más', cta_logo_et='Herramienta gratuita', cta_logo_h2='¿Tu logo pasa la prueba?', cta_logo_p='Sube tu logo y recibe en tu correo un reporte gratis: qué cumple, qué no y qué cambiar primero.', cta_logo_btn='Revisar mi logo',
  port_h1=('Mi ', 'portafolio'), port_lead='Identidades de marca, social media, empaques, piezas editoriales, web y video.', todos='Todos', proyectos_n='proyectos',
  sobre_h1=('Hola, soy ', 'Mariana'), sobre_p=[
   'Diseñadora gráfica senior con más de 8 años de experiencia en branding, identidad visual, diseño digital, diseño web y comunicación de marketing.',
   'Creo experiencias de marca coherentes en puntos de contacto digitales e impresos: sitios web, tiendas online, landing pages, campañas en redes sociales y piezas editoriales. Trabajo con equipos internacionales y multidisciplinarios, apoyando sistemas de diseño, flujos creativos y consistencia de marca, con un enfoque estratégico y atento al detalle.',
   'Me interesa especialmente la intersección entre diseño, tipografía, accesibilidad y narrativa: crear trabajo que no solo se ve bien, sino que comunica con propósito.',
   'El diseño accesible es parte de mi forma de trabajar: cuido el contraste, la legibilidad y la claridad para que las piezas y los sitios web puedan leerse y usarse bien por cualquier persona.', 'Actualmente exploro cómo el diseño, la tecnología y la IA pueden ampliar la forma en que creamos y comunicamos.'],
  datos=[('Dónde', 'Bogotá, Colombia'), ('Formación', 'Licenciatura en Diseño Gráfico'), ('Experiencia', 'Más de 8 años'), ('Trabajo en', 'Branding · Editorial · Web · Tiendas online en Shopify · Social media')],
  exp_h='Experiencia', edu_h='Formación', tools_h='Herramientas y plataformas', skills_h='Habilidades', presente='Presente',
  contacto_h1=('Hablemos de tu ', 'proyecto'), contacto_lead='Cuéntame qué necesitas y te respondo lo antes posible.',
  f_nombre='Nombre', f_email='Correo', f_tel='Teléfono (opcional)', f_origen='¿Cómo supiste de mí?', f_origen_ph='Selecciona una opción', f_origenes=[('google', 'En Google'), ('linkedin', 'En LinkedIn'), ('tiktok', 'En TikTok'), ('behance', 'En Behance'), ('recomendacion', 'Por recomendación'), ('otro', 'Otro')], f_mensaje='Mensaje', f_enviar='Enviar mensaje', f_enviando='Enviando…',
  f_ok='¡Gracias! Recibí tu mensaje y te respondo pronto.', f_err='No pude enviar el mensaje. Escríbeme directamente por correo o WhatsApp.', f_inv='Revisa que el nombre, el correo y el mensaje estén completos.',
  f_lim='Has enviado varios mensajes seguidos. Intenta de nuevo más tarde o escríbeme por WhatsApp.',
  f_priv='Uso tus datos solo para responderte. Si quieres que los borre, escríbeme.',
  otras_vias='O escríbeme directo', whatsapp='WhatsApp', correo='Correo',
  anterior='Anterior', siguiente='Siguiente', volver='Volver al portafolio', ver_behance='Ver más en Behance',
  pie='Diseñadora gráfica senior · Bogotá, Colombia', derechos='Todos los derechos reservados', cat_nombre='Categoría', og_locale='es_CO'),
 'en': dict(lang='en', nav={'inicio': 'Home', 'servicios': 'Services', 'portafolio': 'Work', 'sobre': 'About', 'contacto': 'Contact'},
  otro='ES', otro_nombre='Español', skip='Skip to content', menu='Main navigation',
  titulo_sitio='Senior Graphic Designer in Colombia | Mariana Boscán',
  desc_sitio='Senior graphic designer in Bogotá, Colombia, with 8+ years of experience. Branding and logos, Shopify online stores, social media, web design, editorial design and YouTube thumbnails.',
  h1=('Mariana ', 'Boscán'), lead='Senior graphic designer with a strategic focus on branding, digital experiences and visual communication.',
  servicios=['Branding', 'Social media', 'Packaging', 'Editorial', 'Web design', 'Video'],
  foto_alt='Portrait of Mariana Boscán', idioma_aria='Change language', tema_aria='Switch between light and dark mode',
  ver_portafolio='View work', escribeme='Get in touch', destacados='Selected work', ver_todos='See all projects',
  sobre_et='About', sobre_h2='Creativity and function for brands in the digital world',
  sobre_resumen='8+ years creating strategic brand experiences, with strong visual systems and clear communication.',
  leer_mas='Learn more', cta_logo_et='Free tool', cta_logo_h2='Does your logo pass the test?', cta_logo_p='Upload your logo and get a free report by email: what works, what doesn’t and what to fix first.', cta_logo_btn='Review my logo',
  port_h1=('My ', 'work'), port_lead='Brand identities, social media, packaging, editorial pieces, web and video.', todos='All', proyectos_n='projects',
  sobre_h1=('Hi, I’m ', 'Mariana'), sobre_p=[
   'Senior Graphic Designer with 8+ years of experience in branding, visual identity, digital design, web design and marketing communications.',
   'I create cohesive brand experiences across digital and print touchpoints: websites, e-commerce platforms, landing pages, social media campaigns and editorial materials. I collaborate with cross-functional, international teams, supporting design systems, creative workflows and brand consistency, with a strategic, detail-oriented approach.',
   'I’m especially interested in the intersection of design, typography, accessibility, and storytelling—creating work that not only looks good, but communicates with purpose.',
   'Accessible design is part of how I work: I care about contrast, legibility and clarity so that pieces and websites can be read and used well by everyone.', 'Currently exploring how design, technology, and AI can expand the way we create and communicate.'],
  datos=[('Based in', 'Bogotá, Colombia'), ('Education', 'Degree in Graphic Design'), ('Experience', '8+ years'), ('Work in', 'Branding · Editorial · Web · Online stores on Shopify · Social media')],
  exp_h='Experience', edu_h='Education', tools_h='Tools & platforms', skills_h='Core skills', presente='Present',
  contacto_h1=('Let’s talk about your ', 'project'), contacto_lead='Tell me what you need and I’ll get back to you as soon as I can.',
  f_nombre='Name', f_email='Email', f_tel='Phone (optional)', f_origen='How did you hear about me?', f_origen_ph='Select an option', f_origenes=[('google', 'On Google'), ('linkedin', 'On LinkedIn'), ('tiktok', 'On TikTok'), ('behance', 'On Behance'), ('recomendacion', 'Referral'), ('otro', 'Other')], f_mensaje='Message', f_enviar='Send message', f_enviando='Sending…',
  f_ok='Thank you! I got your message and I’ll reply soon.', f_err='I couldn’t send the message. Please email or WhatsApp me directly.', f_inv='Please fill in your name, a valid email and a message.',
  f_lim='You’ve sent several messages in a row. Try again later or message me on WhatsApp.',
  f_priv='I only use your details to reply to you. If you’d like them deleted, just let me know.',
  otras_vias='Or reach me directly', whatsapp='WhatsApp', correo='Email',
  anterior='Previous', siguiente='Next', volver='Back to work', ver_behance='More on Behance',
  pie='Senior graphic designer · Bogotá, Colombia', derechos='All rights reserved', cat_nombre='Category', og_locale='en_US'),
}


def esc(s): return html.escape(s, quote=True)


def ruta(clave, lang):
    return RUTAS[clave][0 if lang == 'es' else 1]


def rel(desde, hacia):
    """ruta relativa entre dos rutas del sitio (carpetas terminadas en /)"""
    d = os.path.relpath(hacia.rstrip('/') or '.', desde.rstrip('/') or '.')
    if hacia.endswith('/') or hacia == '':
        d = (d if d != '.' else '') + ('/' if d != '.' else '')
    return d if d else './'


def url_abs(path): return SITIO + '/' + path


def h1_html(par, fin=''):
    pre, serif = par
    return f'{esc(pre)}<span class="serif">{esc(serif)}</span>{esc(fin)}'


def proy_ruta(slug, lang): return 'es/' + slug + '/' if lang == 'es' else slug + '/'





ICONOS_RELLENOS = {'behance': ('0 0 511.958 511.958', '<g> <g> <g> <path d="M210.624,240.619c10.624-5.344,18.656-11.296,24.16-17.728c9.792-11.584,14.624-26.944,14.624-45.984 c0-18.528-4.832-34.368-14.496-47.648c-16.128-21.632-43.424-32.704-82.016-33.28H0v312.096h142.56 c16.064,0,30.944-1.376,44.704-4.192c13.76-2.848,25.664-8.064,35.744-15.68c8.96-6.624,16.448-14.848,22.4-24.544 c9.408-14.656,14.112-31.264,14.112-49.76c0-17.92-4.128-33.184-12.32-45.728C238.912,255.627,226.752,246.443,210.624,240.619z M63.072,150.187h68.864c15.136,0,27.616,1.632,37.408,4.864c11.328,4.704,16.992,14.272,16.992,28.864 c0,13.088-4.32,22.24-12.864,27.392c-8.608,5.152-19.776,7.744-33.472,7.744H63.072V150.187z M171.968,348.427 c-7.616,3.68-18.336,5.504-32.064,5.504H63.072v-83.232h77.888c13.568,0.096,24.128,1.888,31.68,5.248 c13.44,6.08,20.128,17.216,20.128,33.504C192.768,328.651,185.856,341.579,171.968,348.427z"/> <rect x="327.168" y="110.539" width="135.584" height="38.848"/> <path d="M509.856,263.851c-2.816-18.08-9.024-33.984-18.688-47.712c-10.592-15.552-24.032-26.944-40.384-34.144 c-16.288-7.232-34.624-10.848-55.04-10.816c-34.272,0-62.112,10.72-83.648,32c-21.472,21.344-32.224,52.032-32.224,92.032 c0,42.656,11.872,73.472,35.744,92.384c23.776,18.944,51.232,28.384,82.4,28.384c37.728,0,67.072-11.232,88.032-33.632 c13.408-14.144,20.992-28.064,22.656-41.728H446.24c-3.616,6.752-7.808,12.032-12.608,15.872 c-8.704,7.04-20.032,10.56-33.92,10.56c-13.216,0-24.416-2.912-33.76-8.704c-15.424-9.28-23.488-25.536-24.512-48.672h170.464 C512.16,289.739,511.52,274.411,509.856,263.851z M342.976,269.835c2.24-15.008,7.68-26.912,16.32-35.712 c8.64-8.768,20.864-13.184,36.512-13.216c14.432,0,26.496,4.128,36.32,12.416c9.696,8.352,15.168,20.48,16.288,36.512H342.976z" /> </g> </g> </g>'), 'linkedin': ('0 0 100 100', '<g><path d="m90 90v-29.3c0-14.4-3.1-25.4-19.9-25.4-8.1 0-13.5 4.4-15.7 8.6h-.2v-7.3h-15.9v53.4h16.6v-26.5c0-7 1.3-13.7 9.9-13.7 8.5 0 8.6 7.9 8.6 14.1v26h16.6z"/><path d="m11.3 36.6h16.6v53.4h-16.6z"/><path d="m19.6 10c-5.3 0-9.6 4.3-9.6 9.6s4.3 9.7 9.6 9.7 9.6-4.4 9.6-9.7-4.3-9.6-9.6-9.6z"/></g>'), 'tiktok': ('0 0 512 512', '<g><path d="m480.32 128.39c-29.22 0-56.18-9.68-77.83-26.01-24.83-18.72-42.67-46.18-48.97-77.83-1.56-7.82-2.4-15.89-2.48-24.16h-83.47v228.08l-.1 124.93c0 33.4-21.75 61.72-51.9 71.68-8.75 2.89-18.2 4.26-28.04 3.72-12.56-.69-24.33-4.48-34.56-10.6-21.77-13.02-36.53-36.64-36.93-63.66-.63-42.23 33.51-76.66 75.71-76.66 8.33 0 16.33 1.36 23.82 3.83v-62.34-22.41c-7.9-1.17-15.94-1.78-24.07-1.78-46.19 0-89.39 19.2-120.27 53.79-23.34 26.14-37.34 59.49-39.5 94.46-2.83 45.94 13.98 89.61 46.58 121.83 4.79 4.73 9.82 9.12 15.08 13.17 27.95 21.51 62.12 33.17 98.11 33.17 8.13 0 16.17-.6 24.07-1.77 33.62-4.98 64.64-20.37 89.12-44.57 30.08-29.73 46.7-69.2 46.88-111.21l-.43-186.56c14.35 11.07 30.04 20.23 46.88 27.34 26.19 11.05 53.96 16.65 82.54 16.64v-60.61-22.49c.02.02-.22.02-.24.02z"/></g>'), 'whatsapp': ('0 0 32 32', '<g><path d="m16 1c-8.2709961 0-15 6.7285156-15 15 0 2.9101563.8344727 5.7158203 2.418457 8.1523438l-2.3374023 5.4541016c-.1611328.375-.0771484.8115234.2119141 1.1005859.1914062.1914062.4472656.2929687.7070312.2929687.1328125 0 .2670898-.0263672.394043-.0810547l5.4541016-2.3378906c2.4360351 1.5849609 5.2416992 2.4189453 8.1518554 2.4189453 8.2714844 0 15-6.7285156 15-15s-6.7285156-15-15-15zm7.6992188 20.3691406s-1.2470703 1.5996094-2.1484375 1.9736328c-2.2910156.9482422-5.5253906 0-9.2099609-3.6835938-3.6835938-3.6845703-4.6323242-6.9189453-3.6835938-9.2099609.3740234-.9023437 1.9736328-2.1484374 1.9736328-2.1484374.4335938-.3378906 1.1074219-.2958984 1.4960938.0927734l1.8095703 1.8095703c.3886719.3886719.3886719 1.0253906 0 1.4140625l-1.1357422 1.1347656s-.4599609 1.3808594 2.3027344 4.1445313c2.7626953 2.7626953 4.1445313 2.3027344 4.1445313 2.3027344l1.1347656-1.1357422c.3886719-.3886719 1.0253906-.3886719 1.4140625 0l1.8095703 1.8095703c.3886718.3886719.430664 1.0615234.0927734 1.4960937z"/></g>'), 'correo': ('0 0 24 24', '<path d="m12 16c-.6 0-1.1-.2-1.6-.4l-8.4-5.2v6.6c0 1.7 1.3 3 3 3h14c1.7 0 3-1.3 3-3v-6.6l-8.4 5.2c-.5.2-1 .4-1.6.4zm7-12h-14c-1.7 0-3 1.3-3 3v1.1l9.5 5.8c.3.2.7.2 1 0l9.5-5.8v-1.1c0-1.7-1.3-3-3-3z"/>')}
ICONOS_RELLENOS.update({'sv_tiendas': ('0 0 512 512', '<g><path d="m451.95 0h-391.9c-33.112 0-60.05 26.938-60.05 60.05v391.9c0 33.112 26.938 60.05 60.05 60.05h391.9c33.112 0 60.05-26.938 60.05-60.05v-391.9c0-33.112-26.938-60.05-60.05-60.05zm-391.9 30h391.9c16.57 0 30.05 13.48 30.05 30.05v59.95h-452v-59.95c0-16.57 13.48-30.05 30.05-30.05zm391.9 452h-391.9c-16.57 0-30.05-13.48-30.05-30.05v-301.95h452v301.95c0 16.57-13.48 30.05-30.05 30.05z"/><path d="m195 90h242c8.284 0 15-6.716 15-15s-6.716-15-15-15h-242c-8.284 0-15 6.716-15 15s6.716 15 15 15z"/><circle cx="75" cy="75" r="15"/><circle cx="135" cy="75" r="15"/><path d="m352.267 232.163h-187.854l-9.725-40.653c-1.512-6.609-7.809-11.578-14.588-11.51h-56.71c-8.284 0-15 6.716-15 15s6.716 15 15 15h44.875l40.868 169.773c-5.768 7.565-9.203 17.001-9.203 27.227 0 24.813 20.187 45 45 45s45-20.187 45-45c0-5.266-.917-10.319-2.587-15.02h56.174c-1.669 4.7-2.587 9.754-2.587 15.02 0 24.813 20.187 45 45 45s45-20.187 45-45c0-12.739-5.329-24.249-13.865-32.444l24.09-75.47c5.036-15.778 2.322-32.501-7.448-45.876-9.772-13.376-24.876-21.047-41.44-21.047zm0 30c6.881 0 13.155 3.187 17.214 8.743s5.187 12.502 3.094 19.057l-22.988 72.018h-153.896l-18.476-76.293c-.003-.013-.004-.025-.007-.038l-5.618-23.486h180.677zm-147.338 159.837c-8.271 0-15-6.729-15-15s6.729-15 15-15 15 6.729 15 15-6.729 15-15 15zm141 0c-8.271 0-15-6.729-15-15s6.729-15 15-15 15 6.729 15 15-6.729 15-15 15z"/></g>'), 'sv_social': ('0 0 512 512', '<g><path d="m467 0h-422c-24.813 0-45 20.187-45 45v422c0 24.813 20.187 45 45 45h422c24.813 0 45-20.187 45-45 0-13.309 0-408.659 0-422 0-24.813-20.187-45-45-45zm-437 45c0-8.271 6.729-15 15-15h422c8.271 0 15 6.729 15 15v20h-452zm452 422c0 8.271-6.729 15-15 15h-422c-8.271 0-15-6.729-15-15v-372h452z"/><path d="m104 383h304c8.284 0 15-6.716 15-15v-224c0-8.284-6.716-15-15-15h-304c-8.284 0-15 6.716-15 15v224c0 8.284 6.716 15 15 15zm15-30v-26.364l73.191-66.538 53.932 47.19c5.942 5.199 14.899 4.901 20.484-.683l76.751-76.751 49.642 55.849v67.297zm274-194v81.547l-37.789-42.513c-5.656-6.363-15.637-6.825-21.817-.641l-78.077 78.077-53.439-46.76c-5.737-5.021-14.327-4.938-19.967.189l-62.911 57.193v-127.092z"/><path d="m232 417h-32c-8.284 0-15 6.716-15 15s6.716 15 15 15h32c8.284 0 15-6.716 15-15s-6.716-15-15-15z"/><path d="m328 417h-32c-8.284 0-15 6.716-15 15s6.716 15 15 15h32c8.284 0 15-6.716 15-15s-6.716-15-15-15z"/><path d="m125.394 413.394-5.394 5.393-5.394-5.394c-5.857-5.857-15.355-5.857-21.213 0s-5.858 15.355 0 21.213l16 16c5.858 5.858 15.355 5.858 21.213 0l16-16c5.858-5.857 5.858-15.355 0-21.213-5.857-5.857-15.355-5.857-21.212.001z"/></g>'), 'sv_branding': ('0 0 512 512', '<g><path d="m497 0h-482c-8.284 0-15 6.716-15 15v482c0 8.284 6.716 15 15 15h482c8.284 0 15-6.716 15-15v-482c0-8.284-6.716-15-15-15zm-15 59.999h-30v-29.999h30zm-60-29.999v29.999h-30v-29.999zm-60 0v29.999h-332v-29.999zm-332 452v-392h452v392z"/><path d="m437 120h-60c-8.284 0-15 6.716-15 15v15h-212v-15c0-8.284-6.716-15-15-15h-60c-8.284 0-15 6.716-15 15v60c0 8.284 6.716 15 15 15h15v152h-15c-8.284 0-15 6.716-15 15v60c0 8.284 6.716 15 15 15h60c8.284 0 15-6.716 15-15v-15h212v15c0 8.284 6.716 15 15 15h60c8.284 0 15-6.716 15-15v-60c0-8.284-6.716-15-15-15h-15v-152h15c8.284 0 15-6.716 15-15v-60c0-8.284-6.716-15-15-15zm-45 30h30v30h-30zm-302 0h30v30h-30zm30 272h-30v-30h30zm302 0h-30v-30h30zm-30-60h-15c-8.284 0-15 6.716-15 15v15h-212v-15c0-8.284-6.716-15-15-15h-15v-152h15c8.284 0 15-6.716 15-15v-15h212v15c0 8.284 6.716 15 15 15h15z"/><path d="m331.651 255.285-40.67-10.203-22.271-35.527c-2.743-4.375-7.544-7.032-12.709-7.032s-9.966 2.657-12.709 7.032l-22.272 35.526-40.669 10.204c-5.009 1.257-9.02 5.002-10.616 9.913-1.596 4.912-.553 10.3 2.761 14.261l26.905 32.16-2.863 41.832c-.353 5.152 1.97 10.124 6.148 13.159 4.178 3.036 9.625 3.708 14.416 1.781l38.9-15.65 38.9 15.65c4.767 1.92 10.228 1.265 14.416-1.781 4.178-3.035 6.501-8.007 6.148-13.159l-2.864-41.832 26.905-32.16c7.107-8.202 2.717-21.717-7.856-24.174zm-45.933 41.713c-2.485 2.97-3.725 6.786-3.46 10.649l1.642 23.981c-33.992-13.301-21.865-13.259-55.8 0 2.138-36.488 5.876-24.847-17.243-53.068 35.443-9.286 25.381-2.026 45.143-32.798 19.783 30.839 9.77 23.512 45.143 32.798z"/></g>'), 'sv_editorial': ('0 0 512 512', '<g><path d="m487.001 62.13h-131.445v-47.13c0-8.284-6.716-15-15-15h-315.557c-8.284 0-15 6.716-15 15v440.58c0 8.284 6.716 15 15 15h131.446v26.42c0 8.284 6.716 15 15 15h315.557c8.284 0 15-6.716 15-15v-419.87c-.001-8.284-6.717-15-15.001-15zm-231.231 0 69.786-25.638v25.638zm-215.771 378.45v-410.58h216.231l-89.958 33.05c-5.903 2.169-9.827 7.791-9.827 14.08v363.45zm432.002 41.42h-285.556v-389.87h285.557v389.87z"/><path d="m359.225 242.062h66.174c8.284 0 15-6.716 15-15v-60.004c0-8.284-6.716-15-15-15h-66.174c-8.284 0-15 6.716-15 15v60.004c0 8.284 6.716 15 15 15zm15-60.004h36.174v30.004h-36.174z"/><path d="m233.047 242.062h66.174c8.284 0 15-6.716 15-15s-6.716-15-15-15h-66.174c-8.284 0-15 6.716-15 15s6.716 15 15 15z"/><path d="m233.047 182.058h66.174c8.284 0 15-6.716 15-15s-6.716-15-15-15h-66.174c-8.284 0-15 6.716-15 15s6.716 15 15 15z"/><path d="m233.047 302.064h192.352c8.284 0 15-6.716 15-15s-6.716-15-15-15h-192.352c-8.284 0-15 6.716-15 15s6.716 15 15 15z"/><path d="m233.047 362.068h192.352c8.284 0 15-6.716 15-15s-6.716-15-15-15h-192.352c-8.284 0-15 6.716-15 15s6.716 15 15 15z"/><path d="m233.047 422.072h192.352c8.284 0 15-6.716 15-15s-6.716-15-15-15h-192.352c-8.284 0-15 6.716-15 15s6.716 15 15 15z"/></g>'), 'sv_web': ('0 0 512 512', '<path d="m467 1h-422c-24.813 0-45 20.187-45 45v420c0 24.813 20.187 45 45 45h422c24.813 0 45-20.187 45-45v-420c0-24.813-20.187-45-45-45zm-422 30h422c8.271 0 15 6.729 15 15v75h-452v-75c0-8.271 6.729-15 15-15zm422 450h-422c-8.271 0-15-6.729-15-15v-315h452v315c0 8.271-6.729 15-15 15z"/><path d="m306.909 197.213c-7.614-3.263-16.433.264-19.696 7.878l-90 210c-3.264 7.614.264 16.433 7.878 19.696 7.617 3.264 16.434-.266 19.696-7.878l90-210c3.264-7.615-.264-16.433-7.878-19.696z"/><path d="m177.713 246.629c-5.176-6.469-14.617-7.517-21.083-2.342l-75 60c-7.499 5.997-7.504 17.424 0 23.426l75 60c6.469 5.176 15.91 4.126 21.083-2.342 5.175-6.469 4.127-15.909-2.343-21.083l-60.358-48.288 60.358-48.287c6.47-5.175 7.518-14.614 2.343-21.084z"/><path d="m430.37 304.287-75-60c-6.469-5.176-15.909-4.127-21.083 2.342-5.175 6.469-4.127 15.909 2.343 21.083l60.358 48.288-60.358 48.287c-6.47 5.175-7.518 14.614-2.343 21.083 5.182 6.476 14.623 7.512 21.083 2.342l75-60c7.499-5.997 7.504-17.423 0-23.425z"/><circle cx="76" cy="76" r="15"/><circle cx="136" cy="76" r="15"/><circle cx="196" cy="76" r="15"/><path d="m346 91h90c8.284 0 15-6.716 15-15s-6.716-15-15-15h-90c-8.284 0-15 6.716-15 15s6.716 15 15 15z"/>'), 'sv_youtube': ('0 0 32 32', '<g id="a1db7c25-445b-4d26-b5a5-e18c8136412f" data-name="Layer 15"><path d="m27 30h-22a3 3 0 0 1 -3-3v-14a3 3 0 0 1 3-3h22a3 3 0 0 1 3 3v14a3 3 0 0 1 -3 3zm-22-18a1 1 0 0 0 -1 1v14a1 1 0 0 0 1 1h22a1 1 0 0 0 1-1v-14a1 1 0 0 0 -1-1zm21-9a1 1 0 0 0 -1-1h-18a1 1 0 0 0 0 2h18a1 1 0 0 0 1-1zm2 4a1 1 0 0 0 -1-1h-22a1 1 0 0 0 0 2h22a1 1 0 0 0 1-1zm-16 18a1 1 0 0 1 -.53-.15 1 1 0 0 1 -.47-.85v-8a1 1 0 0 1 1.45-.89l8 4a1 1 0 0 1 0 1.78l-8 4a1 1 0 0 1 -.45.11zm1-7.38v4.76l4.76-2.38z"/></g>')})


def ico(nombre):
    if nombre in ICONOS_RELLENOS:
        vb, cuerpo = ICONOS_RELLENOS[nombre]
        return f'<svg class="ico fill" viewBox="{vb}" aria-hidden="true">{cuerpo}</svg>'
    d = {
     'tiktok': '<path d="M14 3.5v11a4 4 0 1 1-4-4"/><path d="M14 3.5c.4 2.6 2 4.3 5 4.6"/>',
     'linkedin': '<rect x="3.5" y="3.5" width="17" height="17" rx="3.5"/><path d="M8 10.5v6M8 7.6v.1M12 16.5v-6M12 13c0-1.6 1-2.6 2.5-2.6s2.5 1 2.5 2.6v3.5"/>',
     'behance': '<path d="M2.5 6.5h5a2.3 2.3 0 0 1 0 4.8h-5zM2.5 11.3h5.6a2.5 2.5 0 0 1 0 5.2H2.5zM2.5 6.5v10M14 7.5h6.5M13.5 14.2h7a3.5 3.5 0 1 0-1 2.5"/>',
     'whatsapp': '<path d="M3.5 20.5l1.4-4.3A8.5 8.5 0 1 1 8 19.3z"/><path d="M9 8.8c0 3.2 3 6.2 6.2 6.2l1.1-1.6-2.1-1-.9.9c-1-.4-2-1.4-2.4-2.4l.9-.9-1-2.1z"/>',
     'correo': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7.5 8 6 8-6"/>',
     'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 1 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
     'birrete': '<path d="m2.5 9.5 9.5-5 9.5 5-9.5 5z"/><path d="M6.5 11.8v4.2c1.4 1.5 3.3 2.2 5.5 2.2s4.1-.7 5.5-2.2v-4.2M21.5 9.5v6"/>',
     'maleta': '<rect x="3" y="7.5" width="18" height="12" rx="3"/><path d="M9 7.5V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1.5M3 13h18"/>',
     'capas': '<path d="m12 3.5 9 4.8-9 4.8-9-4.8z"/><path d="m3 12.5 9 4.8 9-4.8M3 16.8l9 4.7 9-4.7"/>',
     'flecha': '<path d="M5 12h14M13 6l6 6-6 6"/>',
     'estrella': '<path d="M12 3c.8 5 2.2 7.2 9 9-6.8 1.8-8.2 4-9 9-.8-5-2.2-7.2-9-9 6.8-1.8 8.2-4 9-9z"/>',
    }[nombre]
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{d}</svg>'


def pie(lang, aqui=''):
    t = UI[lang]
    serv = ''.join(f'<li><a href="{rel(aqui, ruta_serv(k, lang))}">{esc(SERVICIOS[k][lang]["nav"])}</a></li>' for k in ORDEN)
    redes = ''.join(f'<li><a class="red" href="{u}" target="_blank" rel="noopener" aria-label="{n}" title="{n}">{ico(i)}</a></li>' for n, u, i in REDES_ICO)
    return f'''<footer class="pie"><div class="wrap fila"><div><small>© {date.today().year} Mariana Boscán · {esc(t['derechos'])}<br>{esc(t['pie'])}</small></div>
<ul class="redes">{redes}</ul></div>
{f'<nav class="wrap pie-serv" aria-label="{esc(SERV_UI[lang]["servicios"])}"><ul>{serv}</ul></nav>' if MOSTRAR_SERVICIOS else ''}</footer>'''


SERV_UI = {
 'es': dict(h2='Servicios de diseño en Colombia y en todo el mundo', lead='Diseño gráfico para marcas y emprendedores de cualquier lugar: del logo a la tienda online.', ver='Ver servicio', incluye='Qué incluye', proceso='Cómo trabajo',
            faq='Preguntas frecuentes', rel='Proyectos relacionados', cta_h='¿Hablamos de tu proyecto?', cta_b='Contáctame ahora', inicio='Inicio', servicios='Servicios', otros='Otros servicios'),
 'en': dict(h2='Design services in Colombia and worldwide', lead='Graphic design for brands and entrepreneurs anywhere: from logo to online store.', ver='View service', incluye='What’s included', proceso='How I work',
            faq='Frequently asked questions', rel='Related projects', cta_h='Let’s talk about your project?', cta_b='Contact me now', inicio='Home', servicios='Services', otros='Other services'),
}


def ruta_serv(k, lang): return ('es/' if lang == 'es' else '') + SERVICIOS[k]['slug'][0 if lang == 'es' else 1] + '/'


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>\n'


def esquema_home(lang):
    t = UI[lang]; u = SITIO + '/' + ruta('inicio', lang)
    ofertas = [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': SERVICIOS[k][lang]['titulo'], 'url': url_abs(ruta_serv(k, lang))}} for k in ORDEN]
    return jsonld({'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': SITIO + '/#web', 'url': SITIO + '/', 'name': 'Mariana Boscán', 'inLanguage': ['es', 'en']},
        {'@type': 'Person', '@id': SITIO + '/#persona', 'name': 'Mariana Boscán', 'url': SITIO + '/', 'image': SITIO + '/img/og.jpg',
         'jobTitle': 'Design Team Lead · Diseñadora gráfica senior' if lang == 'es' else 'Design Team Lead · Senior Graphic Designer', 'email': EMAIL,
         'address': {'@type': 'PostalAddress', 'addressLocality': 'Bogotá', 'addressCountry': 'CO'},
         'sameAs': [REDES[0][1], REDES[1][1], REDES[2][1]],
         'knowsAbout': ['Branding', 'Identidad visual', 'Sistemas de diseño', 'Diseño web', 'UI', 'Diseño editorial', 'Diseño de redes sociales', 'Diseño accesible']},
        *([] if not MOSTRAR_SERVICIOS else [{'@type': 'ProfessionalService', '@id': SITIO + '/#servicio', 'name': 'Mariana Boscán — ' + ('Diseño gráfico' if lang == 'es' else 'Graphic design'), 'url': u,
         'image': SITIO + '/img/og.jpg', 'telephone': '+573243591199', 'email': EMAIL, 'founder': {'@id': SITIO + '/#persona'},
         'address': {'@type': 'PostalAddress', 'addressLocality': 'Bogotá', 'addressCountry': 'CO'},
         'areaServed': [{'@type': 'Country', 'name': 'Colombia'}, {'@type': 'Place', 'name': 'Worldwide'}], 'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': SERV_UI[lang]['h2'], 'itemListElement': ofertas}}])]})


def servicios_home(lang, aqui):
    t = UI[lang]; u = SERV_UI[lang]
    cards = ''.join(f'<a class="serv-card rev" style="--d:{i * .08:.2f}s" href="{rel(aqui, ruta_serv(k, lang))}">{ico2(SERVICIOS[k]["icono"])}<h3>{esc(SERVICIOS[k][lang]["nav"])}</h3><p>{esc(SERVICIOS[k][lang]["corto"])}</p><span class="mas">{esc(u["ver"])} {ico("flecha")}</span></a>'
                    for i, k in enumerate(ORDEN))
    return f'''<section class="pantalla fondo-suave" id="servicios" data-nombre="{esc(u['servicios'])}" data-nav="servicios"><div class="wrap"><div class="serv-cab rev"><h2>{esc(u['h2'])}</h2><p class="lead">{esc(u['lead'])}</p></div><div class="serv-grid">{cards}</div><p class="btns" style="margin-top:var(--e8)"><a class="btn" href="{rel(aqui, ruta('servicios', lang))}">{esc(u['todos'])} {ico('flecha')}</a></p></div></section>'''


SERV_UI['es'].update(todos='Ver todos los servicios', pag_h1=('Servicios de ', 'diseño'),
    pag_lead='Branding, tiendas online, redes sociales, diseño web, editorial y miniaturas de YouTube, para marcas de Colombia y de todo el mundo.',
    para='Ideal para', ent='Qué recibes', porque='Por qué trabajar conmigo', ver_proy='Ver proyectos', ir='Ver servicio',
    porque_items=[('Más de 8 años de experiencia', 'Diseño para marcas y equipos de Colombia, Estados Unidos y otros países.'), ('Estrategia antes que decoración', 'Cada decisión visual tiene una razón y se explica.'),
                  ('Diseño accesible', 'Cuido contraste, legibilidad y claridad para que todo se lea y se use bien.'), ('Proceso claro', 'Trabajamos por etapas y siempre sabes en qué punto estamos.')],
    proceso_gral=[('Cuéntame tu proyecto', 'Me escribes o llenas un brief y entiendo lo que necesitas.'), ('Propuesta', 'Te envío alcance, entregables y tiempos.'), ('Diseño', 'Trabajo por etapas, con revisiones claras.'), ('Entrega', 'Recibes tus archivos listos para usar.')],
    proceso_h='Así trabajamos juntos', cta_p='Cuéntame qué necesitas y te respondo lo antes posible.', wa='Escribir por WhatsApp')
SERV_UI['en'].update(todos='See all services', pag_h1=('Design ', 'services'),
    pag_lead='Branding, online stores, social media, web design, editorial and YouTube thumbnails, for brands in Colombia and around the world.',
    para='Ideal for', ent='What you get', porque='Why work with me', ver_proy='See projects', ir='View service',
    porque_items=[('8+ years of experience', 'Design for brands and teams in Colombia, the United States and beyond.'), ('Strategy before decoration', 'Every visual decision has a reason and gets explained.'),
                  ('Accessible design', 'I care about contrast, legibility and clarity so everything reads and works well.'), ('A clear process', 'We work in stages and you always know where we are.')],
    proceso_gral=[('Tell me about your project', 'You write to me or fill in a brief and I understand what you need.'), ('Proposal', 'I send you scope, deliverables and timing.'), ('Design', 'I work in stages with clear reviews.'), ('Delivery', 'You receive your files ready to use.')],
    proceso_h='How we work together', cta_p='Tell me what you need and I’ll get back to you as soon as I can.', wa='Message on WhatsApp')

SERV_IMG_DIR = os.path.join(AQUI, 'src', 'img', 'servicios')


def serv_img(k, tipo, aqui, alt, lazy=True):
    for ext in ('webp', 'jpg', 'jpeg', 'png'):
        f = f'{k}-{tipo}.{ext}'
        if os.path.exists(os.path.join(SERV_IMG_DIR, f)):
            return f'<img src="{rel(aqui, "img/servicios/")}{f}" alt="{esc(alt)}" decoding="async"{" loading=lazy" if lazy else " fetchpriority=high"}>'
    return ''


def WA_BTN(u):
    return f'<a class="btn" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("whatsapp")} {esc(u["wa"])}</a>' 


def botones_contacto(lang):
    et = {'es': ('Escríbeme por correo', 'LinkedIn', 'WhatsApp'), 'en': ('Email me', 'Connect on LinkedIn', 'WhatsApp')}[lang]
    return (f'<a class="btn primario" href="mailto:{EMAIL}">{ico("correo")} {esc(et[0])}</a>'
            f'<a class="btn" href="{REDES[1][1]}" target="_blank" rel="noopener">{ico("linkedin")} {esc(et[1])}</a>'
            f'<a class="btn" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("whatsapp")} {esc(et[2])}</a>')


def btn_contacto(lang, aqui, texto=None, primario=True):
    u = SERV_UI[lang]
    return f'<a class="btn{" primario" if primario else ""}" href="{rel(aqui, ruta("contacto", lang))}">{esc(texto or u["cta_b"])} {ico("flecha")}</a>'


def cta_final(lang, aqui, k=None):
    u = SERV_UI[lang]
    otros = ''
    if k:
        otros = f'<p class="otros-t">{esc(u["otros"])}</p><ul class="otros">' + ''.join(f'<li><a class="btn" href="{rel(aqui, ruta_serv(o, lang))}">{esc(SERVICIOS[o][lang]["nav"])}</a></li>' for o in ORDEN if o != k) + '</ul>'
    return f'''<section class="wrap seccion"><div class="panel cta-final rev"><h2>{esc(u['cta_h'])}</h2><p class="lead">{esc(u['cta_p'])}</p><div class="btns">{botones_contacto(lang)}</div>{otros}</div></section>'''


def pagina_servicio(k, lang):
    S = SERVICIOS[k]; c = S[lang]; u = SERV_UI[lang]; x = EXTRA[k][lang]; aqui = ruta_serv(k, lang)
    sv = rel(aqui, ruta('servicios', lang)); home = rel(aqui, ruta('inicio', lang))
    vis = serv_img(k, 'hero', aqui, c['titulo'], lazy=False) or f'<span class="sv-ico">{ico2(S["icono"])}</span>'
    banda_img = serv_img(k, 'banda', aqui, x['frase'])
    inc = ''.join(f'<li class="rev" style="--d:{i * .05:.2f}s"><span class="ok" aria-hidden="true"></span><p>{esc(t_)}</p></li>' for i, t_ in enumerate(c['incluye']))
    para = ''.join(f'<li class="rev" style="--d:{i * .08:.2f}s"><span class="n">{i + 1:02d}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(x['para']))
    pasos = ''.join(f'<li class="rev" style="--d:{i * .08:.2f}s"><span class="n">{i + 1:02d}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(c['pasos']))
    ent = ''.join(f'<li>{esc(e)}</li>' for e in x['entregables'])
    porque = ''.join(f'<li class="rev" style="--d:{i * .08:.2f}s"><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(u['porque_items']))
    faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in c['faq'])
    ps = [p for p in D['proyectos'] if META[p['s']][3] == S['cat']][:3] if S['cat'] else []
    rel_html = ''.join(tarjeta(p, lang, aqui, i + 1) for i, p in enumerate(ps))
    bloque_rel = f'<section class="wrap seccion" id="proyectos"><div class="cab-sec"><h2>{esc(u["rel"])}</h2><a class="btn" href="{rel(aqui, ruta("portafolio", lang))}">{esc(u["ver_proy"])} {ico("flecha")}</a></div><ul class="rejilla">{rel_html}</ul></section>\n' if ps else ''
    banda = f'<section class="wrap seccion"><figure class="banda rev{" con-img" if banda_img else ""}">{banda_img}<blockquote>{esc(x["frase"])}</blockquote></figure></section>'
    cuerpo = f'''<section class="serv-hero wrap"><div class="serv-hero-t"><nav class="migas" aria-label="breadcrumb"><a href="{home}">{esc(u['inicio'])}</a> <span>/</span> <a href="{sv}">{esc(u['servicios'])}</a> <span>/</span> <span>{esc(c['nav'])}</span></nav>
<h1>{h1_html(c['h1'])}</h1><p class="lead">{esc(c['intro'][0])}</p><div class="btns">{btn_contacto(lang, aqui)}{'<a class="btn" href="#proyectos">' + esc(u['ver_proy']) + '</a>' if ps else ''}</div></div>
<div class="serv-hero-v">{vis}</div></section>
<section class="wrap seccion"><h2 class="rev" style="margin-bottom:var(--e8)">{esc(u['para'])}</h2><ul class="tres">{para}</ul></section>
<section class="wrap seccion"><div class="cab-sec"><h2>{esc(u['incluye'])}</h2><p class="lead sm">{esc(c['intro'][1])}</p></div><ul class="inc-grid">{inc}</ul></section>
{banda}
<section class="wrap seccion"><h2 class="rev" style="margin-bottom:var(--e8)">{esc(u['proceso'])}</h2><ol class="pasos">{pasos}</ol></section>
<section class="wrap seccion"><div class="panel entregables rev"><h2 class="h3">{esc(u['ent'])}</h2><ul class="pildoras">{ent}</ul></div></section>
{bloque_rel}<section class="wrap seccion"><h2 class="rev" style="margin-bottom:var(--e8)">{esc(u['porque'])}</h2><ul class="cuatro">{porque}</ul></section>
<section class="wrap seccion"><div class="dos"><div><h2>{esc(u['faq'])}</h2></div><div class="faq">{faq}</div></div></section>
{cta_final(lang, aqui, k)}'''
    esq = jsonld({'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', 'name': c['titulo'], 'description': c['desc'], 'url': url_abs(aqui), 'serviceType': c['nav'],
         'provider': {'@type': 'ProfessionalService', 'name': 'Mariana Boscán', 'url': SITIO + '/', 'telephone': '+573243591199', 'email': EMAIL,
                      'address': {'@type': 'PostalAddress', 'addressLocality': 'Bogotá', 'addressCountry': 'CO'}},
         'areaServed': [{'@type': 'Country', 'name': 'Colombia'}, {'@type': 'Place', 'name': 'Worldwide'}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': u['inicio'], 'item': url_abs(ruta('inicio', lang))},
            {'@type': 'ListItem', 'position': 2, 'name': u['servicios'], 'item': url_abs(ruta('servicios', lang))},
            {'@type': 'ListItem', 'position': 3, 'name': c['titulo'], 'item': url_abs(aqui)}]}]})
    return pagina(lang, aqui, 'servicios', f"{c['titulo']} | Mariana Boscán", c['desc'], cuerpo, ruta_serv(k, 'en' if lang == 'es' else 'es'), extra_head=esq,
                  extra_body=f'<script src="{rel(aqui, "animar.js")}" defer></script>', body_class='servicio')


def pagina_servicios(lang):
    t = UI[lang]; u = SERV_UI[lang]; aqui = ruta('servicios', lang)
    cards = ''
    for i, k in enumerate(ORDEN):
        c = SERVICIOS[k][lang]; x = EXTRA[k][lang]
        top = ''.join(f'<li>{esc(e)}</li>' for e in c['incluye'][:3])
        cards += (f'<li class="sp-card rev" style="--d:{i * .06:.2f}s"><a href="{rel(aqui, ruta_serv(k, lang))}"><span class="sp-ico">{ico2(SERVICIOS[k]["icono"])}</span><span class="sp-n">{i + 1:02d}</span>'
                  f'<h2>{esc(c["nav"])}</h2><p>{esc(c["corto"])}</p><ul class="check">{top}</ul><span class="mas">{esc(u["ir"])} {ico("flecha")}</span></a></li>')
    pasos = ''.join(f'<li class="rev" style="--d:{i * .08:.2f}s"><span class="n">{i + 1:02d}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(u['proceso_gral']))
    cuerpo = f'''<section class="cab-pagina wrap"><h1>{h1_html(u['pag_h1'])}</h1><p class="lead">{esc(u['pag_lead'])}</p></section>
<section class="wrap"><ul class="sp-grid">{cards}</ul></section>
<section class="wrap seccion"><h2 class="rev" style="margin-bottom:var(--e8)">{esc(u['proceso_h'])}</h2><ol class="pasos">{pasos}</ol></section>
<section class="wrap seccion"><h2 class="rev" style="margin-bottom:var(--e8)">{esc(u['porque'])}</h2><ul class="cuatro">{''.join(f'<li class="rev" style="--d:{i * .08:.2f}s"><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(u['porque_items']))}</ul></section>
{cta_final(lang, aqui)}'''
    desc = u['pag_lead']
    return pagina(lang, aqui, 'servicios', f"{u['h2']} | Mariana Boscán", desc, cuerpo, ruta('servicios', 'en' if lang == 'es' else 'es'),
                  extra_body=f'<script src="{rel(aqui, "animar.js")}" defer></script>')


def contacto_form(lang):
    t = UI[lang]
    opciones = ''.join(f'<option value="{v}">{esc(n)}</option>' for v, n in t['f_origenes'])
    return f'''<form class="panel" id="form" novalidate>
<div class="campo"><label for="nombre">{esc(t['f_nombre'])}</label><input id="nombre" name="nombre" type="text" autocomplete="name" required maxlength="120"></div>
<div class="campo"><label for="email">{esc(t['f_email'])}</label><input id="email" name="email" type="email" autocomplete="email" required maxlength="200"></div>
<div class="fila2"><div class="campo"><label for="tel">{esc(t['f_tel'])}</label><input id="tel" name="tel" type="tel" autocomplete="tel" maxlength="40"></div>
<div class="campo"><label for="origen">{esc(t['f_origen'])}</label><div class="sel"><select id="origen" name="origen"><option value="">{esc(t['f_origen_ph'])}</option>{opciones}</select>{ICONO_CHEV}</div></div></div>
<div class="campo"><label for="mensaje">{esc(t['f_mensaje'])}</label><textarea id="mensaje" name="mensaje" rows="4" required maxlength="4000"></textarea></div>
<div class="trampa" aria-hidden="true"><label>Web <input type="text" name="web" tabindex="-1" autocomplete="off"></label></div>
<button class="btn primario" type="submit" id="enviar">{esc(t['f_enviar'])}</button>
<p class="nota">{esc(t['f_priv'])}</p><div id="estado" role="status" aria-live="polite"></div></form>'''


def contacto_js(lang):
    t = UI[lang]
    msgs = json.dumps({'ok': t['f_ok'], 'err': t['f_err'], 'inv': t['f_inv'], 'lim': t['f_lim'], 'enviando': t['f_enviando'], 'enviar': t['f_enviar']}, ensure_ascii=False)
    return f'''<script>
(function(){{
var ENDPOINT={json.dumps(ENDPOINT)},M={msgs},IDIOMA={json.dumps(lang)};
var f=document.getElementById('form'),b=document.getElementById('enviar'),s=document.getElementById('estado');
function aviso(t,err){{s.innerHTML='';var p=document.createElement('p');p.className='aviso'+(err?' error':'');p.textContent=t;s.appendChild(p);}}
f.addEventListener('submit',function(e){{e.preventDefault();
 var d={{formulario:'contacto',idioma:IDIOMA,nombre:f.nombre.value.trim(),email:f.email.value.trim(),telefono:f.tel.value.trim(),origen:f.origen.value,origen_texto:f.origen.options[f.origen.selectedIndex].text,mensaje:f.mensaje.value.trim(),web:f.web.value}};
 if(!d.nombre||!d.mensaje||!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(d.email)){{aviso(M.inv,true);return;}}
 if(ENDPOINT.indexOf('http')!==0){{aviso(M.err,true);return;}}
 b.disabled=true;b.textContent=M.enviando;
 fetch(ENDPOINT,{{method:'POST',headers:{{'Content-Type':'text/plain;charset=utf-8'}},body:JSON.stringify(d)}})
 .then(function(r){{return r.json()}}).then(function(r){{
   if(r&&r.ok){{aviso(M.ok,false);f.reset();}}else{{aviso(r&&r.error==='limite'?M.lim:(r&&r.error==='datos_invalidos'?M.inv:M.err),true);}}
 }}).catch(function(){{aviso(M.err,true);}}).then(function(){{b.disabled=false;b.textContent=M.enviar;}});
}});}})();
</script>'''


FOTO = '593a1fae-6199-48f6-b0f9-59a35c018a67_rw_1200.png?h=870e8eb6e5363c7d73488a4ac025154b'   # tu foto actual (Adobe); pon tu foto nueva en src/img/foto.jpg|png|webp
SRC_IMG = os.path.join(AQUI, 'src', 'img')
LOCALES = set(os.listdir(SRC_IMG)) if os.path.isdir(SRC_IMG) else set()
LOCALES_PROY = {f'proyectos/{d}/{f}' for d in os.listdir(os.path.join(SRC_IMG, 'proyectos'))
                for f in os.listdir(os.path.join(SRC_IMG, 'proyectos', d))} if os.path.isdir(os.path.join(SRC_IMG, 'proyectos')) else set()
FOTO_LOCAL = next((f for f in ('foto.webp', 'foto.jpg', 'foto.jpeg', 'foto.png') if f in LOCALES), None)


def IMG(nombre, aqui):
    """URL de una imagen: si ya está descargada en src/img se usa esa copia; si no, la de Adobe."""
    archivo = nombre.split('?')[0]
    if archivo in LOCALES: return rel(aqui, 'img/') + archivo
    return BASE + nombre


def url_foto(aqui):
    if FOTO_LOCAL: return rel(aqui, 'img/') + FOTO_LOCAL
    return IMG(FOTO, aqui)


def img_portada(p, alt, aqui):
    a, b = p['c']
    return (f'<img src="{IMG(a, aqui)}" srcset="{IMG(a, aqui)} 640w, {IMG(b, aqui)} 1280w" sizes="(min-width:700px) 50vw, 100vw" '
            f'alt="{esc(alt)}" width="640" height="480" loading=lazy decoding="async">')


def tarjeta(p, lang, aqui, n):
    marca, des, den, cat = META[p['s']]
    desc = des if lang == 'es' else den
    href = rel(aqui, proy_ruta(p['s'], lang))
    return (f'<li data-cat="{cat}"><a class="tarjeta" href="{href}"><div class="img">{img_portada(p, marca + " — " + desc, aqui)}</div>'
            f'<div class="meta"><span class="num" aria-hidden="true">{n:02d}</span><div><h3>{esc(marca)}</h3><p>{esc(desc)} · {esc(CATS[cat][0 if lang == "es" else 1])}</p></div></div></a></li>')


def cover_img(e, alt, aqui):
    """Portada de un proyecto de Behance en alta resolución: primero una portada propia (src/img/proyectos/<id>/cover.webp),
    si no, la versión grande de Behance (808 px) con respaldo automático a la original (404 px)."""
    loc = next((l for l in (f'proyectos/{e["id"]}/cover.webp', f'proyectos/{e["clave"]}/cover.webp') if l in LOCALES_PROY), None)
    if loc: src, resp = rel(aqui, 'img/') + loc, ''
    else:
        orig = e['cover']; src = orig.replace('/projects/404/', '/projects/808/')
        resp = f' onerror="this.onerror=null;this.src=\'{esc(orig)}\'"' if src != orig else ''
    return f'<img src="{src}" alt="{esc(alt)}" width="640" height="480" loading=lazy decoding="async"{resp}>'


def tarjeta_ext(e, lang, n, aqui):
    desc = e['des'] if lang == 'es' else e['den']
    cat = e.get('cat', 'branding')
    if e.get('imgs'): enlace = f'href="{rel(aqui, proy_ruta(e["slug"], lang))}"'
    else: enlace = f'href="{esc(e["link"])}" target="_blank" rel="noopener"'   # hasta tener las imágenes, abre Behance
    flecha = '' if e.get('imgs') else ' ↗'
    return (f'<li data-cat="{" ".join(categorias_de(e))}"><a class="tarjeta" {enlace}><div class="img">{cover_img(e, e["marca"] + " — " + desc, aqui)}</div>'
            f'<div class="meta"><span class="num" aria-hidden="true">{n:02d}</span><div><h3>{esc(e["marca"])}</h3><p>{esc(desc)} · {esc(CATS[cat][0 if lang == "es" else 1])}{flecha}</p></div></div></a></li>')


def pagina_proyecto_ext(e, lang):
    t = UI[lang]; aqui = proy_ruta(e['slug'], lang)
    desc = e['des'] if lang == 'es' else e['den']
    piezas = []          # cada elemento: lista de imágenes; las que llevan un 3.er valor 1 continúan la anterior y se pegan sin espacio (imagen larga cortada en tramos)
    for i, m in enumerate(e['imgs']):
        url, pct = m[0], (m[1] if len(m) > 1 else None)
        if not url.startswith('http'): url = rel(aqui, 'img/') + url          # imagen local: img/proyectos/<id>/NN.webp
        dims = f' width="1000" height="{round(pct * 10)}"' if pct else ''
        img = f'<img src="{esc(url)}" alt="{esc(e["marca"])} — {esc(desc)}"{dims} loading="{"eager" if i == 0 else "lazy"}" decoding="async">'
        if len(m) > 2 and m[2] and piezas: piezas[-1].append(img)
        else: piezas.append([img])
    piezas = [f'<div class="serie">{"".join(g)}</div>' for g in piezas]
    cuerpo = cab_int(CATS[e.get('cat', 'branding')][0 if lang == 'es' else 1], esc(e['marca']), esc(desc)) + f'''
<section class="wrap pila-int"><div class="pila">{''.join(piezas)}</div>
<div class="pager"><a class="btn" href="{rel(aqui, ruta('portafolio', lang))}">← {esc(t['volver'])}</a><a class="btn" href="{esc(e['link'])}" target="_blank" rel="noopener">{esc(t['ver_behance'])} ↗</a></div></section>''' + cta_interna(lang, aqui)
    otra = proy_ruta(e['slug'], 'en' if lang == 'es' else 'es')
    return pagina(lang, aqui, 'portafolio', f"{e['marca']} — {desc} | Mariana Boscán", f"{e['marca']}: {desc}. {t['desc_sitio']}"[:250], cuerpo, otra, og_img=e['imgs'][0][0] if e['imgs'][0][0].startswith('http') else SITIO + '/img/' + e['imgs'][0][0], extra_body=INT_JS(aqui), body_class='interna')


ICONO_SOL = '<svg class="i-sol" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICONO_LUNA = '<svg class="i-luna" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>'
ICONO_GLOBO = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.5 3.8 9S14.5 18.5 12 21c-2.5-2.5-3.8-5.5-3.8-9S9.5 5.5 12 3z"/></svg>'
ICONO_CHEV = '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'

TEMA_HEAD = ''
TEMA_JS = '''<script>
(function(){var d=document.querySelector('details.idioma');if(d){document.addEventListener('click',function(e){if(!d.contains(e.target))d.removeAttribute('open')});document.addEventListener('keydown',function(e){if(e.key==='Escape')d.removeAttribute('open')})}})();
</script>'''




def cabecera(lang, aqui, clave, otra_ruta):
    t = UI[lang]
    a = rel(aqui, 'assets/')
    otro = 'en' if lang == 'es' else 'es'
    home = ruta('inicio', lang)
    hc0 = HC[lang]
    base = '' if clave == 'inicio' else rel(aqui, ruta('inicio', lang))
    entradas = [('portafolio', 'proyectos', t['nav']['portafolio']), ('sobre', 'sobre', t['nav']['sobre']), ('experiencia', 'experiencia', hc0['nav_exp']), ('contacto', 'contacto', t['nav']['contacto'])]
    nav = ''.join(f'<a href="{base}#{anc}"{" aria-current=page" if (k == clave and clave != "inicio") else ""}>{esc(v)}</a>' for k, anc, v in entradas)
    nombres = {'es': 'Español', 'en': 'English'}
    items = ''.join(
        f'<li><a href="{rel(aqui, otra_ruta) if l != lang else "#"}" hreflang="{l}" lang="{l}"{" aria-current=true" if l == lang else ""}>{nombres[l]}<small>{l.upper()}</small></a></li>'
        for l in ('es', 'en'))
    hc = HC[lang]
    return f'''<a class="skip" href="#contenido">{esc(t['skip'])}</a>
<div class="barra{' foto' if clave == 'inicio' else ''}"><header class="wrap top">
  <a class="logo" href="{rel(aqui, ruta('inicio', lang))}" aria-label="Mariana Boscán">
    <img class="l-claro" src="{a}mariana-boscan-logo-tinta.svg" alt="Mariana Boscán" width="160" height="46">
    <img class="l-oscuro" src="{a}mariana-boscan-logo-blanco-degradado.svg" alt="" width="160" height="46"></a>
  <nav class="nav" aria-label="{esc(t['menu'])}">{nav}</nav>
  <div class="ctl">
    <a class="btn primario cta-nav" href="{base}#contacto"><span>{esc(hc['nav_cta'])}</span><i class="chip">{ico('flecha')}</i></a>
    <details class="idioma"><summary aria-label="{esc(t['idioma_aria'])}">{ICONO_GLOBO}<span>{nombres[lang]}</span>{ICONO_CHEV}</summary><ul>{items}</ul></details>
  </div>
</header></div>'''


def pagina(lang, aqui, clave, titulo, desc, cuerpo, otra_ruta, og_img=None, extra_head='', extra_body='', body_class='', robots='index,follow,max-image-preview:large'):
    t = UI[lang]
    es_ruta, en_ruta = (aqui, otra_ruta) if lang == 'es' else (otra_ruta, aqui)
    # inglés por defecto; si el navegador está en español (y no eligió idioma a mano) se manda a la versión en español
    guardar = "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[hreflang]');if(a){try{localStorage.setItem('lang',a.getAttribute('hreflang'))}catch(_){}}});"
    ir_es = ("try{if(!localStorage.getItem('lang')){var l=((navigator.languages&&navigator.languages[0])||navigator.language||'en').toLowerCase();if(l.indexOf('es')===0){location.replace(" + json.dumps(rel(aqui, es_ruta)) + "+location.hash)}}}catch(_){}") if lang == 'en' else ''
    lang_script = f'<script>{ir_es}{guardar}</script>\n'
    canon = url_abs(aqui)
    a = rel(aqui, 'assets/')
    og = og_img or (SITIO + '/img/og.jpg' if 'og.jpg' in LOCALES else BASE + D['proyectos'][0]['c'][1])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="es" href="{url_abs(es_ruta)}">
<link rel="alternate" hreflang="en" href="{url_abs(en_ruta)}">
<link rel="alternate" hreflang="x-default" href="{url_abs(en_ruta)}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{og}"><meta property="og:locale" content="{t['og_locale']}"><meta property="og:site_name" content="Mariana Boscán">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#14141e">
<link rel="icon" type="image/svg+xml" href="{a}mariana-boscan-favicon.svg">
<link rel="preload" href="{rel(aqui, 'fonts/')}DMSans-Variable.woff2" as="font" type="font/woff2" crossorigin>
{TEMA_HEAD}
{lang_script}<link rel="stylesheet" href="{rel(aqui, 'styles.css')}">
{extra_head}</head>
<body class="{body_class}">
{cabecera(lang, aqui, clave, otra_ruta)}
<main id="contenido">
{cuerpo}
</main>
{pie(lang, aqui)}
{fab(lang)}
{TEMA_JS}
{extra_body}</body>
</html>
'''


BANNER_LOCAL = next((f for f in ('banner.webp', 'banner.jpg', 'banner.jpeg', 'banner.png') if f in LOCALES), None)


def banner(aqui, alt):
    """Tu banner (src/img/banner.jpg|png|webp). Mientras no esté, se muestra un espacio con tu degradado."""
    if BANNER_LOCAL:
        return f'<div class="banner wrap"><div class="marco"><img src="{rel(aqui, "img/") + BANNER_LOCAL}" alt="{esc(alt)}" fetchpriority="high"></div></div>'
    return '<div class="banner wrap"><div class="marco vacio" aria-hidden="true"></div></div>'



NUEVO = {
 'es': dict(
  h1_a='Branding con estrategia,', h1_b_pre='diseño con ', h1_b_serif='intención', h1_b_post='.',
  hero_sub='Soy Mariana Boscán, diseñadora gráfica en Bogotá, Colombia. Más de 8 años creando logos, tiendas online, redes sociales y sitios web estratégicos y visualmente poderosos.',
  hero_btn2='Escríbeme', hero_cta='Contáctame ahora',
  vidrios=[('Branding', 'Identidad visual', 'capas'), ('Web y tiendas', 'Shopify y WordPress', 'pantalla'), ('Editorial', 'Informes y marcas', 'libro'), ('Social', 'Contenido digital', 'chat')],
  lateral_i=('Estrategia primero.', 'Cada decisión visual tiene una razón.'), lateral_d=('Dos idiomas.', 'Proyectos en español e inglés.'),
  nota_i='Más de 8 años creando marcas.', nota_d='Menos ruido.\nMás sentido.', rueda='MARIANA BOSCÁN · GRAPHIC DESIGNER · ',
  enunciado=[('Una marca no es un logo bonito.', ''), ('Es una idea clara, bien dicha y bien diseñada en cada pieza.', '')],
  galeria_h='Proyectos destacados', galeria_ver='Ver todos los proyectos',
  cine=['Más de 8 años creando experiencias de marca reflexivas, estratégicas y visualmente atractivas.', 'Branding, editorial, experiencias digitales, redes sociales, web y tiendas online en Shopify: sistemas visuales sólidos y comunicación clara.', 'Diseño, tipografía, accesibilidad y narrativa: trabajo que comunica con propósito.'],
  contacto_cta='¿Tienes un proyecto en mente?', contacto_btn='Hablemos', secciones=['Inicio', 'Idea', 'Proyectos', 'Sobre mí', 'Herramienta', 'Contacto']),
 'en': dict(
  h1_a='Strategic branding,', h1_b_pre='design with ', h1_b_serif='intention', h1_b_post='.',
  hero_sub='I’m Mariana Boscán, a graphic designer in Bogotá, Colombia. 8+ years creating logos, online stores, social media and websites that are strategic and visually compelling.',
  hero_btn2='Get in touch', hero_cta='Contact me now',
  vidrios=[('Branding', 'Visual identity', 'capas'), ('Web & stores', 'Shopify & WordPress', 'pantalla'), ('Editorial', 'Reports & brands', 'libro'), ('Social', 'Digital content', 'chat')],
  lateral_i=('Strategy first.', 'Every visual decision has a reason.'), lateral_d=('Two languages.', 'Projects in Spanish and English.'),
  nota_i='8+ years building brands.', nota_d='Less noise.\nMore meaning.', rueda='MARIANA BOSCÁN · GRAPHIC DESIGNER · ',
  enunciado=[('A brand is not a pretty logo.', ''), ('It’s a clear idea, well told and well designed in every piece.', '')],
  galeria_h='Selected work', galeria_ver='See all projects',
  cine=['8+ years creating thoughtful, strategic, and visually compelling brand experiences.', 'Branding, editorial, digital experiences, social media, web and Shopify online stores: strong visual systems and clear communication.', 'Design, typography, accessibility and storytelling: work that communicates with purpose.'],
  contacto_cta='Have a project in mind?', contacto_btn='Let’s talk', secciones=['Home', 'Idea', 'Work', 'About', 'Tool', 'Contact']),
}
for _l in NUEVO: UI[_l].update(NUEVO[_l])

if not MOSTRAR_SERVICIOS:   # textos para reclutadores y agencias (sin servicios ni captación de clientes)
    UI['es'].update(
        titulo_sitio='Mariana Boscán | Design Team Lead y diseñadora gráfica senior',
        desc_sitio='Portafolio de Mariana Boscán, Design Team Lead y diseñadora gráfica senior con más de 8 años de experiencia en branding, web, UI, editorial y sistemas de diseño.',
        hero_sub='Soy Mariana Boscán, Design Team Lead y diseñadora gráfica senior. Más de 8 años liderando y creando branding, web, UI y sistemas de diseño para equipos y agencias internacionales.',
        hero_cta='Conectemos', vidrios=[('Branding', 'Identidad visual', 'capas'), ('Web y UI', 'Sitios y sistemas', 'pantalla'), ('Editorial', 'Informes y marcas', 'libro'), ('Social', 'Contenido digital', 'chat')],
        port_lead='Identidades de marca, web, UI, social media, piezas editoriales y casos de estudio.',
        contacto_cta='Conectemos', contacto_btn='Escríbeme', contacto_h1=('Conectemos', ''),
        contacto_lead='Si tu equipo o agencia busca una diseñadora senior o líder de diseño, escríbeme y conversamos.',
        pie='Diseñadora gráfica senior · Bogotá, Colombia')
    UI['en'].update(
        titulo_sitio='Mariana Boscán | Design Team Lead & Senior Graphic Designer',
        desc_sitio='Portfolio of Mariana Boscán, Design Team Lead and senior graphic designer with 8+ years of experience in branding, web, UI, editorial and design systems.',
        hero_sub='I’m Mariana Boscán, a Design Team Lead and senior graphic designer. 8+ years leading and creating branding, web, UI and design systems for international teams and agencies.',
        hero_cta='Let’s connect', vidrios=[('Branding', 'Visual identity', 'capas'), ('Web & UI', 'Sites & systems', 'pantalla'), ('Editorial', 'Reports & brands', 'libro'), ('Social', 'Digital content', 'chat')],
        port_lead='Brand identities, web, UI, social media, editorial pieces and case studies.',
        contacto_cta='Let’s connect', contacto_btn='Get in touch', contacto_h1=('Let’s ', 'connect'),
        contacto_lead='If your team or agency is looking for a senior designer or design lead, write to me and let’s talk.',
        pie='Senior Graphic Designer · Bogotá, Colombia')
    UI['es'].update(f_err='No pude enviar el mensaje. Escríbeme directamente por correo o LinkedIn.', f_lim='Has enviado varios mensajes seguidos. Intenta de nuevo más tarde o escríbeme por correo.')
    UI['en'].update(f_err='I couldn’t send the message. Please email me or message me on LinkedIn.', f_lim='You’ve sent several messages in a row. Try again later or email me.')
    SERV_UI['es'].update(cta_h='Conectemos', cta_p='Si tu equipo o agencia busca una diseñadora senior o líder de diseño, escríbeme.', cta_b='Escríbeme')
    SERV_UI['en'].update(cta_h='Let’s connect', cta_p='If your team or agency is looking for a senior designer or design lead, write to me.', cta_b='Get in touch')
ICONOS_EXTRA = {
 'pantalla': '<rect x="3" y="4.5" width="18" height="12" rx="2.5"/><path d="M8 20h8M12 16.5V20"/>',
 'libro': '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
 'chat': '<path d="M4 5.5h16v10H9.5L5 19.5v-4H4z"/>',
 'diana': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".8"/>',
 'play': '<rect x="3" y="5" width="18" height="14" rx="4"/><path d="m10 9.2 5 2.8-5 2.8z"/>',
}
HERO_LOCAL = next((f for f in ('hero.webp', 'hero.png', 'hero.jpg', 'hero.jpeg') if f in LOCALES), None)
SOBRE_LOCAL = next((f for f in ('sobre.webp', 'sobre.png', 'sobre.jpg', 'sobre.jpeg') if f in LOCALES), None)


def ico2(n):
    if n in ICONOS_EXTRA: return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONOS_EXTRA[n]}</svg>'
    return ico(n)


def img_escena(aqui, local, alt, **kw):
    if local: return f'<img class="recorte" src="{rel(aqui, "img/") + local}" alt="{esc(alt)}" {kw.get("attrs", "")}>'
    return f'<img class="redonda" src="{url_foto(aqui)}" alt="{esc(alt)}" {kw.get("attrs", "")}>'


CARTAS = {  # (lado, fila, título, subtítulo, icono): una carta por servicio, en orden de aparición al hacer scroll
 'es': [('i', 0, 'Branding', 'Logo, manual de marca e identidad', 'sv_branding'), ('d', 0, 'Tiendas online', 'Shopify a tu medida', 'sv_tiendas'), ('d', 1, 'Redes sociales', 'Contenido consistente', 'sv_social'),
        ('i', 1, 'Editorial', 'Flyers, brochures e informes', 'sv_editorial'), ('i', 2, 'YouTube', 'Miniaturas que invitan a clic', 'sv_youtube'), ('d', 2, 'Diseño web', 'WordPress y Shopify', 'sv_web')],
 'en': [('i', 0, 'Branding', 'Logo, brand guidelines & identity', 'sv_branding'), ('d', 0, 'Online stores', 'Shopify made for you', 'sv_tiendas'), ('d', 1, 'Social media', 'Consistent content', 'sv_social'),
        ('i', 1, 'Editorial', 'Flyers, brochures & reports', 'sv_editorial'), ('i', 2, 'YouTube', 'Thumbnails that invite clicks', 'sv_youtube'), ('d', 2, 'Web design', 'WordPress & Shopify', 'sv_web')],
}


MOSTRAR_CARTAS = False  # pon True para volver a mostrar las cards alrededor de la foto


HERO_ESTILO = os.environ.get('HERO_ESTILO', 'cine')   # 'figma' = interfaz de Figma · 'cine' = foto a pantalla completa estilo cine · 'clasico' = hero anterior

HF = {
 'es': dict(archivo='Mariana Boscán — Portafolio', borrador='Borrador', compartir='Conectemos', paginas='Páginas', capas='Capas', diseno='Diseño', prototipo='Prototipo',
            pags=('inicio', 'portafolio', 'sobre', 'contacto'), cap=('Portafolio', 'Hero', 'Titular', 'Subtítulo', 'Retrato', 'Botón'),
            props=[('Cargo', 'Design Team Lead'), ('Experiencia', '8+ años'), ('Enfoque', 'Branding · Web · UI'), ('Ubicación', 'Bogotá · Remoto')],
            estado='Abierta a roles remotos', color='Color', tipo='Tipografía', tu='Tú', pin_t='Mariana', pin_p='¡Hola! Abierta a roles remotos con equipos de EE. UU.', marco='Hero · 1440 × 900'),
 'en': dict(archivo='Mariana Boscán — Portfolio', borrador='Draft', compartir='Let’s connect', paginas='Pages', capas='Layers', diseno='Design', prototipo='Prototype',
            pags=('inicio', 'portafolio', 'sobre', 'contacto'), cap=('Portfolio', 'Hero', 'Headline', 'Subtitle', 'Portrait', 'Button'),
            props=[('Role', 'Design Team Lead'), ('Experience', '8+ years'), ('Focus', 'Branding · Web · UI'), ('Location', 'Bogotá · Remote')],
            estado='Open to remote roles', color='Color', tipo='Typography', tu='You', pin_t='Mariana', pin_p='Hi! Open to remote roles with US teams.', marco='Hero · 1440 × 900'),
}
_I = lambda d: f'<svg viewBox="0 0 16 16" aria-hidden="true">{d}</svg>'
HF_ICO = {
 'mover': _I('<path d="M3 2l9 4-4 1.500L6.500 12z"/>'), 'marco': _I('<path d="M5 1.500v13M11 1.500v13M1.500 5h13M1.500 11h13"/>'),
 'forma': _I('<rect x="2.500" y="2.500" width="11" height="11" rx="1"/>'), 'pluma': _I('<path d="M2.500 13.500l1-4 6-6 3 3-6 6zM8.500 4.500l3 3"/>'),
 'texto': _I('<path d="M3 4V2.500h10V4M8 2.500v11M6 13.500h4"/>'), 'coment': _I('<path d="M2.500 3h11v8h-6l-3 2.500V11h-2z"/>'),
 'hash': _I('<path d="M5 1.500v13M11 1.500v13M1.500 5h13M1.500 11h13"/>'), 'pagina': _I('<path d="M3.500 1.500h6l3 3v10h-9z"/>'),
}


def _palabras(texto, n0, serif=False):
    out = []; n = n0
    for w in texto.split():
        cls = ' class="serif"' if serif else ''
        out.append(f'<span class="w"><span style="--i:{n}"{cls}>{esc(w)}</span></span>'); n += 1
    return ' '.join(out), n


def hero_figma(lang, aqui):
    t = UI[lang]; h = HF[lang]
    a, n = _palabras(t['h1_a'], 0)
    b, n = _palabras(t['h1_b_pre'].strip(), n)
    c, n = _palabras(t['h1_b_serif'] + t['h1_b_post'], n, serif=True)
    h1 = f'{a}<br>{b} {c}'
    pag = {k: UI[lang]['nav'][k] for k in h['pags']}
    pags = ''.join(f'<li><a href="{rel(aqui, ruta(k, lang))}"{" aria-current=page" if k == "inicio" else ""}>{HF_ICO["pagina"]}{esc(v)}</a></li>' for k, v in pag.items())
    cap = h['cap']
    capas = (f'<li style="--k:0">{HF_ICO["hash"]}{esc(cap[0])}</li><li class="n1" style="--k:1">{HF_ICO["marco"]}{esc(cap[1])}</li>'
             f'<li class="n2 h" style="--k:2;--w:1.5s">{HF_ICO["texto"]}{esc(cap[2])}</li><li class="n2" style="--k:3">{HF_ICO["texto"]}{esc(cap[3])}</li>'
             f'<li class="n2 h" style="--k:4;--w:3.3s">{HF_ICO["forma"]}{esc(cap[4])}</li><li class="n2 h" style="--k:5;--w:5.3s">{HF_ICO["forma"]}{esc(cap[5])}</li>')
    props = ''.join(f'<div style="animation-delay:{1.1 + i * .12:.2f}s"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for i, (k, v) in enumerate(h['props']))
    cursor = '<svg viewBox="0 0 18 20" aria-hidden="true"><path d="M1 1l5.500 15 2.200-6.200L15 7.600z"/></svg>'
    return f'''<section class="hf" id="inicio" data-nombre="{esc(t['secciones'][0])}" data-nav="inicio">
<div class="hf-barra" aria-hidden="true"><span class="t on">{HF_ICO['mover']}</span><span class="t">{HF_ICO['marco']}</span><span class="t">{HF_ICO['forma']}</span><span class="t">{HF_ICO['pluma']}</span><span class="t">{HF_ICO['texto']}</span><span class="t">{HF_ICO['coment']}</span><span class="sep"></span><span class="arch">{esc(h['archivo'])}<small>{esc(h['borrador'])}</small></span><span class="sep"></span><a class="comp" href="{rel(aqui, ruta('contacto', lang))}" tabindex="-1">{esc(h['compartir'])}</a></div>
<div class="hf-layout">
<aside class="hf-panel i" aria-hidden="true"><div class="hf-ph">{esc(h['paginas'])}</div><div class="hf-sec"><ul class="hf-pag">{pags}</ul></div><div class="hf-ph" style="border-top:1px solid var(--hf-borde)">{esc(h['capas'])}</div><div class="hf-sec"><ul class="hf-cap">{capas}</ul></div></aside>
<div class="hf-escena"><p class="hf-titulo">{HF_ICO['hash']}{esc(h['marco'])}</p>
<div class="hf-frame"><div class="hf-texto">
<div class="hf-envuelve"><h1 class="hf-h1">{h1}</h1><i class="hf-sel h" aria-hidden="true"><b></b><b></b><b></b><b></b><em>—</em></i></div>
<p class="hf-sub">{esc(t['hero_sub'])}</p>
<div class="btns"><span class="hf-btnwrap"><a class="btn primario" href="{rel(aqui, ruta('contacto', lang))}">{esc(t['hero_cta'])} {ico('flecha')}</a><i class="hf-sel b" aria-hidden="true"><b></b><b></b><b></b><b></b></i></span><a class="btn" href="{rel(aqui, ruta('portafolio', lang))}">{esc(t['ver_portafolio'])}</a></div></div>
<div class="hf-retrato">{img_escena(aqui, HERO_LOCAL, t['foto_alt'], attrs='fetchpriority="high"')}<i class="hf-sel p" aria-hidden="true"><b></b><b></b><b></b><b></b><em>—</em></i></div></div>
<div class="hf-cursor m" aria-hidden="true">{cursor}<span>{esc(h['pin_t'])}</span></div><div class="hf-cursor r" aria-hidden="true">{cursor}<span>{esc(h['tu'])}</span></div>
<div class="hf-pin" aria-hidden="true"><i>MB</i><p><b>{esc(h['pin_t'])}</b>{esc(h['pin_p'])}</p></div></div>
<aside class="hf-panel d" aria-hidden="true"><div class="hf-ph"><span class="tabs"><span class="a">{esc(h['diseno'])}</span><span>{esc(h['prototipo'])}</span></span><span>100%</span></div>
<div class="hf-sec"><dl class="hf-prop">{props}<div style="animation-delay:1.6s"><dt>Status</dt><dd class="hf-estado">{esc(h['estado'])}</dd></div></dl></div>
<div class="hf-sec"><h2>{esc(h['color'])}</h2><div class="hf-col"><span><i style="background:#afb5e7"></i>AFB5E7</span><span><i style="background:#ffbfef"></i>FFBFEF</span><span><i style="background:#14141e"></i>14141E</span></div></div>
<div class="hf-sec"><h2>{esc(h['tipo'])}</h2><div class="hf-tipo"><b>Aa</b><b class="s">Aa</b><small>DM Sans · Fraunces</small></div></div></aside>
</div>
<script>(function(){{var s=document.currentScript.parentNode;if(!s)return;
function m(e){{var r=s.getBoundingClientRect();s.style.setProperty('--mx',((e.clientX-r.left)/r.width-.5).toFixed(3));s.style.setProperty('--my',((e.clientY-r.top)/r.height-.5).toFixed(3))}}
if(!matchMedia('(prefers-reduced-motion:reduce)').matches&&matchMedia('(hover:hover)').matches)s.addEventListener('pointermove',m,{{passive:true}});
function z(){{s.querySelectorAll('.hf-sel em').forEach(function(e){{var p=e.parentNode.parentNode;e.textContent=Math.round(p.offsetWidth)+' × '+Math.round(p.offsetHeight)}})}}
z();addEventListener('resize',z);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(z)}})();</script>
</section>'''


HC = {
 'es': dict(anuncio='Abierta a roles remotos con equipos de EE. UU. · Design Team Lead en Partner in Publishing', anuncio_cta='Escríbeme', nav_exp='Experiencia', et_exp='Experiencia', exp_titulo='Dónde he trabajado', exp_ver='Ver experiencia completa', actual='Actual', fab='Contáctame', fab_t='Abrir opciones de contacto', fab_items=('Escríbeme por correo', 'WhatsApp', 'LinkedIn'), et_obra='Portafolio', et_sobre='Sobre mí', et_contacto='Contacto', stats=[('8+', 'Años de experiencia'), ('5', 'Empresas y agencias'), ('{n}', 'Proyectos en el portafolio'), ('ES · EN', 'Español nativo · Inglés conversacional')], nav_cta='Conectemos', etiqueta='Design Team Lead · Diseñadora gráfica senior',
         ahora='Ahora mismo', ahora_t='Liderando el equipo de diseño de una agencia de EE. UU.', chips=['Branding', 'Web', 'UI', 'Design systems', 'Accesibilidad'], cita='“Diseño con estrategia, con foco en el detalle.”',
         titulo='Design Team Lead · Diseñadora gráfica senior', anio='Portafolio', caps=['8+ años de experiencia', 'Branding · Web · UI · Design systems', 'Bogotá · Remoto'], estado='Abierta a roles remotos', scroll='Desliza'),
 'en': dict(anuncio='Open to remote roles with US teams · Design Team Lead at Partner in Publishing', anuncio_cta='Get in touch', nav_exp='Experience', et_exp='Experience', exp_titulo='Where I’ve worked', exp_ver='View full experience', actual='Current', fab='Let’s talk', fab_t='Open contact options', fab_items=('Email me', 'WhatsApp', 'LinkedIn'), et_obra='Portfolio', et_sobre='About', et_contacto='Contact', stats=[('8+', 'Years of experience'), ('5', 'Companies & agencies'), ('{n}', 'Projects in the portfolio'), ('ES · EN', 'Spanish native · English conversational')], nav_cta='Let’s connect', etiqueta='Design Team Lead · Senior Graphic Designer',
         ahora='Right now', ahora_t='Leading the design team at a US-based agency', chips=['Branding', 'Web', 'UI', 'Design systems', 'Accessibility'], cita='“Strategic design, obsessed with the details.”',
         titulo='Design Team Lead · Senior Graphic Designer', anio='Portfolio', caps=['8+ years of experience', 'Branding · Web · UI · Design systems', 'Bogotá · Remote'], estado='Open to remote roles', scroll='Scroll'),
}


def hero_cine(lang, aqui):
    t = UI[lang]; h = HC[lang]
    a, n = _palabras(t['h1_a'], 0)
    b, n = _palabras(t['h1_b_pre'].strip(), n)
    c, n = _palabras(t['h1_b_serif'] + t['h1_b_post'], n, serif=True)
    src = rel(aqui, 'img/') + 'hero-cine.webp'
    chips = ''.join(f'<span>{esc(x)}</span>' for x in h['chips'])
    ic = lambda d: f'<svg viewBox="0 0 20 20" aria-hidden="true">{d}</svg>'
    car = '<i class="car" aria-hidden="true"></i>'
    barra = (f'<div class="hc-fig" aria-hidden="true">'
        f'<span class="t on a1">{ic("<path d=\'M4.500 3l11 5-4.700 1.800L8.800 15z\' fill=\'currentColor\'/>")}</span>{car}'
        f'<span class="t a2">{ic("<path d=\'M7 3v14M13 3v14M3 7h14M3 13h14\'/>")}</span>{car}'
        f'<span class="t">{ic("<rect x=\'3.500\' y=\'3.500\' width=\'13\' height=\'13\' rx=\'1.500\'/>")}</span>{car}'
        f'<span class="t a3">{ic("<circle cx=\'10\' cy=\'8\' r=\'3.200\'/><path d=\'M3 17l4.500-5M12 13.500l5 3.500\'/>")}</span>{car}'
        f'<span class="t a4">{ic("<path d=\'M4 5V3.500h12V5M10 3.500v13M8 16.500h4\'/>")}</span>'
        f'<span class="t a5">{ic("<path d=\'M3.500 4h13v9h-7l-3.500 3v-3h-2.500z\'/>")}</span>'
        f'<span class="t">{ic("<path d=\'M4 4h4.500v4.500H4zM11.500 4H16v4.500h-4.500zM4 11.500h4.500V16H4zM11.500 13.700l2.300-2.300 2.300 2.300-2.300 2.300z\'/>")}</span>'
        f'<span class="sep"></span><span class="g"><span class="t">{ic("<path d=\'M4 15c2-6 4-9 6-9s1 5 3 5 2-3 3-3\'/>")}</span><span class="t on2">{ic("<rect x=\'3.500\' y=\'3.500\' width=\'13\' height=\'13\' rx=\'2\'/><path d=\'M7 13l2-4 2 2 2-3\'/>")}</span><span class="t">{ic("<path d=\'M7.500 6L3.500 10l4 4M12.500 6l4 4-4 4\'/>")}</span></span></div>')
    return f'''<section class="hc" id="inicio" data-nombre="{esc(t['secciones'][0])}" data-nav="inicio">
<div class="hc-bg"><div class="hc-par"><img class="hc-img" src="{src}" alt="{esc(t['foto_alt'])}" fetchpriority="high">
<div class="hc-str l" aria-hidden="true"><img src="{src}" alt=""></div></div></div>
<div class="hc-vel" aria-hidden="true"></div><div class="hc-grano" aria-hidden="true"></div>
<div class="hc-bar t" aria-hidden="true"></div><div class="hc-bar b" aria-hidden="true"></div>
<div class="hc-in"><div class="hc-texto"><p class="etiqueta hc-et">{ico('estrella')}<span>{esc(h['etiqueta'])}</span></p>
<h1 class="hc-h1">{a}<br><span class="ln">{b} {c}</span></h1>
<p class="hc-sub">{esc(t['hero_sub'])}</p>
<div class="btns"><a class="btn blanco" href="#contacto"><span>{esc(t['hero_cta'])}</span><i class="chip">{ico('flecha')}</i></a><a class="btn hc-ghost" href="#proyectos"><span>{esc(t['ver_portafolio'])}</span><i class="chip">{ico('flecha')}</i></a></div></div>
<aside class="hc-vidrio"><i class="hv-ic">{ico('estrella')}</i><p class="hv-q">{esc(' '.join(x for x, _ in t['enunciado']))}</p><p class="hv-f">Mariana Boscán</p></aside></div>
<script>(function(){{var s=document.currentScript.parentNode;if(matchMedia('(prefers-reduced-motion:reduce)').matches||!matchMedia('(hover:hover)').matches)return;
s.addEventListener('pointermove',function(e){{var r=s.getBoundingClientRect();s.style.setProperty('--mx',((e.clientX-r.left)/r.width-.5).toFixed(3));s.style.setProperty('--my',((e.clientY-r.top)/r.height-.5).toFixed(3))}},{{passive:true}})}})();</script>
</section>'''


def hero2(lang, aqui):
    if HERO_ESTILO == 'figma': return hero_figma(lang, aqui)
    if HERO_ESTILO == 'cine': return hero_cine(lang, aqui)
    t = UI[lang]
    cartas = '' if not MOSTRAR_CARTAS else ''.join(f'<div class="carta {"izq" if lado == "i" else "der"} f{fila}" style="--i:{n}"><span class="vi">{ico2(ic)}</span><b>{esc(ti)}</b><small>{esc(sub)}</small></div>'
                     for n, (lado, fila, ti, sub, ic) in enumerate(CARTAS[lang]))
    rueda = esc(t['rueda'])
    return f'''<section class="hero2" id="inicio" data-nombre="{esc(t['secciones'][0])}" data-nav="inicio" style="--nc:{len(CARTAS[lang])}"><div class="pantalla hero2-pin">
<div class="hero2-texto"><h1 class="entra"><span>{esc(t['h1_a'])}</span><br>{esc(t['h1_b_pre'])}<span class="serif">{esc(t['h1_b_serif'])}</span>{esc(t['h1_b_post'])}</h1>
<p class="lead2 entra" style="--d:.15s">{esc(t['hero_sub'])}</p>
<div class="btns entra" style="--d:.3s"><a class="btn primario" href="{rel(aqui, ruta('contacto', lang))}">{esc(t['hero_cta'])} {ico('flecha')}</a><a class="btn" href="{rel(aqui, ruta('portafolio', lang))}">{esc(t['ver_portafolio'])}</a></div></div>
<div class="escena2 entra" style="--d:.45s">
<div class="retrato2">{img_escena(aqui, HERO_LOCAL, t['foto_alt'], attrs='fetchpriority="high"')}</div>{cartas}
</div>
<svg class="rueda" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="circ" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1-92 0"/></defs><g class="gira"><text><textPath href="#circ" textLength="284" lengthAdjust="spacing">{rueda}</textPath></text></g><path class="estrella" d="M60 46c1.5 8 4.5 11.500 14 14-9.500 2.500-12.500 6-14 14-1.500-8-4.500-11.500-14-14 9.500-2.500 12.500-6 14-14z"/></svg>
</div></section>'''


def enunciado(lang):
    t = UI[lang]
    palabras = ''.join(f'<span class="pal">{esc(w)}</span> ' for linea, _ in t['enunciado'] for w in linea.split()) 
    # saltos de línea entre frases
    a, b = t['enunciado'][0][0].split(), t['enunciado'][1][0].split()
    html = ''.join(f'<span class="pal">{esc(w)}</span> ' for w in a) + '<br>' + ''.join(f'<span class="pal">{esc(w)}</span> ' for w in b)
    return f'''<section class="enunciado" id="idea" data-nombre="{esc(t['secciones'][1])}" data-nav="inicio"><div class="pin"><p class="grande">{html}</p></div></section>'''


def galeria(lang, aqui):
    t = UI[lang]; h = HC[lang]
    items = []
    for e in NUEVOS:
        desc = e['des'] if lang == 'es' else e['den']
        href = rel(aqui, proy_ruta(e['slug'], lang)) if e.get('imgs') else e['link']
        items.append((href, not e.get('imgs'), cover_img(e, e['marca'] + ' — ' + desc, aqui), e['marca'], desc))
    P = {p['s']: p for p in D['proyectos']}
    for p in D['proyectos']:
        marca, des, den, cat = META[p['s']]; desc = des if lang == 'es' else den
        items.append((rel(aqui, proy_ruta(p['s'], lang)), False, img_portada(p, marca + ' — ' + desc, aqui), marca, desc))
    k0 = 3
    lis = ''.join(f'<li class="tarj" style="--i:{i}"><div class="caja" style="--d:{i * .06:.2f}s"><a href="{esc(hr)}"{" target=_blank rel=noopener" if ext else ""} data-nom="{esc(m)}" data-desc="{esc(d)}"><span class="foto">{im}</span></a></div></li>'
                  for i, (hr, ext, im, m, d) in enumerate(items))
    h0 = items[k0]
    return f'''<section class="arco" id="proyectos" data-nombre="{esc(t['secciones'][2])}" data-nav="portafolio" data-paso="15.5" data-k0="{k0}" style="--n:{len(items)}"><div class="arco-pin"><div class="arco-escena">
<div class="arco-anillo" aria-hidden="true"></div><ul class="arco-rueda">{lis}</ul>
<div class="arco-centro"><p class="etiqueta">{ico('estrella')}<span>{esc(h['et_obra'])}</span></p><h2>{esc(t['galeria_h'])}</h2><p class="arco-sub">{esc(t['port_lead'])}</p>
<a class="arco-act" href="{esc(h0[0])}"><span class="n">{k0 + 1:02d}</span><span class="m">{esc(h0[3])}</span><span class="d">{esc(h0[4])}</span></a>
<div class="btns"><a class="btn primario" href="{rel(aqui, ruta('portafolio', lang))}"><span>{esc(t['galeria_ver'])}</span><i class="chip">{ico('flecha')}</i></a></div></div></div></div></section>'''


def galeria_clasica(lang, aqui):
    t = UI[lang]
    P = {p['s']: p for p in D['proyectos']}
    tarjetas = []
    for e in NUEVOS[:HOME_NUEVOS]:      # los proyectos más recientes de Behance van primero
        desc = e['des'] if lang == 'es' else e['den']
        href = rel(aqui, proy_ruta(e['slug'], lang)) if e.get('imgs') else esc(e['link'])
        ext = '' if e.get('imgs') else ' target="_blank" rel="noopener"'
        tarjetas.append(f'<a class="gcard" href="{href}"{ext}><div class="img">{cover_img(e, e["marca"] + " — " + desc, aqui)}</div>'
                        f'<div class="meta"><span class="num" aria-hidden="true">{len(tarjetas) + 1:02d}</span><div><h3>{esc(e["marca"])}</h3><p>{esc(desc)}</p></div></div></a>')
    for s in DESTACADOS:
        p = P[s]; marca, des, den, cat = META[s]; desc = des if lang == 'es' else den
        tarjetas.append(f'<a class="gcard" href="{rel(aqui, proy_ruta(s, lang))}"><div class="img">{img_portada(p, marca + " — " + desc, aqui)}</div>'
                        f'<div class="meta"><span class="num" aria-hidden="true">{len(tarjetas) + 1:02d}</span><div><h3>{esc(marca)}</h3><p>{esc(desc)}</p></div></div></a>')
    tarjetas.append(f'<a class="gcard final" href="{rel(aqui, ruta("portafolio", lang))}"><span>{esc(t["galeria_ver"])}</span>{ico("flecha")}</a>')
    return f'''<section class="galeria" id="proyectos" data-nombre="{esc(t['secciones'][2])}" data-nav="portafolio" style="--n:{len(tarjetas)}"><div class="pin"><div class="gtitulo"><p class="etiqueta">{ico('estrella')}<span>{esc(HC[lang]['et_obra'])}</span></p><h2>{esc(t['galeria_h'])}</h2></div><div class="pista">{''.join(tarjetas)}</div></div></section>'''


def cine(lang, aqui, tag='h2'):
    t = UI[lang]
    c = t['cine']
    return f'''<section class="pantalla cine" id="sobre" data-nombre="{esc(t['secciones'][3])}" data-nav="sobre"><div class="cine-luz"></div>
<div class="cine-retrato" data-zoom>{img_escena(aqui, SOBRE_LOCAL or HERO_LOCAL, t['foto_alt'], attrs='loading="lazy"')}</div>
<{tag} class="solo-lector">{esc(t['nav']['sobre'])}</{tag}>
</section>'''


HC['es'].update(cv='Descargar CV', cv_t='Descargar mi CV en PDF', sobre_f=[('capas', 'Marca y digital', 'Identidades, sitios web, tiendas online y landing pages coherentes entre canales.'), ('birrete', 'Diseño accesible', 'Contraste, legibilidad y claridad para que cualquier persona pueda usarlo.'), ('estrella', 'Diseño + IA', 'Exploro cómo la tecnología amplía la forma en que creamos.')])
HC['en'].update(cv='Download CV', cv_t='Download my CV as a PDF', sobre_f=[('capas', 'Brand and digital', 'Identities, websites, online stores and landing pages that stay consistent across channels.'), ('birrete', 'Accessible design', 'Contrast, legibility and clarity so anyone can read and use it.'), ('estrella', 'Design + AI', 'Exploring how technology expands the way we create.')])
CV_PDF = 'cv-mariana-boscan/Mariana-Boscan-CV.pdf'


def bio(lang, aqui):
    t = UI[lang]; h = HC[lang]
    ps = ''.join(f'<p>{esc(x)}</p>' for x in t['sobre_p'])
    ds = ''.join(f'<li><strong>{esc(k)}</strong>{esc(v)}</li>' for (k, v) in (t['datos'][0], t['datos'][2]))
    return f'''<section class="pantalla fondo-suave" id="sobre" data-nombre="{esc(t['secciones'][3])}" data-nav="sobre"><div class="wrap"><div class="sobre-v">
<figure class="sobre-foto rev"><img src="{rel(aqui, 'img/')}sobre-retrato.webp" alt="{esc(t['foto_alt'])}" loading="lazy" width="1190" height="1322"></figure>
<div class="sobre rev" style="--d:.12s"><p class="etiqueta">{ico('estrella')}<span>{esc(h['et_sobre'])}</span></p><h2>{h1_html(t['sobre_h1'])}</h2>{ps}
<p class="btns"><a class="btn primario" href="{rel(aqui, CV_PDF)}" download aria-label="{esc(h['cv_t'])}"><span>{esc(h['cv'])}</span><i class="chip">{ico('flecha')}</i></a></p></div></div></div></section>'''


def experiencia(lang):
    t = UI[lang]; en = lang == 'en'
    filas = ''.join(
        f'<li class="fila-e"><span class="anos">{esc(a.replace("—", "— " + t["presente"]) if a.endswith("—") else a)}</span><div><h3>{esc(r_en if en else r_es)}</h3><p class="emp">{esc(emp)}</p><p>{esc(d_en if en else d_es)}</p></div></li>'
        for a, r_es, r_en, emp, d_es, d_en in EXPERIENCIA)
    return f'''<section class="exp" id="experiencia" data-nombre="{esc(t['exp_h'])}" data-nav="sobre" style="--n:{len(EXPERIENCIA)}"><div class="pin"><div class="wrap exp-grid"><h2>{esc(t['exp_h'])}</h2><ol class="tiempo">{filas}</ol></div></div></section>'''


def formacion(lang, aqui):
    t = UI[lang]; en = lang == 'en'
    u, g_es, g_en, lugar, anio = EDUCACION
    ra = rel(aqui, 'assets/herramientas/')
    herr = ''.join(f'<div class="grupo-h"><h3>{esc(g_en_ if en else g_es_)}</h3><ul class="apps">' + ''.join(f'<li><img class="ic-n" src="{ra}{f}.png" alt="" width="56" height="56" loading="lazy"><img class="ic-b" src="{ra}{f}-claro.png" alt="" width="56" height="56" loading="lazy"><span>{esc(n)}</span></li>' for n, f in its) + '</ul></div>' for g_es_, g_en_, its in HERRAMIENTAS)
    hab = HABILIDADES[lang]
    def fila(items, extra=''):
        li = ''.join(f'<li>{esc(x)}</li>' for x in items)
        return f'<div class="mq-row {extra}"><div class="mq-r"><ul>{li}</ul><ul aria-hidden="true">{li}</ul></div></div>'
    skills = fila(hab[0::2], 'a') + fila(hab[1::2], 'b')
    return f'''<section class="pantalla" id="formacion" data-nombre="{esc(t['edu_h'])}" data-nav="sobre"><div class="wrap"><div class="form-top"><div class="edu rev"><h2>{esc(t['edu_h'])}</h2><div class="panel edu-panel"><p class="edu-y">{anio}</p><div><h3>{esc(g_en if en else g_es)}</h3><p class="emp">{esc(u)}</p><p class="nota">{esc(lugar)}</p></div></div></div>
<div class="rev" style="--d:.15s"><h2>{esc(t['tools_h'])}</h2><div class="herr">{herr}</div></div></div></div>
<div class="skills-blk"><div class="wrap"><h2>{esc(t['skills_h'])}</h2></div><div class="mq" aria-label="{esc(t['skills_h'])}">{skills}</div></div></section>'''


def contacto_seccion(lang, aqui, tag='h2'):
    t = UI[lang]
    et = {'es': ('Correo', 'Escríbeme directo'), 'en': ('Email', 'Write to me directly')}[lang]
    return f'''<section class="pantalla" id="contacto" data-nombre="{esc(t['secciones'][5])}" data-nav="contacto"><div class="wrap"><div class="dos contacto-grid"><div class="rev"><{tag} class="gigante-m">{esc(t['contacto_cta'])}</{tag}><p class="lead">{esc(t['contacto_lead'])}</p>
<div class="btns" style="margin-top:var(--e6)">{botones_contacto(lang)}</div></div>
<div class="rev" style="--d:.15s"><ul class="datos panel"><li>{ico('correo')}<div><strong>{esc(t['correo'])}</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
<li>{ico('linkedin')}<div><strong>LinkedIn</strong><a href="{REDES[1][1]}" target="_blank" rel="noopener">Mariana Boscán</a></div></li>
<li>{ico('whatsapp')}<div><strong>{esc(t['whatsapp'])}</strong><a href="{WHATSAPP}" target="_blank" rel="noopener">+57 324 359 1199</a></div></li>
<li>{ico('behance')}<div><strong>Behance</strong><a href="{REDES[2][1]}" target="_blank" rel="noopener">@marianaboscan</a></div></li></ul></div></div></div></section>'''


def sobre_teaser(lang, aqui):
    t = UI[lang]
    ds = ''.join(f'<li>{ico(ic)}<div><strong>{esc(k)}</strong>{esc(v)}</div></li>' for (k, v), ic in zip(t['datos'], ('pin', 'birrete', 'maleta', 'capas')))
    return f'''<section class="pantalla fondo-suave" id="sobre" data-nombre="{esc(t['secciones'][3])}" data-nav="sobre"><div class="wrap"><div class="dos">
<div class="sobre rev"><p class="etiqueta">{ico('estrella')}<span>{esc(HC[lang]['et_sobre'])}</span></p><h2 style="margin-bottom:var(--e6)">{esc(t['sobre_h2'])}</h2><p class="lead">{esc(t['sobre_resumen'])}</p>
<p class="btns"><a class="btn primario" href="{rel(aqui, ruta('sobre', lang))}">{esc(t['leer_mas'])} {ico('flecha')}</a></p></div>
<div class="panel rev" style="--d:.15s;align-self:center"><ul class="datos">{ds}</ul></div></div></div></section>'''


def experiencia_home(lang, aqui):
    h = HC[lang]; t = UI[lang]
    filas = ''
    for n, (anios, ces, cen, emp, des, den) in enumerate(EXPERIENCIA):
        cargo = ces if lang == 'es' else cen
        actual = f'<span class="actual">{esc(h["actual"])}</span>' if n == 0 else ''
        desc = des if lang == 'es' else den
        a = anios.replace("—", "— " + t["presente"]) if anios.endswith("—") else anios
        filas += (f'<li class="tl-it" style="--k:{n}"><span class="tl-dot" aria-hidden="true"></span><article class="tl-card"><span class="anios">{esc(a)}</span>'
                  f'<h3>{esc(cargo)}</h3>{actual}<p class="emp">{esc(emp)}</p><p class="desc">{esc(desc)}</p></article></li>')
    return f'''<section class="exph" id="experiencia" data-nombre="{esc(t['exp_h'])}" data-nav="experiencia"><div class="tl-pin"><div class="wrap">
<div class="exph-cab rev"><div><p class="etiqueta">{ico('estrella')}<span>{esc(h['et_exp'])}</span></p><h2>{esc(h['exp_titulo'])}</h2></div></div></div>
<div class="tl-view wrap"><ol class="tl"><li class="tl-rail" aria-hidden="true"><i class="tl-fill"></i></li>{filas}</ol></div></div></section>'''


def fab(lang):
    h = HC[lang]; it = h['fab_items']
    chat = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.500h16v10.500H9.500L5.500 19.500V16H4z"/></svg>'
    cerrar = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
    return f'''<div class="fab" id="fab"><ul class="fab-menu" id="fab-menu">
<li style="--k:2"><a href="{REDES[1][1]}" target="_blank" rel="noopener">{ico('linkedin')}<span>{esc(it[2])}</span></a></li>
<li style="--k:1"><a href="{WHATSAPP}" target="_blank" rel="noopener">{ico('whatsapp')}<span>{esc(it[1])}</span></a></li>
<li style="--k:0"><a href="mailto:{EMAIL}">{ico('correo')}<span>{esc(it[0])}</span></a></li></ul>
<button type="button" class="fab-btn" aria-expanded="false" aria-controls="fab-menu" aria-label="{esc(h['fab_t'])}"><span class="fab-lbl">{esc(h['fab'])}</span><i class="chip"><span class="a">{chat}</span><span class="b">{cerrar}</span></i></button></div>
<script>(function(){{var f=document.getElementById('fab'),b=f.querySelector('.fab-btn');function c(){{f.classList.remove('abierto');b.setAttribute('aria-expanded','false')}}
b.addEventListener('click',function(e){{e.stopPropagation();var o=f.classList.toggle('abierto');b.setAttribute('aria-expanded',o?'true':'false')}});
document.addEventListener('click',function(e){{if(!f.contains(e.target))c()}});document.addEventListener('keydown',function(e){{if(e.key==='Escape')c()}})}})();</script>'''


def estadisticas(lang):
    n = len(D['proyectos']) + len(NUEVOS)
    items = ''.join(f'<li><b>{esc(v.replace("{n}", str(n)))}</b><span>{esc(k)}</span></li>' for v, k in HC[lang]['stats'])
    return f'<section class="stats" aria-label="{esc(HC[lang]["et_sobre"])}"><div class="wrap"><ul>{items}</ul></div></section>'


def cta_home(lang, aqui):
    t = UI[lang]; u = SERV_UI[lang]
    return f'''<section class="pantalla" id="contacto" data-nombre="{esc(t['secciones'][5])}" data-nav="contacto"><div class="wrap"><div class="panel cta-final rev"><p class="etiqueta">{ico('estrella')}<span>{esc(HC[lang]['et_contacto'])}</span></p><h2 class="gigante-m" style="margin-bottom:0">{esc(t['contacto_cta'])}</h2><p class="lead">{esc(t['contacto_lead'])}</p>
<div class="btns">{botones_contacto(lang)}</div></div></div></section>'''


def pagina_inicio(lang):
    t = UI[lang]; aqui = ruta('inicio', lang)
    cuerpo = hero2(lang, aqui) + galeria(lang, aqui) + estadisticas(lang) + (servicios_home(lang, aqui) if MOSTRAR_SERVICIOS else '') + bio(lang, aqui) + experiencia_home(lang, aqui) + formacion(lang, aqui) + cta_home(lang, aqui)
    return pagina(lang, aqui, 'inicio', t['titulo_sitio'], t['desc_sitio'], cuerpo, ruta('inicio', 'en' if lang == 'es' else 'es'),
                  extra_head=esquema_home(lang) + '<link rel="preconnect" href="https://cdn.myportfolio.com" crossorigin>\n', extra_body=f'<script src="{rel(aqui, "animar.js")}" defer></script>', body_class='home inicio-pg')


def pagina_sobre(lang):
    t = UI[lang]; aqui = ruta('sobre', lang)
    cuerpo = cine(lang, aqui, 'h1') + bio(lang, aqui) + experiencia(lang) + formacion(lang, aqui) + cta_final(lang, aqui)
    return pagina(lang, aqui, 'sobre', f"{t['nav']['sobre']} — Mariana Boscán", t['sobre_resumen'], cuerpo, ruta('sobre', 'en' if lang == 'es' else 'es'),
                  extra_body=f'<script src="{rel(aqui, "animar.js")}" defer></script>', body_class='home')


def pagina_contacto(lang):
    t = UI[lang]; aqui = ruta('contacto', lang)
    cuerpo = contacto_seccion(lang, aqui, 'h1')
    return pagina(lang, aqui, 'contacto', f"{t['nav']['contacto']} — Mariana Boscán", t['contacto_lead'], cuerpo, ruta('contacto', 'en' if lang == 'es' else 'es'),
                  extra_body=f'<script src="{rel(aqui, "animar.js")}" defer></script>')


# ---------- briefs por servicio (solo accesibles por URL) ----------
def ruta_brief(k, lang):
    return ('es/brief/' if lang == 'es' else 'brief/') + BRIEFS[k]['slug'][0 if lang == 'es' else 1] + '/'


BRIEF_UI = {
 'es': dict(h_lead='Cuéntame sobre tu proyecto. Responde lo que puedas; lo que no sepas, déjalo en blanco y lo resolvemos juntos. Toma unos 5 a 10 minutos.',
            enviar='Enviar brief', enviando='Enviando…', ok_t='¡Gracias! Recibí tu brief', ok_p='Lo voy a revisar con calma y te escribo pronto al correo que dejaste. También te envié una copia de confirmación.',
            inv='Revisa los campos marcados como obligatorios (nombre, correo y las preguntas con asterisco).', err='No pude enviar el brief. Escríbeme por correo o WhatsApp, por favor.', lim='Has enviado varios formularios seguidos. Intenta de nuevo más tarde.',
            priv='Uso esta información solo para preparar tu propuesta. Si quieres que la borre, escríbeme.', req='obligatorio', elegir='Selecciona una opción'),
 'en': dict(h_lead='Tell me about your project. Answer what you can; leave blank what you’re unsure about and we’ll figure it out together. It takes about 5 to 10 minutes.',
            enviar='Send brief', enviando='Sending…', ok_t='Thank you! I got your brief', ok_p='I’ll review it carefully and write to you soon at the email you left. I also sent you a confirmation copy.',
            inv='Please check the required fields (name, email and the questions marked with an asterisk).', err='I couldn’t send the brief. Please email or WhatsApp me.', lim='You’ve sent several forms in a row. Please try again later.',
            priv='I only use this information to prepare your proposal. If you’d like it deleted, just let me know.', req='required', elegir='Select an option'),
}


def campo_html(c, lang, pref):
    i = 0 if lang == 'es' else 1
    lab = c['es'] if lang == 'es' else c['en']
    nm = pref + c['k']; t = c['t']
    star = ' <span class="req" aria-hidden="true">*</span>' if c['req'] else ''
    ay = f'<p class="ayuda" id="{nm}-a">{esc(c["ayuda"][i])}</p>' if c['ayuda'] else ''
    desc = f' aria-describedby="{nm}-a"' if c['ayuda'] else ''
    rq = ' required' if c['req'] else ''
    if t in ('radio', 'checkbox'):
        ops = ''.join(f'<label class="opc"><input type="{t}" name="{nm}" value="{esc(o[i])}"><span>{esc(o[i])}</span></label>' for o in c['ops'])
        return f'<fieldset class="campo grupo" data-k="{nm}" data-t="{t}" data-req="{int(c["req"])}"><legend>{esc(lab)}{star}</legend>{ay}<div class="opciones">{ops}</div></fieldset>'
    if t == 'select':
        ops = f'<option value="">{esc(BRIEF_UI[lang]["elegir"])}</option>' + ''.join(f'<option value="{esc(o[i])}">{esc(o[i])}</option>' for o in c['ops'])
        ctl = f'<div class="sel"><select id="{nm}" name="{nm}"{rq}{desc}>{ops}</select>{ICONO_CHEV}</div>'
    elif t == 'textarea':
        ctl = f'<textarea id="{nm}" name="{nm}" rows="3" maxlength="3000"{rq}{desc}></textarea>'
    else:
        ac = {'nombre': 'name', 'email': 'email', 'telefono': 'tel'}.get(c['k'], 'off')
        ctl = f'<input id="{nm}" name="{nm}" type="{t}" maxlength="300" autocomplete="{ac}"{rq}{desc}>'
    return f'<div class="campo" data-k="{nm}" data-t="{t}" data-req="{int(c["req"])}"><label for="{nm}">{esc(lab)}{star}</label>{ay}{ctl}</div>'


def pagina_brief(k, lang):
    B = BRIEFS[k]; b = BRIEF_UI[lang]; i = 0 if lang == 'es' else 1; aqui = ruta_brief(k, lang)
    titulo = B['titulo'][i]
    secs = ''
    for n, (ts, tn, campos) in enumerate(B['secciones']):
        secs += f'<section class="panel bloque"><h2 class="h3"><span class="num">{n + 1:02d}</span> {esc(ts if lang == "es" else tn)}</h2>' + ''.join(campo_html(c, lang, 'f_') for c in campos) + '</section>'
    cuerpo = f'''<section class="cab-pagina wrap"><h1 style="font-size:clamp(36px,6vw,72px)">{esc(titulo)}</h1><p class="lead">{esc(b['h_lead'])}</p></section>
<section class="wrap"><form id="brief" class="brief-form" novalidate>{secs}
<div class="trampa" aria-hidden="true"><label>Web <input type="text" name="hp_web" tabindex="-1" autocomplete="off"></label></div>
<div class="enviar-fila"><button class="btn primario" type="submit" id="enviar">{esc(b['enviar'])}</button><p class="nota">{esc(b['priv'])}</p></div><div id="estado" role="status" aria-live="polite"></div></form>
<div id="gracias" class="panel cta-final" hidden><h2>{esc(b['ok_t'])}</h2><p class="lead">{esc(b['ok_p'])}</p></div></section>'''
    msgs = json.dumps({'inv': b['inv'], 'err': b['err'], 'lim': b['lim'], 'enviando': b['enviando'], 'enviar': b['enviar']}, ensure_ascii=False)
    js = f'''<script>
(function(){{
var ENDPOINT={json.dumps(ENDPOINT)},M={msgs},IDIOMA={json.dumps(lang)},SERVICIO={json.dumps(titulo, ensure_ascii=False)},CLAVE={json.dumps(k)};
var f=document.getElementById('brief'),b=document.getElementById('enviar'),s=document.getElementById('estado');
function aviso(t){{s.innerHTML='';var p=document.createElement('p');p.className='aviso error';p.textContent=t;s.appendChild(p);}}
function valor(c){{var t=c.getAttribute('data-t');
 if(t==='radio'||t==='checkbox'){{return Array.prototype.map.call(c.querySelectorAll('input:checked'),function(x){{return x.value}}).join(', ');}}
 var e=c.querySelector('input,select,textarea');return e?e.value.trim():'';}}
function etiqueta(c){{var l=c.querySelector('label,legend');return l?l.textContent.replace(/\\s*\\*\\s*$/,'').trim():'';}}
f.addEventListener('submit',function(e){{e.preventDefault();
 var campos=f.querySelectorAll('[data-k]'),resp=[],falta=null,d={{formulario:'brief',idioma:IDIOMA,servicio:SERVICIO,servicio_clave:CLAVE,web:f.hp_web.value}};
 Array.prototype.forEach.call(campos,function(c){{var v=valor(c),k=c.getAttribute('data-k');c.classList.remove('falta');
  if(c.getAttribute('data-req')==='1'&&!v){{c.classList.add('falta');if(!falta)falta=c;}}
  if(k==='f_nombre')d.nombre=v;if(k==='f_email')d.email=v;if(k==='f_telefono')d.telefono=v;
  if(v)resp.push({{p:etiqueta(c),r:v}});}});
 if(!d.email||!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(d.email)){{var ce=f.querySelector('[data-k="f_email"]');ce.classList.add('falta');if(!falta)falta=ce;}}
 if(falta){{aviso(M.inv);falta.scrollIntoView({{behavior:'smooth',block:'center'}});return;}}
 if(ENDPOINT.indexOf('http')!==0){{aviso(M.err);return;}}
 d.respuestas=resp;b.disabled=true;b.textContent=M.enviando;
 fetch(ENDPOINT,{{method:'POST',headers:{{'Content-Type':'text/plain;charset=utf-8'}},body:JSON.stringify(d)}})
 .then(function(r){{return r.json()}}).then(function(r){{
  if(r&&r.ok){{f.hidden=true;var g=document.getElementById('gracias');g.hidden=false;g.scrollIntoView({{behavior:'smooth',block:'center'}});}}
  else{{aviso(r&&r.error==='limite'?M.lim:(r&&r.error==='datos_invalidos'?M.inv:M.err));}}
 }}).catch(function(){{aviso(M.err);}}).then(function(){{b.disabled=false;b.textContent=M.enviar;}});
}});}})();
</script>'''
    return pagina(lang, aqui, 'servicios', f'{titulo} | Mariana Boscán', b['h_lead'], cuerpo, ruta_brief(k, 'en' if lang == 'es' else 'es'),
                  extra_body=js, body_class='brief', robots='noindex,nofollow,noarchive')


EXPERIENCIA = [  # (años, cargo ES, cargo EN, empresa, descripción ES, descripción EN)
 ('2026 —', 'Líder del equipo de diseño', 'Design Team Lead', 'Partner in Publishing', 'Lidero proyectos de diseño para varias cuentas, con identidad de marca, material de marketing, presentaciones y contenido digital. Trabajo con marketing y copywriting y apoyo sistemas de diseño y accesibilidad.', 'I lead design projects across multiple client accounts, creating branding assets, marketing collateral, presentations and digital content. I work with marketing and copywriting teams and support design systems and accessibility standards.'),
 ('2024 — 2026', 'Diseñadora gráfica y web', 'Graphic & Web Designer', 'Partner in Publishing', 'Sitios web, landing pages y activos digitales para marcas clientes, junto con material de marketing, contenido para redes y presentaciones alineados con sus guías de marca, aplicando buenas prácticas de accesibilidad (WCAG 2.1 AA).', 'Websites, landing pages and digital assets for client brands, plus marketing collateral, social content and presentations aligned with brand guidelines, applying accessibility best practices (WCAG 2.1 AA).'),
 ('2021 — 2024', 'Diseñadora gráfica y web', 'Graphic & Web Designer', 'Naranja Brand', 'Identidades visuales y materiales de marca alineados con los objetivos del cliente, y piezas digitales y publicitarias para distintos canales.', 'Visual identities and branding materials aligned with client objectives, plus digital and advertising assets across multiple channels.'),
 ('2020 — 2023', 'Diseñadora gráfica y web', 'Graphic & Web Designer', 'Magic Commerce', 'Activos de marca y materiales digitales para clientes; diseño y desarrollo de sitios web y tiendas online que combinan diseño visual y funcionalidad.', 'Branding assets and digital materials for clients; design and development of websites and e-commerce experiences combining visual design with functionality.'),
 ('2018 — 2021', 'Diseñadora gráfica y web', 'Graphic & Web Designer', 'Nevato', 'Piezas visuales para campañas de publicidad y marketing digital, y apoyo en proyectos web y materiales creativos para marcas clientes.', 'Visual assets for advertising and digital marketing campaigns, plus support on web design projects and creative materials for client brands.'),
 ('2017 — 2018', 'Diseñadora gráfica', 'Graphic Designer', 'Staff Leverage', 'Materiales de diseño gráfico para iniciativas de marketing y comunicación.', 'Graphic design materials supporting marketing and communication initiatives.'),
]
EDUCACION = ('Universidad Privada Dr. Rafael Belloso Chacín', 'Licenciatura en Diseño Gráfico', 'Bachelor’s Degree in Graphic Design', 'Maracaibo, Venezuela', '2018')
HERRAMIENTAS = [  # (grupo ES, grupo EN, [(nombre, archivo)])
 ('Diseño y creatividad', 'Design & Creative', [('Figma', 'figma'), ('Adobe Illustrator', 'illustrator'), ('Adobe Photoshop', 'photoshop'), ('Adobe InDesign', 'indesign'), ('Adobe Lightroom', 'lightroom'), ('After Effects', 'aftereffects')]),
 ('Web y e-commerce', 'Web & E-commerce', [('Shopify', 'shopify'), ('WordPress', 'wordpress')]),
 ('Marketing y contenido', 'Marketing & Content', [('Mailchimp', 'mailchimp'), ('CapCut', 'capcut'), ('Canva', 'canva')]),
 ('IA y productividad', 'AI & Productivity', [('Claude', 'claude'), ('ChatGPT', 'chatgpt'), ('Adobe Firefly', 'firefly'), ('Gemini', 'gemini'), ('ClickUp', 'clickup'), ('Slack', 'slack')]),
]
HABILIDADES = {'es': ['Identidad de marca', 'Branding', 'Dirección de arte', 'Manuales de marca', 'Diseño digital', 'Diseño web', 'Diseño para e-commerce', 'Landing pages', 'Sistemas de diseño', 'Diseño editorial', 'Diseño para redes sociales', 'Infografías', 'White papers', 'Annual reports', 'Diseño de ads', 'Email marketing', 'Presentaciones', 'Diseño con IA', 'Accesibilidad digital (WCAG 2.1 AA)'],
 'en': ['Brand Identity', 'Branding', 'Art Direction', 'Brand Guidelines', 'Digital Design', 'Web Design', 'E-commerce Design', 'Landing Pages', 'Design Systems', 'Editorial Design', 'Social Media Design', 'Infographics', 'White Papers', 'Annual Reports', 'Ad Design', 'Email Marketing', 'Presentations', 'AI Design', 'Digital Accessibility (WCAG 2.1 AA)']}


FILTRO_JS = '''<script>
(function(){var bs=document.querySelectorAll('.filtros button'),ul=document.querySelector('.rejilla'),lis=document.querySelectorAll('.rejilla li');
bs.forEach(function(b){b.addEventListener('click',function(){var c=b.getAttribute('data-f');
bs.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});ul.classList.toggle('filtrada',c!=='todos');
lis.forEach(function(li){li.hidden=!(c==='todos'||(' '+li.getAttribute('data-cat')+' ').indexOf(' '+c+' ')>-1)});});});})();
</script>'''


INT_JS = lambda aqui: f'<script src="{rel(aqui, "interno.js")}" defer></script>'


def cab_int(eyebrow, h1, lead='', extra=''):
    ld = f'<p class="lead">{lead}</p>' if lead else ''
    return f'''<section class="cab-int wrap"><p class="etiqueta">{ico('estrella')}<span>{esc(eyebrow)}</span></p><h1>{h1}</h1>{ld}{extra}</section>'''


def cta_interna(lang, aqui):
    return cta_home(lang, aqui).replace(' data-nav="contacto"', '').replace(' data-nombre=', ' data-x=')


def pagina_cv():
    lang = 'en'; aqui = 'cv-mariana-boscan/'
    cab = cab_int('Curriculum vitae', 'Mariana <span class="serif">Boscán</span>', 'Senior Graphic Designer based in Bogotá, Colombia',
        extra='''<p class="btns"><a class="btn primario" href="Mariana-Boscan-CV.pdf" download><span>Download PDF</span><i class="chip">''' + ico('flecha') + '''</i></a><a class="btn" href="Mariana-Boscan-CV.pdf" target="_blank" rel="noopener"><span>Open full size</span></a><a class="btn" href="../work/"><span>View my portfolio</span></a></p>''')
    hoja = '<section class="wrap hoja-int"><div class="hoja rev"><img src="cv-preview.webp" width="2040" height="3370" alt="Curriculum vitae of Mariana Boscán, Senior Graphic Designer. Download the PDF for the full text."></div></section>'
    return pagina(lang, aqui, 'cv', 'Mariana Boscán — CV', 'Curriculum vitae of Mariana Boscán, Senior Graphic Designer.', cab + hoja + cta_interna(lang, aqui), 'es/',
                  extra_body=INT_JS(aqui), body_class='interna cv-int', robots='noindex,nofollow,noarchive,nosnippet')


def pagina_portafolio(lang):
    t = UI[lang]; aqui = ruta('portafolio', lang)
    usadas = []
    for c in [META[p['s']][3] for p in D['proyectos']] + [c for e in NUEVOS for c in categorias_de(e)]:
        if c not in usadas: usadas.append(c)
    orden = [c for c in CATS if c in usadas]
    filtros = f'<button type="button" data-f="todos" aria-pressed="true">{esc(t["todos"])}</button>' + ''.join(
        f'<button type="button" data-f="{c}" aria-pressed="false">{esc(CATS[c][0 if lang == "es" else 1])}</button>' for c in orden)
    cards = ''.join(tarjeta_ext(e, lang, i + 1, aqui) for i, e in enumerate(NUEVOS)) + ''.join(tarjeta(p, lang, aqui, len(NUEVOS) + i + 1) for i, p in enumerate(D['proyectos']))
    cuerpo = cab_int(HC[lang]['et_obra'], h1_html(t['port_h1']), esc(t['port_lead'])) + f'''
<section class="wrap lista-int"><div class="filtros" role="group" aria-label="{esc(t['cat_nombre'])}" id="filtros" hidden>{filtros}</div>
<ul class="rejilla">{cards}</ul>
<p class="btns centrado"><a class="btn" href="https://www.behance.net/marianaboscan" target="_blank" rel="noopener"><span>{esc(t['ver_behance'])}</span><i class="chip">{ico('flecha')}</i></a></p></section>
<script>document.getElementById("filtros").hidden=false</script>''' + cta_interna(lang, aqui)
    return pagina(lang, aqui, 'portafolio', f"{t['nav']['portafolio']} — Mariana Boscán", t['port_lead'], cuerpo,
                  ruta('portafolio', 'en' if lang == 'es' else 'es'), extra_body=FILTRO_JS + INT_JS(aqui), body_class='interna')



def pagina_proyecto(i, lang):
    t = UI[lang]; ps = D['proyectos']; p = ps[i]; aqui = proy_ruta(p['s'], lang)
    marca, des, den, cat = META[p['s']]
    desc = des if lang == 'es' else den
    piezas = []
    for m in p['m']:
        if m[0] == 'i':
            piezas.append(f'<div class="pieza" style="aspect-ratio:100/{m[2]}"><img src="{IMG(m[1], aqui)}" alt="{esc(marca)} — {esc(desc)}" loading="{"eager" if not piezas else "lazy"}" decoding="async"></div>')
        else:
            piezas.append(f'<div class="pieza" style="aspect-ratio:16/9"><iframe src="https://www-ccv.adobe.io/v1/player/ccv/{m[1]}/embed?bgcolor=%23191919&amp;lazyLoading=true&amp;api_key=BehancePro2View" title="{esc(marca)} — {esc(desc)}" loading="lazy" allow="fullscreen; autoplay" allowfullscreen></iframe></div>')
    ant, sig = ps[i - 1], ps[(i + 1) % len(ps)]
    cuerpo = cab_int(CATS[cat][0 if lang == 'es' else 1], esc(marca), esc(desc)) + f'''
<section class="wrap pila-int"><div class="pila">{''.join(piezas)}</div>
<div class="pager"><a class="btn" href="{rel(aqui, proy_ruta(ant['s'], lang))}">← {esc(t['anterior'])}</a><a class="btn" href="{rel(aqui, ruta('portafolio', lang))}">{esc(t['volver'])}</a><a class="btn" href="{rel(aqui, proy_ruta(sig['s'], lang))}">{esc(t['siguiente'])} →</a></div></section>''' + cta_interna(lang, aqui)
    otra = proy_ruta(p['s'], 'en' if lang == 'es' else 'es')
    return pagina(lang, aqui, 'portafolio', f'{marca} — {desc} | Mariana Boscán', f'{marca}: {desc}. {t["desc_sitio"]}'[:250], cuerpo, otra, og_img=BASE + p['c'][1], extra_body=INT_JS(aqui), body_class='interna')


DESCARGADOR = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Descargar imágenes del portafolio</title>
<style>body{font:16px/1.6 system-ui,sans-serif;max-width:560px;margin:48px auto;padding:0 20px;color:#14141e}button{font:inherit;font-weight:600;padding:12px 24px;border-radius:999px;border:0;background:#afb5e7;cursor:pointer}progress{width:100%;height:14px;margin:20px 0}li{margin:6px 0}</style></head><body>
<h1>Descargar las imágenes</h1>
<p>Este archivo baja todas las imágenes de tu portafolio actual (Adobe) y las guarda en un solo ZIP. Así el sitio nuevo ya no depende de Adobe.</p>
<ol><li>Pulsa el botón y espera (son __N__ archivos).</li><li>Se descarga <b>imagenes.zip</b>. Descomprímelo dentro de <b>sitio/src/img/</b>.</li><li>Ejecuta de nuevo <code>python3 build.py</code>.</li></ol>
<button id="go">Descargar imágenes</button><progress id="p" value="0" max="__N__" hidden></progress><p id="s" role="status"></p>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script>
var BASE="__BASE__",FILES=__FILES__;
document.getElementById('go').onclick=async function(){var b=this;b.disabled=true;var p=document.getElementById('p'),s=document.getElementById('s');p.hidden=false;
var zip=new JSZip(),ok=0,fail=[];
for(var i=0;i<FILES.length;i++){var f=FILES[i];try{var r=await fetch(BASE+f);if(!r.ok)throw 0;zip.file(f.split('?')[0],await r.blob());ok++}catch(e){fail.push(f)}p.value=i+1;s.textContent=(i+1)+' / '+FILES.length}
var blob=await zip.generateAsync({type:'blob'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='imagenes.zip';a.click();
s.textContent='Listo: '+ok+' imágenes.'+(fail.length?' No se pudieron bajar '+fail.length+'. Avísame.':'');b.disabled=false};
</script></body></html>
'''


def descargador():
    archivos = [FOTO]
    for p in D['proyectos']:
        archivos += p['c']
        archivos += [m[1] for m in p['m'] if m[0] == 'i']
    out = DESCARGADOR.replace('__N__', str(len(archivos))).replace('__BASE__', BASE).replace('__FILES__', json.dumps(archivos))
    open(os.path.join(AQUI, 'descargar-imagenes.html'), 'w', encoding='utf-8').write(out)


def escribir(ruta_rel, contenido):
    p = os.path.join(DIST, ruta_rel, 'index.html') if (ruta_rel == '' or ruta_rel.endswith('/')) else os.path.join(DIST, ruta_rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if PREVIEW:
        import re
        contenido = re.sub(r'(<a [^>]*?href=")([^"#:]*/)(#[^"]*)?(")', r'\1\2index.html\3\4', contenido)
    open(p, 'w', encoding='utf-8').write(contenido)


def redireccion(desde, hacia):
    if hacia.startswith('#'): hacia = ('es/' if desde.startswith('es/') else '') + hacia
    base, _, h = hacia.partition('#')
    destino = rel(desde, base) + ('#' + h if h else '')
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Mariana Boscán</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{url_abs(base)}"><meta http-equiv="refresh" content="0; url={destino}">
<script>location.replace({json.dumps(destino)})</script></head><body><a href="{destino}">{destino}</a></body></html>'''


def main():
    if os.path.isdir(DIST): shutil.rmtree(DIST)
    os.makedirs(DIST)
    for d in ('assets', 'fonts'): shutil.copytree(os.path.join(AQUI, 'src', d), os.path.join(DIST, d))
    shutil.copy(os.path.join(AQUI, 'src', 'estilos.css'), os.path.join(DIST, 'styles.css'))
    shutil.copy(os.path.join(AQUI, 'src', 'animar.js'), DIST)
    shutil.copy(os.path.join(AQUI, 'src', 'interno.js'), DIST)
    os.makedirs(os.path.join(DIST, 'cierre'), exist_ok=True)
    shutil.copy(os.path.join(AQUI, 'src', 'cierre.html'), os.path.join(DIST, 'cierre', 'index.html'))
    os.makedirs(os.path.join(DIST, 'cv-mariana-boscan'), exist_ok=True)   # CV: fuera del sitemap y noindex
    for f in ('Mariana-Boscan-CV.pdf', 'cv-preview.webp'): shutil.copy(os.path.join(AQUI, 'src', 'cv', f), os.path.join(DIST, 'cv-mariana-boscan', f))
    escribir('cv-mariana-boscan/', pagina_cv())
    os.makedirs(os.path.join(DIST, 'cv-mariana-hkxmcj9e'), exist_ok=True)   # enlace anterior: redirige al nuevo
    open(os.path.join(DIST, 'cv-mariana-hkxmcj9e', 'index.html'), 'w').write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>CV</title><meta http-equiv="refresh" content="0; url=../cv-mariana-boscan/"><a href="../cv-mariana-boscan/">CV</a>')
    if os.path.isdir(SRC_IMG): shutil.copytree(SRC_IMG, os.path.join(DIST, 'img'))
    descargador()
    urls = []
    for lang in ('es', 'en'):
        for clave, fn in (('inicio', pagina_inicio), ('servicios', pagina_servicios), ('portafolio', pagina_portafolio), ('sobre', pagina_sobre), ('contacto', pagina_contacto)):
            if clave == 'servicios' and not MOSTRAR_SERVICIOS: continue
            if clave in ('sobre', 'contacto'):   # todo vive en el home: la página vieja redirige a su sección
                escribir(ruta(clave, lang), redireccion(ruta(clave, lang), ruta('inicio', lang) + '#' + clave)); continue
            escribir(ruta(clave, lang), fn(lang)); urls.append(ruta(clave, lang))
        for k in ORDEN:
            if MOSTRAR_SERVICIOS:
                escribir(ruta_brief(k, lang), pagina_brief(k, lang))   # no van al sitemap ni tienen enlaces
                escribir(ruta_serv(k, lang), pagina_servicio(k, lang)); urls.append(ruta_serv(k, lang))
            else:   # se conservan las URLs viejas, pero llevan al portafolio (sin indexar)
                destino = ruta('portafolio', lang)
                escribir(ruta_brief(k, lang), redireccion(ruta_brief(k, lang), destino))
                escribir(ruta_serv(k, lang), redireccion(ruta_serv(k, lang), destino))
        if not MOSTRAR_SERVICIOS: escribir(ruta('servicios', lang), redireccion(ruta('servicios', lang), ruta('portafolio', lang)))
        for i, p in enumerate(D['proyectos']):
            escribir(proy_ruta(p['s'], lang), pagina_proyecto(i, lang)); urls.append(proy_ruta(p['s'], lang))
        for e in NUEVOS:
            if e.get('imgs'):
                escribir(proy_ruta(e['slug'], lang), pagina_proyecto_ext(e, lang)); urls.append(proy_ruta(e['slug'], lang))
    for viejo, nuevo in REDIRECCIONES.items(): escribir(viejo, redireccion(viejo, nuevo))
    # direcciones anteriores (español en la raíz, inglés en /en/) -> nuevas, para no perder enlaces
    nuevas = set(urls)
    for u in list(urls):
        viejo = u[3:] if u.startswith('es/') else 'en/' + u
        if viejo and viejo not in nuevas and not os.path.exists(os.path.join(DIST, viejo, 'index.html')):
            escribir(viejo, redireccion(viejo, u))
    for k in ORDEN:
        v = SERVICIOS[k]['slug'][0] + '/'
        if not os.path.exists(os.path.join(DIST, v, 'index.html')): escribir(v, redireccion(v, ruta('portafolio', 'es')))
    for v, n in (('servicios/', ruta('portafolio', 'es')), ('en/services/', ruta('portafolio', 'en'))):
        if not os.path.exists(os.path.join(DIST, v, 'index.html')): escribir(v, redireccion(v, n))
    # 404 (GitHub Pages la usa sola)
    escribir('404.html', pagina('es', '', '404', 'No encontrada · Not found — Mariana Boscán', 'Página no encontrada',
        cab_int('Error 404', 'Esta página <span class="serif">no existe</span>', 'This page doesn’t exist.', extra='<p class="btns"><a class="btn primario" href="/"><span>Home</span></a><a class="btn" href="/es/"><span>Inicio (ES)</span></a></p>'), '', body_class='interna'))
    hoy = date.today().isoformat()
    sm = ''.join(f'<url><loc>{url_abs(u)}</loc><lastmod>{hoy}</lastmod></url>\n' for u in urls)
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITIO}/sitemap.xml\n')
    open(os.path.join(DIST, '.nojekyll'), 'w').write('')
    open(os.path.join(DIST, 'CNAME'), 'w').write(SITIO.split('//')[1] + '\n')
    print(f'{len(urls)} páginas generadas en {DIST}')


if __name__ == '__main__':
    main()

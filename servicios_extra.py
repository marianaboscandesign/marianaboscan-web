# Contenido adicional de las páginas de servicio (más visual): para quién es, entregables y una frase destacada.
# Las imágenes (opcionales) van en src/img/servicios/<clave>-hero.webp (4:5) y <clave>-banda.webp (16:7).

EXTRA = {
 'branding': dict(
  es=dict(frase='Una marca clara se reconoce, se recuerda y se elige.',
          para=[('Emprendedores que empiezan', 'Necesitas una identidad profesional desde el primer día para que tu marca se tome en serio.'),
                ('Negocios que quieren renovarse', 'Tu marca ya existe, pero se ve desactualizada o inconsistente y quieres ordenarla.'),
                ('Agencias y equipos', 'Necesitas apoyo de diseño para las identidades de tus clientes, con criterio y entregas ordenadas.')],
          entregables=['Logo en versión principal, secundaria e isotipo', 'Archivos AI, SVG, PNG y PDF', 'Versiones a color, en negro y en blanco', 'Paleta de color y tipografías', 'Manual de marca en PDF', 'Ejemplos de aplicación de la marca']),
  en=dict(frase='A clear brand gets recognized, remembered and chosen.',
          para=[('Entrepreneurs getting started', 'You need a professional identity from day one so your brand is taken seriously.'),
                ('Businesses ready to refresh', 'Your brand exists, but it looks outdated or inconsistent and you want to bring order to it.'),
                ('Agencies and teams', 'You need design support for your clients’ identities, with judgment and organized deliveries.')],
          entregables=['Logo in primary, secondary and symbol versions', 'AI, SVG, PNG and PDF files', 'Full-color, black and white versions', 'Color palette and typefaces', 'Brand guidelines in PDF', 'Brand application examples'])),
 'tiendas': dict(
  es=dict(frase='Una tienda clara convierte visitas en compras.',
          para=[('Marcas que empiezan a vender online', 'Quieres lanzar tu primera tienda con una base bien diseñada y fácil de administrar.'),
                ('Tiendas que no convierten', 'Recibes visitas, pero poca gente compra. Revisamos estructura y diseño para facilitar la compra.'),
                ('Catálogos que crecen', 'Necesitas colecciones, páginas y una navegación que escale contigo.')],
          entregables=['Tienda Shopify configurada y publicada', 'Diseño para celular y computador', 'Páginas clave: inicio, colección, producto y contacto', 'Carga inicial de productos (según lo acordado)', 'Guía básica para administrar tu tienda', 'Recomendaciones de mejora después del lanzamiento']),
  en=dict(frase='A clear store turns visits into purchases.',
          para=[('Brands starting to sell online', 'You want to launch your first store with a well-designed foundation that is easy to manage.'),
                ('Stores that don’t convert', 'You get visits but few purchases. We review structure and design to make buying easier.'),
                ('Growing catalogs', 'You need collections, pages and navigation that scale with you.')],
          entregables=['Shopify store set up and published', 'Design for mobile and desktop', 'Key pages: home, collection, product and contact', 'Initial product upload (as agreed)', 'Basic guide to manage your store', 'Post-launch improvement recommendations'])),
 'social': dict(
  es=dict(frase='Cuando tu contenido se ve coherente, tu marca se vuelve reconocible.',
          para=[('Marcas con contenido irregular', 'Publicas, pero cada pieza se ve distinta. Necesitas un sistema que lo unifique.'),
                ('Equipos con poco tiempo', 'Quieres plantillas editables para producir más rápido sin perder calidad.'),
                ('Lanzamientos y campañas', 'Tienes una fecha o una campaña y necesitas piezas coherentes con tu marca.')],
          entregables=['Plantillas editables (Canva o Figma)', 'Publicaciones y carruseles', 'Stories y portadas de destacadas', 'Piezas adaptadas a cada red', 'Guía rápida del sistema visual', 'Archivos listos para publicar']),
  en=dict(frase='When your content looks consistent, your brand becomes recognizable.',
          para=[('Brands with uneven content', 'You post, but every piece looks different. You need a system that ties it together.'),
                ('Teams short on time', 'You want editable templates to produce faster without losing quality.'),
                ('Launches and campaigns', 'You have a date or a campaign and need pieces consistent with your brand.')],
          entregables=['Editable templates (Canva or Figma)', 'Posts and carousels', 'Stories and highlight covers', 'Pieces adapted to each platform', 'Quick guide to the visual system', 'Files ready to publish'])),
 'web': dict(
  es=dict(frase='Un buen sitio web explica quién eres en pocos segundos.',
          para=[('Profesionales y marcas personales', 'Necesitas un sitio que te presente con claridad y genere confianza.'),
                ('Negocios y estudios', 'Quieres un sitio informativo con servicios, portafolio y contacto bien organizados.'),
                ('Sitios que hay que renovar', 'Tu web actual es lenta, confusa o no se ve bien en el celular.')],
          entregables=['Diseño de interfaz en Figma', 'Sitio desarrollado en WordPress o Shopify', 'Versión adaptada a celular, tablet y computador', 'Configuración básica de SEO', 'Formulario de contacto funcionando', 'Capacitación breve para editar el contenido']),
  en=dict(frase='A good website explains who you are in a few seconds.',
          para=[('Professionals and personal brands', 'You need a site that presents you clearly and builds trust.'),
                ('Businesses and studios', 'You want an informative site with services, portfolio and contact well organized.'),
                ('Sites that need a refresh', 'Your current site is slow, confusing or doesn’t look good on mobile.')],
          entregables=['Interface design in Figma', 'Site built in WordPress or Shopify', 'Version adapted to mobile, tablet and desktop', 'Basic SEO setup', 'Working contact form', 'Short training to edit your content'])),
 'editorial': dict(
  es=dict(frase='Una buena diagramación hace que el contenido se lea y se entienda.',
          para=[('Empresas con informes y reportes', 'Necesitas documentos claros y bien diagramados que transmitan seriedad.'),
                ('Marcas con piezas impresas', 'Flyers, brochures y catálogos que se vean profesionales y coherentes con tu marca.'),
                ('Equipos con presentaciones', 'Presentaciones y piezas digitales ordenadas, legibles y fáciles de compartir.')],
          entregables=['PDF final para imprenta y para pantalla', 'Archivos editables (InDesign o Canva)', 'Versión optimizada para compartir en digital', 'Sangrados y márgenes listos para imprenta', 'Plantilla reutilizable (si aplica)']),
  en=dict(frase='Good layout makes content easy to read and understand.',
          para=[('Companies with reports', 'You need clear, well-laid-out documents that convey professionalism.'),
                ('Brands with printed pieces', 'Flyers, brochures and catalogs that look professional and consistent with your brand.'),
                ('Teams with presentations', 'Presentations and digital pieces that are organized, legible and easy to share.')],
          entregables=['Final PDF for print and screen', 'Editable files (InDesign or Canva)', 'Version optimized for digital sharing', 'Bleeds and margins ready for print', 'Reusable template (if applicable)'])),
 'youtube': dict(
  es=dict(frase='Una miniatura clara es la primera invitación a ver tu video.',
          para=[('Creadores de contenido', 'Quieres miniaturas atractivas y consistentes que inviten a ver tus videos.'),
                ('Marcas con canal de YouTube', 'Tu canal necesita una imagen profesional y coherente con tu marca.'),
                ('Educadores y consultores', 'Tus videos explican cosas valiosas y necesitas miniaturas claras que lo transmitan.')],
          entregables=['Miniaturas en 1280 × 720 px (JPG o PNG)', 'Plantillas editables para tus próximos videos', 'Diseño legible también en tamaño pequeño', 'Estilo consistente con tu canal', 'Archivos listos para subir']),
  en=dict(frase='A clear thumbnail is the first invitation to watch your video.',
          para=[('Content creators', 'You want attractive, consistent thumbnails that invite people to watch your videos.'),
                ('Brands with a YouTube channel', 'Your channel needs a professional image consistent with your brand.'),
                ('Educators and consultants', 'Your videos explain valuable things and you need clear thumbnails that show it.')],
          entregables=['Thumbnails at 1280 × 720 px (JPG or PNG)', 'Editable templates for your next videos', 'Design that stays legible at small sizes', 'Style consistent with your channel', 'Files ready to upload'])),
}

# Prompts para generar con IA las imágenes de cada servicio (1 vertical 4:5 + 1 panorámica 16:7).
ESTILO = ('Editorial, minimal, soft studio lighting, clean composition, lots of breathing room, pastel lavender (#afb5e7), '
          'peach (#e9b8b1) and soft pink (#ffbfef) accents with deep ink navy (#14141e), subtle paper and fabric textures, '
          'photorealistic, no text, no logos, no real brands, no watermarks, no people’s faces.')
PROMPTS = {
 'branding': ('Top-down flat lay of a brand identity mockup on a soft lavender surface: a business card, letterhead, a tote bag and a small notebook with an abstract geometric monogram, shadows soft and natural.',
              'Wide panoramic scene of a designer’s desk with printed brand guidelines pages fanned out, color swatches, a pencil and a small plant, calm and elegant.'),
 'tiendas': ('Close-up of a minimalist product packaging box and a small glossy product on a pastel pedestal, next to a laptop showing an abstract blurred online store layout, studio lighting.',
             'Wide panoramic shot of neatly arranged products on shelves and a shipping box with tissue paper, pastel palette, airy and clean.'),
 'social': ('A smartphone standing upright showing an abstract grid of colorful social media posts (no readable text), surrounded by floating soft pastel shapes, studio lighting.',
            'Wide panoramic arrangement of several phones and tablets in a row displaying a consistent abstract visual system in pastel colors, no readable text.'),
 'web': ('A laptop and a tablet on a pastel desk showing an abstract modern website layout with big shapes and blocks (no readable text), soft shadows, top three-quarter view.',
         'Wide panoramic view of a desktop monitor, a phone and a tablet showing responsive abstract web layouts, pastel gradient background.'),
 'editorial': ('A stack of printed brochures, a folded flyer and an open annual report with clean grid layouts and abstract shapes (no readable text), on a soft peach surface, soft light.',
               'Wide panoramic spread of an open magazine-style report with large abstract graphics and a paper clip, calm editorial mood.'),
 'youtube': ('A monitor showing a grid of bold abstract video thumbnails with simple shapes and bright pastel colors (no readable text), a microphone and a camera beside it, studio lighting.',
             'Wide panoramic creator desk with a camera, ring light, headphones and a monitor with abstract thumbnails, pastel palette.'),
}

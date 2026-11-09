# Briefs por servicio (formularios que solo se abren con su URL; no hay enlaces desde el sitio).
# Cada campo: (clave, tipo, texto ES, texto EN, requerido, opciones[(es, en)], ayuda (es, en))
# tipos: text, textarea, url, tel, email, date, select, radio, checkbox


def C(k, t, es, en, req=False, ops=None, ayuda=None):
    return dict(k=k, t=t, es=es, en=en, req=req, ops=ops or [], ayuda=ayuda)


def O(*pares):
    return [p if isinstance(p, tuple) else (p, p) for p in pares]


SI_NO = O(('Sí', 'Yes'), ('No', 'No'))

# ---- bloques comunes ----
SOBRE_TI = ('Sobre ti', 'About you', [
    C('nombre', 'text', 'Tu nombre', 'Your name', True),
    C('email', 'email', 'Correo electrónico', 'Email', True),
    C('telefono', 'tel', 'WhatsApp o teléfono', 'WhatsApp or phone'),
    C('marca', 'text', 'Nombre de tu marca o empresa', 'Your brand or company name'),
    C('pais', 'text', 'País y ciudad', 'Country and city'),
    C('web', 'url', 'Sitio web o redes sociales actuales (si tienes)', 'Current website or social media (if any)'),
])

DETALLES = ('Últimos detalles', 'Final details', [
    C('fecha', 'text', '¿Para cuándo lo necesitas?', 'When do you need it?', ayuda=('Una fecha o un rango aproximado.', 'A date or an approximate range.')),
    C('presupuesto', 'text', 'Presupuesto estimado (opcional)', 'Estimated budget (optional)', ayuda=('Me ayuda a proponerte la mejor opción. Puedes indicar la moneda.', 'It helps me suggest the best option. You can include the currency.')),
    C('referencias', 'textarea', 'Referencias que te gusten (links o nombres)', 'References you like (links or names)'),
    C('material', 'url', 'Enlace a tu carpeta con material (Drive, Dropbox, etc.)', 'Link to your folder with materials (Drive, Dropbox, etc.)', ayuda=('Logos, textos, fotos o cualquier archivo útil. Asegúrate de que el enlace permita ver.', 'Logos, copy, photos or any useful file. Make sure the link allows viewing.')),
    C('extra', 'textarea', '¿Algo más que quieras contarme?', 'Anything else you’d like to tell me?'),
])

BRIEFS = {
 'branding': dict(slug=('branding', 'branding'), titulo=('Brief de branding y logo', 'Branding and logo brief'), secciones=[
    SOBRE_TI,
    ('Tu marca', 'Your brand', [
        C('necesito', 'checkbox', '¿Qué necesitas?', 'What do you need?', True, O(('Logo nuevo', 'New logo'), ('Rediseño de logo', 'Logo redesign'), ('Manual de marca', 'Brand guidelines'), ('Identidad visual completa', 'Full visual identity'), ('Papelería', 'Stationery'), ('Piezas para redes sociales', 'Social media pieces'))),
        C('nombre_marca', 'text', 'Nombre exacto de la marca (como debe escribirse)', 'Exact brand name (as it should be written)', True),
        C('eslogan', 'text', '¿Tiene eslogan o frase?', 'Does it have a tagline?'),
        C('actividad', 'textarea', '¿A qué se dedica tu negocio?', 'What does your business do?', True),
        C('cliente', 'textarea', '¿Quién es tu cliente ideal?', 'Who is your ideal customer?'),
        C('sentir', 'textarea', '¿Qué quieres que la gente piense o sienta al ver tu marca?', 'What do you want people to think or feel when they see your brand?'),
        C('palabras', 'text', 'Tres palabras que describan tu marca', 'Three words that describe your brand'),
        C('logo_actual', 'radio', '¿Tienes un logo actual?', 'Do you have a current logo?', False, O(('Sí, quiero rediseñarlo', 'Yes, I want to redesign it'), ('Sí, quiero mantenerlo', 'Yes, I want to keep it'), ('No', 'No'))),
    ]),
    ('Estilo y uso', 'Style and use', [
        C('estilo', 'checkbox', 'Estilo que imaginas', 'Style you imagine', False, O(('Minimalista', 'Minimalist'), ('Elegante', 'Elegant'), ('Moderno', 'Modern'), ('Divertido', 'Playful'), ('Clásico', 'Classic'), ('Audaz', 'Bold'), ('Natural', 'Natural'), ('Premium', 'Premium'))),
        C('colores', 'text', 'Colores que te gustan o quieres evitar', 'Colors you like or want to avoid'),
        C('competencia', 'textarea', 'Marcas de tu competencia (links o nombres)', 'Competitor brands (links or names)'),
        C('usos', 'checkbox', '¿Dónde se va a usar?', 'Where will it be used?', False, O(('Redes sociales', 'Social media'), ('Sitio web', 'Website'), ('Material impreso', 'Print'), ('Empaques', 'Packaging'), ('Señalización', 'Signage'), ('Uniformes o merch', 'Uniforms or merch'))),
    ]),
    DETALLES]),
 'tiendas': dict(slug=('tienda-online', 'online-store'), titulo=('Brief de tienda online', 'Online store brief'), secciones=[
    SOBRE_TI,
    ('Tu tienda', 'Your store', [
        C('tipo', 'radio', '¿Qué necesitas?', 'What do you need?', True, O(('Tienda nueva', 'New store'), ('Rediseñar mi tienda actual', 'Redesign my current store'), ('Migrar desde otra plataforma', 'Migrate from another platform'))),
        C('vendes', 'textarea', '¿Qué vendes y a quién?', 'What do you sell and to whom?', True),
        C('productos', 'select', 'Cantidad aproximada de productos', 'Approximate number of products', False, O(('1 a 10', '1 to 10'), ('11 a 50', '11 to 50'), ('51 a 200', '51 to 200'), ('Más de 200', 'More than 200'))),
        C('marca_def', 'radio', '¿Tienes logo y marca definidos?', 'Do you have a logo and brand defined?', False, O(('Sí, completos', 'Yes, complete'), ('En parte', 'Partly'), ('No', 'No'))),
        C('mercado', 'text', '¿A qué países vendes?', 'Which countries do you sell to?'),
        C('moneda', 'text', 'Idiomas y monedas de la tienda', 'Store languages and currencies'),
    ]),
    ('Funciones', 'Features', [
        C('pagos', 'checkbox', 'Pagos y envíos que necesitas', 'Payments and shipping you need', False, O(('Tarjetas', 'Cards'), ('PayPal', 'PayPal'), ('Transferencia', 'Bank transfer'), ('Contra entrega', 'Cash on delivery'), ('Envíos nacionales', 'Domestic shipping'), ('Envíos internacionales', 'International shipping'))),
        C('funciones', 'checkbox', 'Funciones que te interesan', 'Features you’re interested in', False, O(('Blog', 'Blog'), ('Reseñas de clientes', 'Customer reviews'), ('Cupones y descuentos', 'Coupons and discounts'), ('Suscripciones', 'Subscriptions'), ('Email marketing', 'Email marketing'), ('Colecciones con filtros', 'Filterable collections'))),
        C('cuentas', 'radio', '¿Tienes dominio y cuenta de Shopify?', 'Do you have a domain and a Shopify account?', False, O(('Ambos', 'Both'), ('Solo dominio', 'Domain only'), ('Ninguno', 'Neither'), ('No sé', 'Not sure'))),
        C('que_cambiar', 'textarea', 'Si ya tienes tienda: ¿qué te gustaría mejorar?', 'If you already have a store: what would you like to improve?'),
    ]),
    DETALLES]),
 'social': dict(slug=('redes-sociales', 'social-media'), titulo=('Brief de redes sociales', 'Social media brief'), secciones=[
    SOBRE_TI,
    ('Tu contenido', 'Your content', [
        C('redes', 'checkbox', '¿Para qué redes?', 'Which platforms?', True, O('Instagram', 'TikTok', 'LinkedIn', 'Facebook', 'YouTube', 'Pinterest', 'X', ('Otras', 'Other'))),
        C('piezas', 'checkbox', '¿Qué piezas necesitas?', 'What pieces do you need?', True, O(('Publicaciones', 'Posts'), ('Carruseles', 'Carousels'), ('Stories', 'Stories'), ('Portadas de destacadas', 'Highlight covers'), ('Plantillas editables', 'Editable templates'), ('Piezas para una campaña', 'Campaign pieces'), ('Banners o portadas de perfil', 'Profile banners or covers'))),
        C('cantidad', 'select', 'Cantidad de piezas', 'Number of pieces', False, O(('Proyecto único (1 a 10)', 'One-off project (1 to 10)'), ('Mensual: 5 a 12', 'Monthly: 5 to 12'), ('Mensual: 13 a 30', 'Monthly: 13 to 30'), ('Más de 30 al mes', 'More than 30 a month'))),
        C('frecuencia', 'text', '¿Cada cuánto publicas?', 'How often do you post?'),
        C('objetivo', 'textarea', '¿Cuál es el objetivo de tu contenido?', 'What is the goal of your content?', True),
        C('tono', 'checkbox', 'Tono del contenido', 'Content tone', False, O(('Educativo', 'Educational'), ('Inspirador', 'Inspirational'), ('Corporativo', 'Corporate'), ('Divertido', 'Fun'), ('Cercano', 'Friendly'), ('Premium', 'Premium'))),
    ]),
    ('Marca y producción', 'Brand and production', [
        C('manual', 'radio', '¿Tienes manual de marca?', 'Do you have brand guidelines?', False, O(('Sí', 'Yes'), ('Parcial', 'Partial'), ('No', 'No'))),
        C('textos', 'radio', '¿Quién crea los textos?', 'Who writes the copy?', False, O(('Yo', 'Me'), ('Tengo copywriter', 'I have a copywriter'), ('Necesito ayuda con los textos', 'I need help with the copy'))),
        C('plantillas', 'radio', 'Si hay plantillas: ¿quién las usará?', 'If there are templates: who will use them?', False, O(('Yo, en Canva', 'Me, in Canva'), ('Yo, en Figma', 'Me, in Figma'), ('Prefiero que las uses tú', 'I prefer you to use them'))),
        C('cuentas_ref', 'textarea', 'Cuentas que te inspiran (links)', 'Accounts that inspire you (links)'),
    ]),
    DETALLES]),
 'web': dict(slug=('diseno-web', 'web-design'), titulo=('Brief de diseño web', 'Web design brief'), secciones=[
    SOBRE_TI,
    ('Tu sitio web', 'Your website', [
        C('tipo', 'radio', 'Tipo de sitio', 'Type of site', True, O(('Landing page', 'Landing page'), ('Sitio corporativo', 'Business site'), ('Portafolio', 'Portfolio'), ('Blog', 'Blog'), ('Tienda online', 'Online store'), ('Otro', 'Other'))),
        C('objetivo', 'textarea', '¿Cuál es el objetivo principal del sitio?', 'What is the main goal of the site?', True),
        C('plataforma', 'radio', 'Plataforma', 'Platform', False, O('WordPress', 'Shopify', ('Solo diseño en Figma', 'Design only in Figma'), ('No sé, recomiéndame', 'Not sure, recommend one'))),
        C('paginas', 'checkbox', 'Páginas que necesitas', 'Pages you need', False, O(('Inicio', 'Home'), ('Nosotros', 'About'), ('Servicios', 'Services'), ('Portafolio', 'Portfolio'), ('Blog', 'Blog'), ('Preguntas frecuentes', 'FAQ'), ('Contacto', 'Contact'), ('Otras', 'Other'))),
        C('contenido', 'radio', '¿Tienes los textos e imágenes?', 'Do you have the copy and images?', False, O(('Todo listo', 'All ready'), ('En parte', 'Partly'), ('Nada, necesito apoyo', 'Nothing, I need support'))),
        C('idiomas', 'text', 'Idiomas del sitio', 'Site languages'),
    ]),
    ('Funciones y técnico', 'Features and technical', [
        C('funciones', 'checkbox', 'Funciones que necesitas', 'Features you need', False, O(('Formulario de contacto', 'Contact form'), ('Reservas o agenda', 'Bookings or scheduling'), ('Blog', 'Blog'), ('Varios idiomas', 'Multiple languages'), ('Pagos online', 'Online payments'), ('Email marketing', 'Email marketing'), ('Botón de WhatsApp', 'WhatsApp button'))),
        C('hosting', 'radio', '¿Tienes dominio y hosting?', 'Do you have a domain and hosting?', False, O(('Ambos', 'Both'), ('Solo dominio', 'Domain only'), ('Ninguno', 'Neither'), ('No sé', 'Not sure'))),
        C('no_gusta', 'textarea', 'Si ya tienes sitio: ¿qué no te gusta?', 'If you already have a site: what don’t you like about it?'),
    ]),
    DETALLES]),
 'editorial': dict(slug=('editorial', 'editorial'), titulo=('Brief de diseño editorial', 'Editorial design brief'), secciones=[
    SOBRE_TI,
    ('Tu pieza', 'Your piece', [
        C('piezas', 'checkbox', '¿Qué necesitas?', 'What do you need?', True, O('Flyer', 'Brochure', ('Catálogo', 'Catalog'), ('Informe anual', 'Annual report'), ('Presentación', 'Presentation'), ('Portafolio', 'Portfolio'), ('Revista o libro digital', 'Magazine or ebook'), ('Otro', 'Other'))),
        C('formato', 'radio', 'Formato', 'Format', False, O(('Impreso', 'Print'), ('Digital', 'Digital'), ('Ambos', 'Both'))),
        C('paginas', 'text', 'Número aproximado de páginas y tamaño (si lo sabes)', 'Approximate number of pages and size (if you know)'),
        C('cantidad', 'text', 'Cantidad de piezas o versiones', 'Number of pieces or versions'),
        C('contenido', 'radio', '¿Tienes los textos e imágenes?', 'Do you have the copy and images?', False, O(('Todo listo', 'All ready'), ('Textos listos, faltan imágenes', 'Copy ready, images missing'), ('Necesito ayuda con la estructura', 'I need help with the structure'))),
        C('descripcion', 'textarea', 'Cuéntame de qué trata y para quién es', 'Tell me what it is about and who it is for', True),
    ]),
    ('Marca e impresión', 'Brand and printing', [
        C('manual', 'radio', '¿Tienes manual de marca?', 'Do you have brand guidelines?', False, O(('Sí', 'Yes'), ('Parcial', 'Partial'), ('No', 'No'))),
        C('imprenta', 'radio', '¿Ya tienes imprenta definida?', 'Do you already have a printer?', False, SI_NO),
        C('idiomas', 'text', 'Idiomas del contenido', 'Content languages'),
        C('tono', 'checkbox', 'Tono visual', 'Visual tone', False, O(('Corporativo', 'Corporate'), ('Institucional', 'Institutional'), ('Creativo', 'Creative'), ('Minimalista', 'Minimalist'), ('Editorial', 'Editorial'))),
    ]),
    DETALLES]),
 'youtube': dict(slug=('miniaturas-youtube', 'youtube-thumbnails'), titulo=('Brief de miniaturas de YouTube', 'YouTube thumbnails brief'), secciones=[
    SOBRE_TI,
    ('Tu canal', 'Your channel', [
        C('canal', 'url', 'Enlace a tu canal', 'Link to your channel', True),
        C('tematica', 'text', 'Temática del canal', 'Channel topic', True),
        C('cantidad', 'select', '¿Cuántas miniaturas necesitas?', 'How many thumbnails do you need?', False, O(('1', '1'), ('2 a 5', '2 to 5'), ('6 a 12', '6 to 12'), ('Pack mensual', 'Monthly pack'))),
        C('frecuencia', 'text', '¿Cada cuánto subes videos?', 'How often do you upload videos?'),
        C('titulos', 'textarea', 'Títulos o temas de los primeros videos', 'Titles or topics of the first videos'),
    ]),
    ('Estilo', 'Style', [
        C('estilo', 'checkbox', 'Estilo que imaginas', 'Style you imagine', False, O(('Minimalista', 'Minimalist'), ('Llamativo y colorido', 'Eye-catching and colorful'), ('Con rostro grande', 'Big face'), ('Con ilustraciones', 'Illustrated'), ('Con texto grande', 'Big text'), ('Profesional', 'Professional'))),
        C('marca_canal', 'radio', '¿Tienes colores y marca del canal?', 'Do you have channel colors and branding?', False, O(('Sí', 'Yes'), ('En parte', 'Partly'), ('No', 'No'))),
        C('rostro', 'radio', '¿Vas a aparecer en las miniaturas?', 'Will you appear in the thumbnails?', False, O(('Sí, enviaré fotos', 'Yes, I’ll send photos'), ('No, usar elementos gráficos', 'No, use graphic elements'), ('A veces', 'Sometimes'))),
        C('plantilla', 'radio', '¿Quieres una plantilla editable?', 'Do you want an editable template?', False, SI_NO),
    ]),
    DETALLES]),
}

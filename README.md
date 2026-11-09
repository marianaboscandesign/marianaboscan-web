# Sitio marianaboscan.com (ES / EN) — guía

Sitio estático, gratis, con tu design system (logo, colores, DM Sans + Fraunces, modo claro/oscuro según el dispositivo).

| Carpeta / archivo | Qué es |
|---|---|
| `dist/` | **El sitio listo para publicar** (esto es lo que se sube a GitHub) |
| `build.py` | Genera `dist/` desde los textos. Todo el contenido (textos ES/EN, categorías, proyectos destacados) está arriba en el archivo |
| `data/proyectos.json` | Tus 17 proyectos (portadas, imágenes, videos) |
| `src/` | Estilos (`estilos.css`), logos y tipografías |
| `src/img/` | (opcional) tus imágenes y tu foto locales. Si están aquí, el sitio las usa en vez de las de Adobe |
| `descargar-imagenes.html` | Ábrelo en tu navegador y baja todas las imágenes del portafolio en un ZIP (descomprímelo en `src/img/`) |

Para cambiar algo: edita `build.py` y ejecuta `python3 build.py`.

## Tu foto del banner
Pon tu foto en `src/img/foto.jpg` (o `.png` / `.webp`) y ejecuta `python3 build.py`. Ideal: cuadrada, mínimo 1200 px, con el rostro centrado. El círculo recorta solo; el fondo pastel se ve mejor si la foto tiene fondo liso o recortado.
Las fichas «Ps, Ai, Id, Fig, Pr, Ae» alrededor son fichas de color propias del design system (no logos oficiales); se editan en `CHIPS` dentro de `build.py`.

## Modo claro / oscuro y selector de idioma
El botón de luna/sol cambia el modo y recuerda la elección; sin elegir, sigue el dispositivo. El idioma es un menú con los nombres (Español / English).

## Páginas
Español (raíz): `/`, `/portafolio/`, `/sobre-mi/`, `/contacto/`, `/<proyecto>/` (misma dirección que ya tenías, así no se rompen enlaces ni Google).
Inglés: `/en/`, `/en/work/`, `/en/about/`, `/en/contact/`, `/en/<proyecto>/`.
Las direcciones viejas `/work`, `/bio-2` y `/contact` redirigen a las nuevas.

## Publicar (gratis, GitHub Pages)
1. Repositorio público nuevo, por ejemplo `marianaboscan-web`. Sube **el contenido** de `dist/` (no la carpeta en sí).
2. Settings → Pages → rama `main`, carpeta `/ (root)`.
3. Prueba primero en `https://TU-USUARIO.github.io/marianaboscan-web/` (los enlaces son relativos y funcionan ahí).
4. Cuando todo esté bien, **lanzamiento**: crea un archivo `CNAME` en el repo con `www.marianaboscan.com`, ponlo en Settings → Pages → Custom domain y en GoDaddy:
   - `CNAME` · nombre `www` → `TU-USUARIO.github.io` (reemplaza el registro actual de `www`).
   - Para el dominio sin www, cuatro registros `A` en `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 (borra los A/redirecciones anteriores hacia Adobe). Verifica estos valores en la documentación de GitHub Pages antes de hacerlo.
   - Activa *Enforce HTTPS* cuando el chequeo salga en verde.
5. Si algo sale mal, devuelve los registros DNS anteriores y tu sitio de Adobe sigue ahí.

## Formulario de contacto
Usa el mismo Apps Script del formulario de logos. Pega de nuevo el `Code.gs` actualizado (carpeta `revisa-logo/`), crea **nueva versión** de la implementación, y ejecuta `ENDPOINT=https://script.google.com/macros/s/XXXX/exec python3 build.py`. Los mensajes quedan en la hoja **Contactos** y te llegan a tu Gmail (responder responde a quien escribió).

## Cosas que debes saber
- **Las imágenes siguen alojadas en Adobe Portfolio** hasta que corras `descargar-imagenes.html` y pongas el ZIP en `src/img/`. Los videos usan el reproductor de Adobe (no se pueden descargar así). En previsualizaciones con restricciones (como el visor de artefactos) las imágenes externas no cargan; en GitHub Pages sí. Si cancelas Adobe Portfolio, esas imágenes dejan de cargar. Antes de cancelar: descarga tus imágenes (de Behance o de tus archivos) y las pasamos a la carpeta del sitio.
- Los enlaces de la CDN llevan una firma; si Adobe los cambia, hay que volver a extraerlos.
- Los textos de los proyectos son solo título y categoría; si quieres descripción (cliente, rol, año) por proyecto, se agrega en `META`.

## Proyectos nuevos desde Behance (automático)

- `scripts/sync_behance.py` lee tu feed de Behance y agrega los proyectos nuevos a `data/behance_nuevos.json`.
- `build.py` los pone primero en la página de Portafolio, con enlace a Behance. Puedes editar a mano marca, descripción y categoría en ese archivo y no se sobrescriben.
- `.github/workflows/sitio.yml` corre cada 6 horas (y cuando subes cambios): lee Behance, construye el sitio y lo publica. También hay un botón "Run workflow" en la pestaña Actions.
- Para cambiar desde qué fecha entran proyectos solos, edita `DESDE` en `scripts/sync_behance.py`.

### Páginas internas para proyectos de Behance
Las tarjetas nuevas abren Behance hasta que exista `data/imagenes/<ID>.json`. Con ese archivo el sitio genera la página interna (ES/EN) con las imágenes y la tarjeta enlaza a ella. Para crearlo usa `herramientas/marcador-behance.html` (marcador para el navegador).

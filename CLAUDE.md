# Casona El Castillo — Claude Code Instructions

## Skills

- **Nuevo feature o mejora**: `superpowers:brainstorming` antes de escribir código
- **Bugs difíciles**: `superpowers:systematic-debugging`
- **Siempre**: `superpowers:test-driven-development` al implementar features
- **Antes de terminar**: `superpowers:verification-before-completion`

---

## Preferencias de trabajo

- Al terminar un cambio de UI, levantar el servidor de dev (`flutter run -d web-server` o similar) y avisar la URL — **no** manejar el navegador con Playwright/MCP para hacer clic o tomar screenshots. JP prefiere verificar visualmente él mismo. Usar Playwright en este proyecto solo si JP lo pide explícitamente.

---

## Descripción del proyecto

App Flutter para "Casona El Castillo" — hotel/restaurante/lugar turístico. App de presentación con galería, menú, contacto e información del lugar. Incluye scripts Python para generación de contenido de marketing.

**Pantallas:**

- `home_screen.dart` — pantalla principal
- `gallery_screen.dart` — galería de fotos
- `menu_screen.dart` — carta/menú del restaurante
- `contact_screen.dart` — información de contacto
- `sections.dart` — secciones de contenido
- `config.dart` — configuración (URLs, textos)
- `theme.dart` — colores y estilos

---

## Stack

- **Framework:** Flutter (web + mobile)
- **Lenguaje:** Dart
- **Deploy:** Netlify (`netlify.toml`)
- **Scripts:** Python para generación de marketing (`generar_marketing*.py`)

### Comandos

```bash
flutter pub get
flutter run -d chrome          # web (desarrollo)
flutter run                    # mobile (desarrollo)
flutter build web --release    # build web
```

```bash
# Generar contenido de marketing
python generar_marketing.py
python generar_marketing2.py
```

---

## Estructura

```
lib/
  main.dart
  config.dart              — URLs, textos y configuración
  theme.dart               — colores y estilos
  home_screen.dart
  gallery_screen.dart
  menu_screen.dart
  contact_screen.dart
  faq_section.dart         — preguntas frecuentes (espejo del FAQPage, ver SEO)
  sections.dart
tool/validar_seo.py        — valida JSON-LD, espejo SEO y paridad del FAQ
assets/                    — imágenes del lugar
marketing/                 — materiales de marketing generados
mobile/                    — assets específicos mobile
old_web/                   — versión anterior (referencia)
generar_marketing*.py      — scripts Python de generación de contenido
```

### Notas

- `config.dart` centraliza textos, URLs e imágenes — modificar ahí primero antes de tocar pantallas
- `old_web/` es referencia histórica, no modificar

---

## SEO / GEO (posicionamiento en buscadores de IA)

**Dominio de producción:** `casonafundoelcastillo.cl`

### Limitación de base: Flutter Web = canvas

Flutter Web renderiza todo en `<canvas>` vía CanvasKit, así que el DOM no contiene texto real de la app: un crawler ve un documento vacío. El flag `--web-renderer html` **fue removido en Flutter 3.29+** (confirmado en 3.44.4), no hay forma de forzar renderer HTML. La solución adoptada es el **espejo SEO** descrito abajo, no prerendering.

### Reglas que NO se deben romper

1. **El espejo SEO (`#seo-content` en `web/index.html`) NO se elimina del DOM.**
   Es el único contenido semántico legible del sitio — lo que indexan Google, GPTBot, ClaudeBot, PerplexityBot y OAI-SearchBot. Cuando Flutter monta su UI, el listener de `flutter-first-frame` solo le pone `aria-hidden="true"` + `inert`.
   **Nunca reemplazar por `.remove()` / `removeChild` / `display:none`.** Los crawlers de IA ejecutan JS y disparan ese mismo evento; si se elimina el nodo, vuelven a indexar una página vacía y se pierde todo el trabajo. El `.visually-hidden` usa `position:absolute` + `clip` justamente porque `display:none` lo haría invisible también para los crawlers.

2. **El copy del espejo y de `web/llms.txt` debe seguir al de `lib/`.**
   Si cambia un texto en `sections.dart`, `home_screen.dart` o `contact_screen.dart`, hay que actualizar el espejo en `web/index.html` **y** `web/llms.txt`. Son tres lugares que dicen lo mismo y se desincronizan solos.

3. **Las preguntas del FAQ viven en TRES lugares y deben coincidir LITERALMENTE.**
   - `lib/faq_section.dart` (`kFaqItems`) — lo que **ve el usuario** en la app
   - `web/index.html` → JSON-LD `FAQPage` — lo que leen los motores
   - `web/index.html` → `<dt>`/`<dd>` del espejo `#seo-content`

   Google exige que las preguntas del structured data estén **visibles en la página**; por eso existe la sección FAQ en Flutter, no solo el espejo oculto. Si editas una pregunta, edítala en los tres lados y corre el validador. La coincidencia es carácter por carácter.

### Validación

```bash
python3 tool/validar_seo.py                      # sobre web/index.html
python3 tool/validar_seo.py build/web/index.html # sobre el build
```

Verifica: JSON-LD parsea, tipos requeridos presentes, `@id` referenciados existen, FAQ 1:1 contra los `<dt>` del espejo **y** contra `kFaqItems` de `lib/faq_section.dart` (preguntas **y** respuestas), coherencia de la cifra de capacidad entre `index.html` / `llms.txt` / `faq_section.dart` / `maximumAttendeeCapacity`, y que no haya `.remove()` sobre el espejo. **Correr siempre después de tocar el copy o el JSON-LD.**

La capacidad se repite en ~15 lugares: cambiarla a mano en unos pocos deja el sitio diciendo dos cifras distintas. El validador atrapa exactamente eso (pasó con el cambio 200 → 300, que perdió `maximumAttendeeCapacity`).

### Estado (2026-07-29)

- **Espejo SEO** en `web/index.html`: ~5.400 chars de texto, 1 h1 / 9 h2 / 3 h3, listas de servicios y tipos de evento, `<dl>` con 9 preguntas frecuentes. (Antes: 166 chars, cero h2.)
- **Sección FAQ visible** en `lib/faq_section.dart`: `ExpansionTile` con las 9 preguntas, entre Ubicación y Contacto, con entrada en navbar ("FAQ") y drawer ("Preguntas Frecuentes"). Existe para que el `FAQPage` del schema refleje contenido realmente visible al usuario — no solo el espejo oculto.
- **JSON-LD** como `@graph` único con `@id` cruzados: `Organization`, `WebSite`, `WebPage`, `ImageObject`, `EventVenue`+`LocalBusiness` (geo, `maximumAttendeeCapacity: 300`, 12 `amenityFeature`, teléfono, `openingHoursSpecification`, `event[]`) y `FAQPage` con 9 preguntas.
- **`web/llms.txt`**: resumen factual denso en blockquote + secciones.
- **og:image**: `web/og-image.jpg`, 1200×630, recorte de `assets/images/pileta.jpeg` (la pileta del parque francés), con `og:image:width/height/alt`. Antes apuntaba a `icons/Icon-512.png` (ícono cuadrado, se recortaba mal en WhatsApp).
- **`netlify.toml`**: headers `Content-Type` con `charset=utf-8` para `.txt` y `.xml` — sin eso los acentos llegan mal decodificados a los crawlers.
- **Sin `priceRange`** y **sin horario de término** de eventos: decisión de JP, no publicarlos. El FAQ dice que se cotiza caso a caso.

### Datos factuales del lugar (fuente para el copy)

Todo esto viene del código (`lib/sections.dart`, `old_web/pages/servicios.html`, `generar_marketing*.py`) o fue confirmado por JP. **No inventar cifras ni servicios fuera de esta lista** — si falta un dato, preguntar.

- Parque diseñado por paisajista francés, +80 años, árboles centenarios, acceso privado
- Casona antigua restaurada: baños modernos, cocina de +300 m²
- Carpa de eventos: más de **300 personas**, clima controlado, iluminación especial, equipamiento completo
- Ubicación: Calle Larga, Los Andes, Región de Valparaíso · lat −32,8850 lon −70,6494 · a 5 min del Casino Enjoy Santiago · ~75 km de Santiago
- Contacto: +56 9 9779 4301 (WhatsApp) · casonaelcastillo1933@gmail.com · @casonafundoelcastillo
- Confirmado por JP (2026-07-29): catering externo **permitido**, estacionamiento privado **sí**, ceremonia civil en el lugar **sí**, plan de lluvia = **carpa**
- Servicios (de `old_web/pages/servicios.html`): planificación integral, banquetería de autor, ambientación floral, coordinación día del evento

### Landing pages por intención de búsqueda

Hechas (2026-08-24): 3 páginas estáticas HTML independientes de la app Flutter (evitan el problema de CanvasKit — no son rutas de la SPA), en `web/<slug>/index.html`, copiadas tal cual al build por `flutter build web`:

- `web/matrimonios-los-andes/index.html`
- `web/centro-de-eventos-los-andes/index.html`
- `web/eventos-corporativos-los-andes/index.html`

Cada una: título/meta description propios, contenido real distinto (no copia del home, para evitar que Google las trate como doorway pages), imágenes reales del sitio sin repetir el mismo hero entre páginas, JSON-LD liviano (`WebPage` + `BreadcrumbList`, sin duplicar todo el schema del home), CTA a WhatsApp y al `#contacto` del sitio principal. Agregadas a `web/sitemap.xml` y enlazadas desde el footer de la app (`lib/main.dart` → `_buildFooter`) para que no queden huérfanas.

**Para agregar una nueva página de este tipo:** copiar el patrón de una existente (mismo `<head>`/CSS/paleta), cambiar título/meta/JSON-LD/contenido/imágenes, agregar a `sitemap.xml` y a la lista de `_footerLink(...)` en `main.dart`.

---

## Analytics (GA4)

- **Measurement ID:** `G-FQHVYMVDFJ`. Snippet gtag.js instalado en `web/index.html` (dentro de `<head>`, antes del bloque `<style>`).
- **Objetivo configurado en GA4:** generación de oportunidades de venta (+ tráfico web).
- **`lib/analytics.dart`**: export condicional (`analytics_web.dart` con `dart:js_interop` llamando a `window.gtag` en web, `analytics_stub.dart` no-op en mobile) — la app también compila a iOS/Android, por eso el stub.
- **Eventos custom:**
  - `generate_lead` — al enviar con éxito el formulario de contacto (`lib/contact_screen.dart`)
  - `contact_click` con parámetro `channel: whatsapp|instagram` — al hacer clic en los íconos sociales (`_SocialIcon` en `lib/main.dart`, usado en nav/drawer/footer)
- Para agregar un nuevo evento: `import 'analytics.dart'; trackEvent('nombre_evento', {'param': valor});`

---

## Skills disponibles

- `/code-review` — Revisar cambios antes de merge
- `/verify` — Verificar que la app se ve correctamente
- `/run` — Iniciar Flutter web y observar en Chrome
- `/image-enhancer` — Mejorar fotos del lugar para la galería

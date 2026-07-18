# Casona El Castillo — Claude Code Instructions

## Skills

- **Nuevo feature o mejora**: `superpowers:brainstorming` antes de escribir código
- **Bugs difíciles**: `superpowers:systematic-debugging`
- **Siempre**: `superpowers:test-driven-development` al implementar features
- **Antes de terminar**: `superpowers:verification-before-completion`

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
  sections.dart
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

## Skills disponibles

- `/code-review` — Revisar cambios antes de merge
- `/verify` — Verificar que la app se ve correctamente
- `/run` — Iniciar Flutter web y observar en Chrome
- `/image-enhancer` — Mejorar fotos del lugar para la galería

# 100 Verbos Irregulares

App web instalable (PWA) para estudiar 100 verbos irregulares en inglés: presente, pasado, participio, significado en español y pronunciación con voces neuronales (mujer u hombre, acento estadounidense o británico).

En línea: https://verbos-comarca.vercel.app

## Estructura
- `index.html`: la app completa (lista de verbos, búsqueda, reproductor).
- `audio/{us,gb}-{f,m}/`: un MP3 por forma verbal y voz.
- `sw.js` + `manifest.webmanifest`: instalación y uso sin internet.
- `scripts/make_audio.py`: regenera los audios con edge-tts (`python scripts/make_audio.py index.html audio`).
- `scripts/icons.py`: dibuja los íconos (requiere Pillow).

## Publicar
Cada push a `main` se publica solo en Vercel.

Si cambias `index.html` o los audios, sube la versión en `sw.js` (por ejemplo `verbos-v2` → `verbos-v3`) para que los celulares que la tienen instalada se actualicen.

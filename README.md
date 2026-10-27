# Transcriptor de audio del Lab IA

Transcribe audios de reuniones en español con **Whisper** (vía `faster-whisper`), **en tu propio computador**. Funciona en Windows, Mac y Linux, con o sin tarjeta gráfica.

> **El audio no se sube a ningún servicio en línea**: ni páginas web, ni Google Colab, ni el transcriptor de Zoom. En las reuniones se habla de resultados no publicados y de proyectos con el Hospital de Curicó.

## Instalar (una sola vez)

Necesitas **Python 3.10 o superior**, **git** y unos 3 GB libres en disco.

```bash
git clone https://github.com/utalca-ai/Audio-Transcript.git
cd Audio-Transcript
pip install -r requirements.txt
```

No hace falta instalar FFmpeg ni PyTorch. La primera vez que transcribas se descarga el modelo (unos 1,6 GB).

## Transcribir

Desde la carpeta `Audio-Transcript`:

```bash
python transcrip.py ruta/al/2026-10-22-reunion.m4a
```

El texto aparece en pantalla y queda guardado junto al audio, con el mismo nombre y extensión `.txt`, con la hora de cada frase:

```txt
[00:12:41] Entonces el objetivo es predecir el nivel de glicemia, no clasificar.
[00:12:47] Si la regresión funciona, la clasificación sale gratis con un umbral.
```

**Cuánto demora:** sin tarjeta gráfica, del orden de la duración del audio. Con tarjeta NVIDIA, unos pocos minutos.

## Glosario

`glosario-whisper.txt` le indica a Whisper los nombres del laboratorio y los términos técnicos. Sin él escribe «Windows Chap» por WindowSHAP o «Sotero» por Zotero. Si tu tema tiene términos propios, agrégalos al final. Mantenlo corto: Whisper solo lee las primeras ~200 palabras.

## Actualizar

```bash
git pull
```

Si modificaste el glosario y `git pull` reclama, guarda tus términos aparte, corre `git checkout glosario-whisper.txt`, haz `git pull` y vuelve a agregarlos.

## Si algo falla

| Problema | Qué hacer |
|---|---|
| `pip` no se reconoce | `python -m pip install -r requirements.txt` (en Mac, `python3`) |
| Se queda sin memoria o es muy lento | `python transcrip.py audio.m4a --modelo medium` |
| Repite la misma frase muchas veces | Pasa en silencios largos. Bórralas al revisar |
| No logras instalarlo | Escríbele a Ignacio Martínez |

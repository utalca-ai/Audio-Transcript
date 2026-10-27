# Transcriptor de Audio con OpenAI Whisper

Este repositorio contiene un script en Python (compatible con cuadernos Jupyter) que permite transcribir archivos de audio de forma eficiente utilizando el modelo `large-v3` de **OpenAI Whisper**. Está diseñado para funcionar de manera flexible tanto en tu entorno **local** como en la nube (como **Google Colab**).

## Características

* **Modelo Whisper Large-v3**: Máxima precisión en transcripción multilenguaje.
* **Detección Automática**: Identificación automática del idioma del audio.
* **Detección de Entorno Inteligente**: El código detecta automáticamente si se está ejecutando localmente o en Google Colab para gestionar las rutas de guardado de forma segura.
* **Aceleración por Hardware (GPU)**: Configurado para aprovechar GPUs de NVIDIA (CUDA) localmente, o las GPUs T4/L4 en la nube, reduciendo drásticamente el tiempo de transcripción.


## Requisitos e Instalación

Para que Whisper funcione correctamente, necesitas tener instalado **Python**, la librería de **Whisper** y **FFmpeg** (una herramienta del sistema para procesar audio). Elige tu entorno de ejecución:

### Opción A: Ejecución Local (Tu PC/Servidor)

Si deseas correr el script en tu propia máquina:

1. **Instalar FFmpeg**:
* **Windows:** Puedes usar un gestor de paquetes como Chocolatey (`choco install ffmpeg`) o descargarlo desde [ffmpeg.org](https://ffmpeg.org/).
* **macOS:** Usando Homebrew: `brew install ffmpeg`
* **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg`


2. **Instalar Dependencias de Python**:
Se recomienda usar un entorno virtual. Ejecuta en tu terminal:
```bash
pip install openai-whisper

```

*Nota sobre GPU local: Si tienes una tarjeta gráfica NVIDIA, asegúrate de tener instalado [PyTorch con soporte para CUDA](https://pytorch.org/get-started/locally/) para acelerar el proceso.*

### Opción B: Ejecución en Google Colab

Si prefieres no instalar nada y usar la nube:

1. Sube el código a un cuaderno de Colab.
2. Activa la GPU: `Entorno de ejecución` -> `Cambiar tipo de entorno de ejecución` -> Selecciona `T4 GPU` o `L4 GPU`.
3. Ejecuta la siguiente celda antes del script para instalar todo:
```bash
!pip install openai-whisper
!apt-get install ffmpeg -y

```

## Estructura de Directorios y Guardado

El script es inteligente con las rutas. Utiliza la variable de entorno `BN_OUTPUT_DIR` o rutas predeterminadas dependiendo de dónde lo ejecutes:

1. **Localmente**: Creará y buscará archivos en una carpeta llamada `audio` dentro del directorio donde ejecutes el script (o en la ruta que definas en `BN_OUTPUT_DIR`).
2. **En Google Colab**: Si tienes tu Google Drive montado (`/content/drive`), guardará las transcripciones allí directamente para que no pierdas tus datos al cerrar la sesión.

## Configuración y Uso

Antes de ejecutar el script, debes indicarle qué archivo de audio transcribir. Modifica la siguiente línea en el código con el nombre de tu archivo (asegúrate de que el archivo esté dentro de tu carpeta de salida):

```python
# Modifica esta línea con el nombre de tu archivo de audio
audio_path = OUTPUT_DIR + "/tu_archivo_de_audio.m4a"

```

Una vez configurado, simplemente ejecuta el script:

```bash
python nombre_del_script.py

```

*(O ejecuta la celda si estás en un cuaderno Jupyter/Colab).*

El resultado será un archivo de texto llamado `transcripcion_completa.txt` en el mismo directorio de salida, conteniendo todo el texto extraído.

## Consideraciones de Hardware

El modelo `large-v3` es muy preciso pero requiere bastante memoria gráfica (VRAM).

* Si lo ejecutas localmente y recibes un error de "Out of Memory" (OOM) en tu tarjeta gráfica, puedes cambiar el modelo en el código a uno más ligero, como `medium` o `small`:
```python
model = whisper.load_model("medium", device=device)

```


* Para audios largos, se recomienda encarecidamente el uso de GPU. Si el script detecta que solo tienes CPU, emitirá una advertencia, ya que el proceso será significativamente más lento.

## Opción C: Transcripción local sin GPU (`transcribir_local.py`)

Para reuniones con información sensible (datos del Hospital de Curicó, resultados no publicados), el audio **no debe subirse a Colab ni a Drive**. Esta opción corre completamente en tu computador, sin tarjeta gráfica, usando `faster-whisper` con el modelo `large-v3-turbo` cuantizado (int8). No requiere FFmpeg ni PyTorch.

```bash
pip install -r requirements-local.txt
python transcribir_local.py ruta/al/2026-10-22-reunion.m4a
```

El resultado queda junto al audio, con el mismo nombre y extensión `.txt`, y la hora de cada frase:

```txt
[00:12:41] Entonces el objetivo es predecir el nivel de glicemia, no clasificar.
```

* El idioma está fijo en español.
* `glosario-whisper.txt` le indica a Whisper los nombres y términos del laboratorio (WindowSHAP, BiGRU, Zotero…). Agrega los de tu tema al final; Whisper solo lee las primeras ~200 palabras.
* Sin GPU demora del orden de la duración del audio. Si se queda sin memoria: `--modelo medium`.

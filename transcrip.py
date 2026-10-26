import whisper
import torch
import os

# Verificar si hay GPU disponible para acelerar el proceso
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando el dispositivo: {device.upper()}")
if device != "cuda":
    print("ADVERTENCIA: No se detectó GPU. Para audios largos de más de 1 hora, se recomienda cambiar el entorno de ejecución a T4 GPU o L4 GPU en el menú 'Entorno de ejecución' -> 'Cambiar tipo de entorno de ejecución'.")

# 1. Ruta del archivo de audio (reemplaza con la ruta de tu archivo)

OUTPUT_DIR = os.environ.get("BN_OUTPUT_DIR", "/content/drive/MyDrive/audio")
if not os.path.exists("/content/drive"):
    OUTPUT_DIR = os.environ.get("BN_OUTPUT_DIR", "audio")

audio_path = OUTPUT_DIR + "/audio1520630667.m4a"



if not os.path.exists(audio_path):
    print(f"Por favor, sube tu archivo de audio a Colab y actualiza la variable 'audio_path' con su nombre correcto. Actualmente no se encuentra en: {audio_path}")
else:
    print("Cargando el modelo Whisper 'large-v3'... (Esto puede demorar unos minutos la primera vez)")
    # Cargamos el modelo más grande compatible con la GPU
    model = whisper.load_model("large-v3", device=device)

    print(f"Iniciando la transcripción de {audio_path}...")
    # Transcribimos el audio. 'verbose=True' te permitirá ver el avance en tiempo real
    result = model.transcribe(audio_path, verbose=True)

    # Guardar el resultado en un archivo de texto
    output_txt = OUTPUT_DIR + "/transcripcion_completa.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"\n¡Transcripción completada con éxito! Guardada en: {output_txt}")

import argparse
from pathlib import Path
from faster_whisper import WhisperModel

parser = argparse.ArgumentParser(description="Transcribe un audio en español, en tu computador.")
parser.add_argument("audio", help="Archivo de audio (m4a, mp3, wav, ...)")
parser.add_argument(
    "--modelo",
    default="large-v3-turbo",
    help="Modelo de Whisper. Usa 'medium' si se queda sin memoria o es muy lento.",
)
args = parser.parse_args()

audio = Path(args.audio)
if not audio.exists():
    raise SystemExit(f"No se encuentra el audio: {audio}")

# El glosario le enseña a Whisper los nombres y términos técnicos del laboratorio
glosario_txt = Path(__file__).with_name("glosario-whisper.txt")
glosario = glosario_txt.read_text(encoding="utf-8").strip() if glosario_txt.exists() else None

print(f"Cargando el modelo '{args.modelo}'... (la primera vez lo descarga)")
model = WhisperModel(args.modelo, device="auto", compute_type="int8")
segments, info = model.transcribe(
    str(audio), language="es", initial_prompt=glosario, vad_filter=True
)


def hms(t):
    t = int(t)
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


salida = audio.with_suffix(".txt")
with salida.open("w", encoding="utf-8") as f:
    for s in segments:
        linea = f"[{hms(s.start)}] {s.text.strip()}"
        print(linea)
        f.write(linea + "\n")
print(f"Listo: {salida}")

from pathlib import Path

#raiz
PROJECT_DIR = Path(__file__).resolve().parents[1]

AUDIO_DIR = PROJECT_DIR / "audios"
OUTPUT_DIR = PROJECT_DIR / "outputs"
MODEL_DIR = PROJECT_DIR / "models"

# Modelo de separação de seis faixas
# ex: voz, violao, baixo...
SEPARATION_MODEL = "htdemucs_6s.yaml"

# espectrograma
SPECTROGRAM_N_FFT = 2048
SPECTROGRAM_HOP_LENGTH = 512


def ensure_directories() -> None:
    """Cria os diretórios necessários para o processamento."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

from pathlib import Path

from src.analysis import analyze_audio
from src.config import OUTPUT_DIR


def prepare_singleplayer(audio_path: Path):
    """Prepara a música para uma partida singleplayer."""
    return analyze_audio(
        audio_path=audio_path,
        generate_plot=True,
        output_dir=OUTPUT_DIR,
    )

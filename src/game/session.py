
from pathlib import Path

from src.analysis import analyze_audio
from src.analysis.instrument_presence import detect_present_instruments
from src.config import OUTPUT_DIR
from src.separator.separation import separate_audio


def prepare_singleplayer(audio_path: Path):
    """Analisa a música e identifica os stems presentes."""

    analysis = analyze_audio(
        audio_path=audio_path,
        generate_plot=True,
        output_dir=OUTPUT_DIR,
    )

    stem_paths = separate_audio(audio_path)
    instruments = detect_present_instruments(stem_paths)

    return analysis, instruments


from pathlib import Path

from audio_separator.separator import Separator


from src.config import (
    MODEL_DIR,
    OUTPUT_DIR,
    SEPARATION_MODEL,
)


def separate_audio(
    audio_path: Path,
    output_dir: Path = OUTPUT_DIR / "separacao_6_stems",
    model_dir: Path = MODEL_DIR,
    model_filename: str = SEPARATION_MODEL,
) -> list[str]:
    """
    Separa um áudio em faixas usando o modelo configurado.

    Retorna os nomes dos arquivos produzidos pelo separador.
    """
    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    model_dir = Path(model_dir)

    if not audio_path.is_file():
        raise FileNotFoundError(
            f"Arquivo de áudio não encontrado: {audio_path}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    separator = Separator(
        output_dir=str(output_dir),
        output_format="WAV",
        model_file_dir=str(model_dir),
    )

    separator.load_model(model_filename=model_filename)

    return separator.separate(str(audio_path))

import logging
import time
import shutil
from pathlib import Path

from audio_separator.separator import Separator

from src.config import (
    MODEL_DIR,
    OUTPUT_DIR,
    SEPARATION_MODEL,
)

logger = logging.getLogger(__name__)

STEM_NAMES = (
    "Vocals",
    "Drums",
    "Bass",
    "Guitar",
    "Piano",
    "Other",
)


def separate_audio(
    audio_path: Path,
    output_dir: Path = OUTPUT_DIR / "separacao_6_stems",
    model_dir: Path = MODEL_DIR,
    model_filename: str = SEPARATION_MODEL,
    reuse_existing: bool = True,
) -> list[str]:
    """Separa o áudio ou reutiliza os seis stems existentes."""
    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    model_dir = Path(model_dir)

    if not audio_path.is_file():
        raise FileNotFoundError(
            f"Arquivo de áudio não encontrado: {audio_path}"
        )

    model_dir.mkdir(parents=True, exist_ok=True)

    model_name = Path(model_filename).stem

    # Cada música terá sua própria pasta de saída.
    song_output_dir = output_dir / audio_path.stem
    song_output_dir.mkdir(parents=True, exist_ok=True)

    expected_files = [
        song_output_dir
        / f"{audio_path.stem}_({stem})_{model_name}.wav"
        for stem in STEM_NAMES
    ]

    # Reaproveita a separação quando todos os stems existem.
    if reuse_existing and all(
        path.is_file() for path in expected_files
    ):
        logger.info(
            "Reutilizando separação existente: %s",
            audio_path.name,
        )
        return [str(path) for path in expected_files]

    # Compatibilidade com separações feitas na pasta antiga.
    legacy_files = [
        output_dir
        / f"{audio_path.stem}_({stem})_{model_name}.wav"
        for stem in STEM_NAMES
    ]

    if reuse_existing and all(
        path.is_file() for path in legacy_files
    ):
        for old_path, new_path in zip(
            legacy_files, expected_files
        ):
            shutil.move(str(old_path), str(new_path))

        logger.info(
            "Separação existente organizada na pasta: %s",
            song_output_dir,
        )
        return [str(path) for path in expected_files]

    logger.info(
        "Iniciando nova separação: %s",
        audio_path.name,
    )

    separator = Separator(
        output_dir=str(song_output_dir),
        output_format="WAV",
        model_file_dir=str(model_dir),
    )

    separator.load_model(model_filename=model_filename)

    start_time = time.perf_counter()

    output_files = separator.separate(str(audio_path))

    elapsed_time = time.perf_counter() - start_time

    logger.info(
        "Separação concluída: %s | Tempo: %.2f segundos",
        audio_path.name,
        elapsed_time,
    )

    # Normaliza os caminhos retornados pela biblioteca.
    resolved_files = []
    for filename in output_files:
        path = Path(filename)

        if not path.is_absolute():
            path = song_output_dir / path

        resolved_files.append(str(path))

    return resolved_files

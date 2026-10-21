
from pathlib import Path

import librosa
import numpy as np


INSTRUMENT_NAMES = {
    "vocals": "Voz",
    "drums": "Bateria",
    "bass": "Baixo",
    "guitar": "Guitarra",
    "piano": "Piano",
    "other": "Outros instrumentos",
}

# Valores iniciais para testes; serão ajustados com músicas reais.
MIN_LEVEL_DBFS = -50.0
MAX_LEVEL_GAP_DB = 25.0


def detect_present_instruments(stem_paths: list[str | Path]) -> list[dict]:
    """Estima quais stems possuem sinal significativo."""

    measurements = []

    for stem_path in stem_paths:
        path = Path(stem_path)
        filename = path.name.lower()

        instrument_key = next(
            (
                key
                for key in INSTRUMENT_NAMES
                if key in filename
            ),
            None,
        )

        if instrument_key is None:
            continue

        audio, _ = librosa.load(
            str(path),
            sr=None,
            mono=True,
        )

        if audio.size == 0:
            level_dbfs = float("-inf")
        else:
            rms = float(np.sqrt(np.mean(np.square(audio))))
            level_dbfs = (
                20 * np.log10(rms)
                if rms > 0
                else float("-inf")
            )

        measurements.append({
            "instrument": INSTRUMENT_NAMES[instrument_key],
            "level_dbfs": level_dbfs,
        })

    if not measurements:
        return []

    loudest_level = max(
        item["level_dbfs"] for item in measurements
    )

    for item in measurements:
        item["present"] = (
            item["level_dbfs"] >= MIN_LEVEL_DBFS
            and item["level_dbfs"]
            >= loudest_level - MAX_LEVEL_GAP_DB
        )

    return measurements

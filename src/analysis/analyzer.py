from dataclasses import dataclass
from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

from ..config import (
    OUTPUT_DIR,
    SPECTROGRAM_HOP_LENGTH,
    SPECTROGRAM_N_FFT,
)


@dataclass
class AudioAnalysis:
    """Resultados da análise técnica de um áudio."""

    file_name: str
    sample_rate: int
    duration: float
    sample_count: int
    peak_amplitude: float
    rms: float
    spectrogram_path: Path | None = None


def calculate_audio_metrics(audio: np.ndarray, sample_rate: int) -> dict:
    """Calcula métricas básicas de um sinal de áudio."""
    if audio.size == 0:
        raise ValueError("O áudio está vazio.")

    return {
        "duration": float(
            librosa.get_duration(y=audio, sr=sample_rate)
        ),
        "sample_count": int(audio.size),
        "peak_amplitude": float(np.max(np.abs(audio))),
        "rms": float(np.sqrt(np.mean(audio**2))),
    }


def generate_spectrogram(
    audio: np.ndarray,
    sample_rate: int,
    destination: Path,
) -> Path:
    """Gera e salva o espectrograma de um sinal de áudio."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    spectrogram = np.abs(
        librosa.stft(
            audio,
            n_fft=SPECTROGRAM_N_FFT,
            hop_length=SPECTROGRAM_HOP_LENGTH,
        )
    )

    spectrogram_db = librosa.amplitude_to_db(
        spectrogram,
        ref=np.max,
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    try:
        image = librosa.display.specshow(
            spectrogram_db,
            sr=sample_rate,
            hop_length=SPECTROGRAM_HOP_LENGTH,
            x_axis="time",
            y_axis="log",
            ax=ax,
        )

        ax.set_title("Espectrograma da música")
        fig.colorbar(image, ax=ax, format="%+2.0f dB")
        fig.tight_layout()
        fig.savefig(destination, dpi=150)
    finally:
        plt.close(fig)

    return destination


def analyze_audio(
    audio_path: Path,
    generate_plot: bool = True,
    output_dir: Path = OUTPUT_DIR,
) -> AudioAnalysis:
    """
    Analisa um arquivo de áudio e, opcionalmente,
    salva seu espectrograma.
    """
    audio_path = Path(audio_path)

    if not audio_path.is_file():
        raise FileNotFoundError(
            f"Arquivo de áudio não encontrado: {audio_path}"
        )

    audio, sample_rate = librosa.load(
        audio_path,
        sr=None,
        mono=True,
    )

    metrics = calculate_audio_metrics(audio, sample_rate)
    spectrogram_path = None

    if generate_plot:
        spectrogram_dir = output_dir / "spectrograms"
        spectrogram_path = generate_spectrogram(
            audio,
            sample_rate,
            spectrogram_dir / f"{audio_path.stem}_spectrogram.png",
        )

    return AudioAnalysis(
        file_name=audio_path.name,
        sample_rate=sample_rate,
        spectrogram_path=spectrogram_path,
        **metrics,
    )



if __name__ == "__main__":
    print("estou em analyzer")

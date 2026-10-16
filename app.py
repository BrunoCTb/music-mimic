from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent
AUDIO_PATH = PROJECT_DIR / "audios" / "musiquinha.mp3"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def analisar_audio(caminho: Path) -> None:
    if not caminho.exists():
        print(f"Arquivo não encontrado: {caminho}")
        return

    # Carrega o áudio preservando a taxa de amostragem original.
    audio, sr = librosa.load(
        caminho,
        sr=None,
        mono=True,
    )

    duracao = librosa.get_duration(y=audio, sr=sr)
    pico = float(np.max(np.abs(audio)))
    rms = float(np.sqrt(np.mean(audio**2)))

    print("=== Análise inicial ===")
    print(f"Arquivo: {caminho.name}")
    print(f"Taxa de amostragem: {sr} Hz")
    print(f"Duração: {duracao:.2f} segundos")
    print(f"Amostras: {len(audio):,}")
    print(f"Pico de amplitude: {pico:.4f}")
    print(f"RMS médio: {rms:.4f}")

    # Espectrograma: mostra a distribuição das frequências ao longo do tempo.
    espectrograma = np.abs(
        librosa.stft(audio, n_fft=2048, hop_length=512)
    )

    espectrograma_db = librosa.amplitude_to_db(
        espectrograma,
        ref=np.max,
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    imagem = librosa.display.specshow(
        espectrograma_db,
        sr=sr,
        hop_length=512,
        x_axis="time",
        y_axis="log",
        ax=ax,
    )

    ax.set_title("Espectrograma da música")
    fig.colorbar(imagem, ax=ax, format="%+2.0f dB")
    fig.tight_layout()

    destino = OUTPUT_DIR / "espectrograma.png"
    fig.savefig(destino, dpi=150)
    plt.close(fig)

    print(f"Espectrograma salvo em: {destino}")


if __name__ == "__main__":
    analisar_audio(AUDIO_PATH)

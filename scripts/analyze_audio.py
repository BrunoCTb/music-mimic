import argparse

from src.analysis.analyzer import analyze_audio
from src.config import AUDIO_DIR, OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Analisa um arquivo de áudio."
    )
    parser.add_argument(
        "audio",
        nargs="?",
        default=str(AUDIO_DIR / "musiquinha.mp3"),
        help="Caminho do arquivo de áudio."
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Executa a análise sem gerar o espectrograma."
    )

    args = parser.parse_args()

    resultado = analyze_audio(
        audio_path=args.audio,
        generate_plot=not args.no_plot,
        output_dir=OUTPUT_DIR,
    )

    print("\n=== Análise do áudio ===")
    print(f"Arquivo: {resultado.file_name}")
    print(f"Taxa de amostragem: {resultado.sample_rate} Hz")
    print(f"Duração: {resultado.duration:.2f} segundos")
    print(f"Amostras: {resultado.sample_count:,}")
    print(f"Pico de amplitude: {resultado.peak_amplitude:.4f}")
    print(f"RMS médio: {resultado.rms:.4f}")

    if resultado.spectrogram_path:
        print(f"Espectrograma: {resultado.spectrogram_path}")


if __name__ == "__main__":
    main()


import argparse

from src.config import AUDIO_DIR, OUTPUT_DIR
from src.separator import separate_audio


def main():
    parser = argparse.ArgumentParser(
        description="Separa os componentes de uma música."
    )
    parser.add_argument(
        "audio",
        nargs="?",
        default=str(AUDIO_DIR / "musiquinha.mp3"),
        help="Caminho do arquivo de áudio."
    )

    args = parser.parse_args()

    arquivos = separate_audio(
        audio_path=args.audio,
        output_dir=OUTPUT_DIR / "separacao_6_stems",
    )

    print("\n=== Separação concluída ===")

    for arquivo in arquivos:
        print(arquivo)


if __name__ == "__main__":
    main()

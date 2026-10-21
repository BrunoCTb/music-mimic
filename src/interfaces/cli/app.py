
from pathlib import Path

from src.config import AUDIO_DIR
from src.game.session import prepare_singleplayer


def show_menu() -> str:
    print("\n=== MUSIC MIMIC ===")
    print("1. Singleplayer")
    print("0. Sair")

    return input("\nEscolha uma opção: ").strip()


def display_instruments(instruments: list[dict]) -> None:
    print("\n=== INSTRUMENTOS DETECTADOS ===")

    present = [
        item for item in instruments
        if item["present"]
    ]

    if not present:
        print("Nenhum instrumento foi identificado com confiança.")
        return

    for item in present:
        print(f"- {item['instrument']}")

    print("\nOutras faixas não atingiram o limite inicial:")
    for item in instruments:
        if not item["present"]:
            print(f"- {item['instrument']}")



def request_audio_path() -> Path | None:
    raw_path = input(
        "\nInforme o caminho do arquivo de música "
        "(ou digite 'voltar'): "
    ).strip()

    if raw_path.lower() == "voltar":
        return None

    # Permite informar caminhos entre aspas, como os copiados
    # do Windows Explorer.
    raw_path = raw_path.strip('"').strip("'")
    audio_path = Path(raw_path).expanduser()

    # Se o caminho relativo não existir no diretório atual,
    # procura também dentro da pasta de áudios do projeto.
    if not audio_path.is_absolute() and not audio_path.is_file():
        audio_path = AUDIO_DIR / audio_path

    audio_path = audio_path.resolve()

    if not audio_path.is_file():
        print("\nArquivo não encontrado.")
        return None

    return audio_path


def display_analysis(result) -> None:
    print("\n=== ANÁLISE CONCLUÍDA ===")
    print(f"Arquivo: {result.file_name}")
    print(f"Taxa de amostragem: {result.sample_rate} Hz")
    print(f"Duração: {result.duration:.2f} segundos")
    print(f"Número de amostras: {result.sample_count}")
    print(f"Amplitude de pico: {result.peak_amplitude:.4f}")
    print(f"RMS: {result.rms:.4f}")

    if result.spectrogram_path:
        print(f"Espectrograma: {result.spectrogram_path}")


def start_singleplayer() -> None:
    print("\n=== SINGLEPLAYER ===")
    audio_path = request_audio_path()

    if audio_path is None:
        return

    print("\nAnalisando música... Isso pode levar algum tempo.")

    
    try:
        result, instruments = prepare_singleplayer(audio_path)
    except Exception as exc:
        print(f"\nNão foi possível preparar a música: {exc}")
        return

    display_analysis(result)
    display_instruments(instruments)

    print("\nPreparação concluída.")



def main() -> None:
    while True:
        option = show_menu()

        if option == "1":
            start_singleplayer()
        elif option == "0":
            print("\nAté mais!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()

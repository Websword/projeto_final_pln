import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer



# Baixe o modelo e especifique o caminho do diretório onde ele está descompactado
MODEL_PATH = "model-br/vosk-model-small-pt-0.3"
# Verifica se o modelo existe
if not os.path.exists(MODEL_PATH):
    print("Por favor, baixe o modelo e descompacte-o na pasta especificada.")
    exit(1)

# Carrega o modelo do Vosk
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)  # Reconhecedor, taxa de amostragem 16 kHz

# Configurações para captura de áudio com PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

print("Iniciando a transcrição em tempo real...")

try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            # Extrai a transcrição do resultado
            text = json.loads(result).get("text", "")
            if text:
                print(f"Transcrição: {text}")
        else:
            partial_result = recognizer.PartialResult()
            partial_text = json.loads(partial_result).get("partial", "")
            # Mostra o resultado parcial enquanto fala
            if partial_text:
                print(f"Parcial: {partial_text}")

except KeyboardInterrupt:
    # Finaliza o processo de captura quando pressionar Ctrl+C
    print("Transcrição encerrada.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

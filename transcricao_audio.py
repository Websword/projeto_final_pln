from vosk import Model, KaldiRecognizer
import wave

# Carregar o modelo offline (exige download prévio do modelo)
model = Model("modelo_vosk_pt")  # Caminho para o modelo Vosk

# Carregando o arquivo de áudio
audio_file = wave.open('seu_audio.wav', 'rb')
recognizer = KaldiRecognizer(model, audio_file.getframerate())

while True:
    data = audio_file.readframes(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print(result)

audio_file.close()

import whisper
import pyaudio
import numpy as np
import soundfile as sf
import tempfile

# Carregar o modelo Whisper (você pode escolher "tiny", "base", "small", "medium" ou "large")
model = whisper.load_model("small")

# Configuração do PyAudio para capturar o áudio do microfone
CHUNK = 1024  # Tamanho do bloco de áudio
FORMAT = pyaudio.paInt16  # Formato de captura de áudio
CHANNELS = 1  # Mono
RATE = 16000  # Taxa de amostragem (16 kHz)
RECORD_SECONDS = 5  # Duração de cada captura de bloco (em segundos)

# Inicializar PyAudio
p = pyaudio.PyAudio()

# Abrir stream para captura de áudio
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Capturando áudio em tempo real... Pressione Ctrl+C para parar.")

try:
    while True:
        frames = []

        # Captura de áudio por um intervalo (RECORD_SECONDS)
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(np.frombuffer(data, dtype=np.int16))

        # Converter para um array NumPy
        audio_data = np.hstack(frames)

        # Salvar áudio temporariamente em um arquivo WAV
        with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
            sf.write(temp_audio_file.name, audio_data, RATE)
            
            # Fazer a transcrição usando Whisper
            result = model.transcribe(temp_audio_file.name, language="pt")
            print("Transcrição: ", result["text"])

except KeyboardInterrupt:
    # Parar a captura de áudio
    print("Finalizando...")
    stream.stop_stream()
    stream.close()
    p.terminate()

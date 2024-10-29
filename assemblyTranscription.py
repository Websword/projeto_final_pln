import pyaudio
import wave
import assemblyai as aai
import os
import time

# Defina sua chave de API
aai.settings.api_key = "73262562897b406caae400acd9d358b5"

# Inicializar o transcritor da AssemblyAI
transcriber = aai.Transcriber()

# Configuração do PyAudio para captura do áudio em tempo real
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5  # Gravação de blocos de 5 segundos

# Função para capturar áudio em tempo real e transcrever
def gravar_audio_e_transcrever():
    p = pyaudio.PyAudio()

    # Abrir stream de captura
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Gravando e transcrevendo áudio em tempo real... Pressione Ctrl+C para parar.")

    try:
        while True:
            frames = []

            # Gravar bloco de áudio por RECORD_SECONDS
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            # Salvar bloco de áudio em arquivo temporário
            wf = wave.open("temp_audio.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # Enviar para AssemblyAI para transcrição
            transcript = transcriber.transcribe("temp_audio.wav")

            # Exibir a transcrição
            print("Transcrição: ", transcript.text)

            # Remover o arquivo temporário após a transcrição
            os.remove("temp_audio.wav")

    except KeyboardInterrupt:
        print("Parando a gravação e transcrição.")
        stream.stop_stream()
        stream.close()
        p.terminate()

# Chamar a função para capturar e transcrever
gravar_audio_e_transcrever()

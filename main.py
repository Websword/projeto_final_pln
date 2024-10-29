import pygame
import math as mt
from matplotlib import image
import matplotlib
from PIL import ImageColor
from modelo import *
import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

# Funções existentes do jogo
dt = 0
direcao = "00"
terreno = 0
parar = False
esperar = 0
objetivos = [(268,130),(131,275),(344,382)]
mar = [(128, 255, 255),(245,137,142), (136, 0, 21), (153, 217, 234)]

# data_mapa = image.imread("imagens/exemplo.png")
data_limites = image.imread("imagens/mapa_limites.png")

fundo = pygame.image.load('imagens/mapa_navegavel_Color.png')
barco = pygame.image.load('imagens/BARCO01.png')
obj = pygame.image.load('tiles/chao.png')

pessoa_direita = pygame.image.load('imagens/PERSONAGEM03.png')
pessoa_esquerda = pygame.image.load('imagens/PERSONAGEM01.png')
pessoa_tras = pygame.image.load('imagens/PERSONAGEM02.png')

tela_parada = pygame.image.load("imagens/tela_parada.png")



barco2 = barco
imagem_original = barco
player_pos = pygame.Vector2(-10 - 270 * 20,-10 - 14 * 20)

velo = 2
y_acelerar = 0
x_acelerar = 0
rotacao = 0
turbo = 1
raiz_meio = mt.sqrt((velo**2)/2)

# Função de conversão de RGBA para RGB
def convert_rgba4hex(x):
    hex = (matplotlib.colors.to_hex(x))
    rgb = ImageColor.getcolor(hex, "RGB")
    return rgb

# Função para rotacionar o barco
def rotacinar_barco(x, y, rot):
    if x < 0:
        if y > 0:
            return 270+45
        elif y < 0:
            return 270-45
        else:
            return 270
    elif x > 0:
        if y > 0:
            return 45
        elif y < 0:
            return 90+45
        else:
            return 90
    else:
        if y > 0:
            return 0
        elif y < 0:
            return 180
        else:
            return rot

# Integração com a transcrição de áudio e predição de ação
MODEL_PATH = "model-br/vosk-model-small-pt-0.3"
if not os.path.exists(MODEL_PATH):
    print("Por favor, baixe o modelo e descompacte-o na pasta especificada.")
    exit(1)

model_vosk = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model_vosk, 16000)



# Configurações de captura de áudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=4096)  # Ajustar tamanho do buffer

stream.start_stream()

# Função para capturar comandos de voz
def capturar_comando():
    data = stream.read(1024, exception_on_overflow=False)  # Prevenir overflow
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        text = json.loads(result).get("text", "")
        if text:
            print(f"Comando reconhecido: {text}")
            return text
    return ""


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 650))
clock = pygame.time.Clock()
running = True

while running:
    if parar:
         comando_voz = capturar_comando()
         if comando_voz:
            # Predição da ação com base no comando
            acao = retorna_acao([comando_voz])

            # Atualização da direção do barco
            if acao == "move_up":
                if direcao[0] == "0":
                        if direcao[1] == "S":
                            y_acelerar = 0
                            direcao = "00"
                        elif direcao[1] == "0":
                            y_acelerar = velo
                            direcao = "0N"
                        elif direcao[1] == "L":
                            y_acelerar = raiz_meio
                            x_acelerar = -raiz_meio
                            direcao = "NL"
                        elif direcao[1] == "O":
                            y_acelerar = raiz_meio
                            x_acelerar = raiz_meio
                            direcao = "NO"
                        else:
                            y_acelerar = velo

                elif direcao[0] == "S":
                        if direcao[1] == "L":
                            y_acelerar = 0
                            direcao = "0L"
                        elif direcao[1] == "O":
                            y_acelerar = 0
                            direcao = "0O"


                else:
                        y_acelerar = velo
                        x_acelerar = 0
                        direcao = "0N"

                parar = False
                esperar = 2
                turbo = 1

            if acao == "move_down":

                if direcao[0] == "0":
                    if direcao[1] == "N":
                        y_acelerar = 0
                        direcao = "00"
                    elif direcao[1] == "0":
                        y_acelerar = -velo
                        direcao = "0S"
                    elif direcao[1] == "L":
                        y_acelerar = -raiz_meio
                        x_acelerar = -raiz_meio
                        direcao = "SL"
                    elif direcao[1] == "O":
                        y_acelerar = -raiz_meio
                        x_acelerar = raiz_meio
                        direcao = "SO"
                    else:
                        y_acelerar = -velo


                elif direcao[0] == "N":
                        if direcao[1] == "L":
                            y_acelerar = 0
                            direcao = "0L"
                        elif direcao[1] == "O":
                            y_acelerar = 0
                            direcao = "0O"

                else:
                        y_acelerar = -velo
                        x_acelerar = 0
                        direcao = "0S"
                parar =False
                esperar = 2
                turbo = 1



            if acao == "move_left":

                if direcao[0] == "0":
                        if direcao[1] == "L":
                            x_acelerar = 0
                            direcao = "00"
                        elif direcao[1] == "0":
                            x_acelerar = velo
                            direcao = "0O"
                        elif direcao[1] == "S":
                            x_acelerar = raiz_meio
                            y_acelerar = -raiz_meio
                            direcao = "SO"
                        elif direcao[1] == "N":
                            x_acelerar = raiz_meio
                            y_acelerar = raiz_meio
                            direcao = "NO"
                        else:
                            x_acelerar = velo


                elif direcao[1] == "L":
                        if direcao[0] == "N":
                            x_acelerar = 0
                            direcao = "0N"
                        elif direcao[0] == "S":
                            x_acelerar = 0
                            direcao = "0S"


                else:
                        x_acelerar = velo
                        y_acelerar = 0
                        direcao = "0O"
                parar =False
                esperar = 2
                turbo = 1

            if acao == "move_right":
                if direcao[0] == "0":
                        if direcao[1] == "O":
                            x_acelerar = 0
                            direcao = "00"
                        elif direcao[1] == "0":
                            x_acelerar = -velo
                            direcao = "0L"
                        elif direcao[1] == "S":
                            x_acelerar = -raiz_meio
                            y_acelerar = -raiz_meio
                            direcao = "SL"
                        elif direcao[1] == "N":
                            x_acelerar = -raiz_meio
                            y_acelerar = raiz_meio
                            direcao = "NL"
                        else:
                            x_acelerar = -velo


                elif direcao[1] == "O":
                        if direcao[0] == "N":
                            x_acelerar = 0
                            direcao = "0N"
                        elif direcao[0] == "S":
                            x_acelerar = 0
                            direcao = "0S"

                            
                else:
                        x_acelerar = -velo
                        y_acelerar = 0
                        direcao = "0L"

                parar =False
                esperar = 2
                turbo = 1

            if acao == "turbo":
                turbo = 2
                parar =False
                esperar = 2
        
            if acao == "pause":
                x_acelerar = 0
                y_acelerar = 0
                turbo = 1
                parar =False
                esperar = 2
            # Atualização da posição do barco
            if terreno == 0:
                rotacao = rotacinar_barco(x_acelerar,y_acelerar,rotacao)
                barco2 = pygame.transform.rotate(imagem_original,rotacao)
            else:
                if (direcao[0] == 'N') or (direcao[1] == 'N'):
                    barco2 = pessoa_tras
                elif (direcao[1] == 'O'):
                    barco2 = pessoa_esquerda
                else:
                    barco2 = pessoa_direita

         dt = clock.tick(60) / 1000

    else:
        # Captura comando de voz
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            
            if event.type == pygame.QUIT:
                        running = False
            if keys[pygame.K_w]:
                 parar =True
            
            
                

            

        screen.fill("blue")


        if ((direcao[0]!= "0")):
            if direcao[0] == "S":
                if direcao[1] == "O":
                    x_acelerar = raiz_meio
                    y_acelerar = -raiz_meio
                else:
                    x_acelerar = -raiz_meio
                    y_acelerar = -raiz_meio

            else:
                if direcao[1] == "O":
                    x_acelerar = raiz_meio
                    y_acelerar = raiz_meio
                else:
                    x_acelerar = -raiz_meio
                    y_acelerar = raiz_meio

        if terreno == 0:
        
            if convert_rgba4hex(data_limites[int((player_pos.y+5)*-1),int(player_pos.x* -1)]) == (0,0,0):
                #print("norte")
                if y_acelerar > 0:
                    y_acelerar = 0
                    turbo = 1
            
            if convert_rgba4hex(data_limites[int((player_pos.y-5)*-1),int(player_pos.x* -1)])  == (0,0,0):
                #print("sul")
                if y_acelerar < 0:
                    y_acelerar = 0
                    turbo = 1

            if convert_rgba4hex(data_limites[int(player_pos.y *-1),int((player_pos.x+5) * -1)])  == (0,0,0):
                #print("oeste")
                if x_acelerar > 0:
                    x_acelerar = 0
                    turbo = 1
            
            if convert_rgba4hex(data_limites[int(player_pos.y *-1),int((player_pos.x-5) * -1)])  == (0,0,0):
                #print("leste")
                if x_acelerar < 0:
                    x_acelerar = 0
                    turbo = 1
                            




        else:
            if convert_rgba4hex(data_limites[int((player_pos.y+5)*-1),int(player_pos.x* -1)]) != (0,0,0):
                #print("norte")
                if y_acelerar > 0:
                    y_acelerar = 0
                    turbo = 1
            
            if convert_rgba4hex(data_limites[int((player_pos.y-5)*-1),int(player_pos.x* -1)])  != (0,0,0):
                #print("sul")
                if y_acelerar < 0:
                    y_acelerar = 0
                    turbo = 1

            if convert_rgba4hex(data_limites[int(player_pos.y *-1),int((player_pos.x+5) * -1)])  != (0,0,0):
                #print("oeste")
                if x_acelerar > 0:
                    x_acelerar = 0
                    turbo = 1
            
            if convert_rgba4hex(data_limites[int(player_pos.y *-1),int((player_pos.x-5) * -1)])  != (0,0,0):
                #print("leste")
                if x_acelerar < 0:
                    x_acelerar = 0
                    turbo = 1

        
        screen.blit(fundo,(screen.get_width() / 2 + player_pos.x, screen.get_height() / 2 +player_pos.y))

        if parar:
                screen.blit(tela_parada,(0,0))
        #print(int(((player_pos.y)//-20)),int((player_pos.x//-20)))

        if len(objetivos) > 0:

            objetivo_pos_x = screen.get_width() / 2 + player_pos.x+objetivos[0][0]*20 +10
            objetivo_pos_y = screen.get_height() / 2 + player_pos.y+objetivos[0][1]*20+10


            if (objetivo_pos_x > screen.get_width()):
                objetivo_pos_x = screen.get_width()
            elif (objetivo_pos_x < 0):
                objetivo_pos_x = 0
            
            
            if (objetivo_pos_y > screen.get_height()):
                objetivo_pos_y =screen.get_height()
            elif (objetivo_pos_y < 0):
                objetivo_pos_y = 0

            pygame.draw.circle(screen,"green",(objetivo_pos_x, objetivo_pos_y),10)

            pygame.draw.circle(screen,"white",(objetivo_pos_x, objetivo_pos_y),7,5)

            pygame.draw.circle(screen,"green",(objetivo_pos_x, objetivo_pos_y),5)

            if int(((player_pos.x)//-20))== objetivos[0][0]   and   int((player_pos.y//-20)) == objetivos[0][1]:
                print("entrou")
                objetivos.pop(0)
        else:
            terreno = 1
            player_pos.x -= 20
            objetivos = [(362,361),(362,421),(346,382)]
            x_acelerar = 0
            y_acelerar = 0
            barco2 = pessoa_direita

        if esperar <= 0:
            player_pos.y += 80 * dt * y_acelerar * turbo

            player_pos.x += 80 * dt * x_acelerar  * turbo
        else:
             esperar -=1

        screen.blit(barco2,(screen.get_width() / 2 - 10, screen.get_height() / 2 - 10))






        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()
                
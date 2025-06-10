import os, time
import json
from datetime import datetime
import pygame

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("log.dat","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.dat","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("log.dat","r")
    dados = banco.read()
    banco.close()
    print("dados",type(dados))
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("log.dat","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo

class TextInput:
    def __init__(self, font, max_lenght=16):
        self.text = ""
        self.font = font
        self.max_lenght = max_lenght
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.text.strip():
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable() and len(self.text) < self.max_lenght:
                self.text += event.unicode
        return False
    
    def draw(self, surface, x, y):
        text_surface = self.font.render(self.text + "|", True, (255,255,255))
        text_rect = text_surface.get_rect(midleft=(x,y))
        pygame.draw.rect(surface,(0,0,0), text_rect.inflate(20,10))
        surface.blit(text_surface, text_rect)
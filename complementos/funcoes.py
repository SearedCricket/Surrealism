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
        
    data_hora_br = datetime.now().strftime("%d/%m/%Y %H:%M")
    dadosDict[nome] = (pontos, data_hora_br)
    
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
        self._cursor_visible = True
        self._last_cursor_toggle = 0
        self._cursor_toggle_interval = 500

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
        text_surface = self.font.render(self.text + ('|' if self._cursor_visible else ''), True, (255,255,255))
        surface.blit(text_surface, (x,y))
        
        current_time = pygame.time.get_ticks()
        if current_time - self._last_cursor_toggle > self._cursor_toggle_interval:
            self._cursor_visible = not self._cursor_visible
            self._last_cursor_toggle = current_time
        
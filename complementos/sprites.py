import pygame
import os

def carregar_imagens(caminho_pasta, largura):
    imagens = []
    for arquivo in sorted(os.listdir(caminho_pasta)):
        if arquivo.endswith('.png'):
            imagem = pygame.image.load(os.path.join(caminho_pasta, arquivo))
            proporcao = imagem.get_height() / imagem.get_width()
            altura_desejada = int(largura * proporcao)
            imagem = pygame.transform.scale(imagem, (largura, altura_desejada))
            imagens.append(imagem)
    return imagens

class SpriteOlho(pygame.sprite.Sprite):
    def __init__(self, posicao, imagens):
        super().__init__()
        self.imagens = imagens
        self.indice_atual = 0
        self.image = self.imagens[self.indice_atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = posicao
        self.tempo_animacao = 200
        self.ultimo_tempo = pygame.time.get_ticks()

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tempo > self.tempo_animacao:
            self. indice_atual = (self.indice_atual + 1) % len(self.imagens)
            self.image = self.imagens[self.indice_atual]
            self.ultimo_tempo = agora
  
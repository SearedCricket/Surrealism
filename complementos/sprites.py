import pygame
import os
from PIL import Image
import random

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
  
def load_gif_frames(caminho_gif, largura_desejada=None):
    frames = []
    gif = Image.open(caminho_gif)

    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame = gif.convert("RGBA")
        if largura_desejada:
            proporcao = frame.height / frame.width
            nova_altura = int(largura_desejada * proporcao)
            frame = frame.resize((largura_desejada, nova_altura), Image.Resampling.LANCZOS)
        frame_data = frame.tobytes()
        size = frame.size
        mode = frame.mode
        py_frame = pygame.image.fromstring(frame_data, size, mode)
        frames.append(py_frame)
    return frames

class SpriteOlho2(pygame.sprite.Sprite):
    def __init__(self, posicao, frames):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect(center=posicao)

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

class BloodSplatter(pygame.sprite.Sprite):
    def __init__(self, position, gif_path):
        super().__init__()
        self.frames = load_gif_frames(gif_path, largura_desejada=200)
        self.current_frame = 0
        self.is_explosion = "explosion" in gif_path
        self.animation_speed = 0.2 if self.is_explosion else 0.3
        self.max_frames = len(self.frames) * 0.5 if self.is_explosion else len(self.frames)
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= self.max_frames:
            self.kill()
        else:
            self.image = self.frames[int(self.current_frame)]

class FloatingObject(pygame.sprite.Sprite):
    def __init__(self, position, image_path, speed=3):
        super().__init__()
        # Load and scale image
        original_image = pygame.image.load(image_path)
        target_width = 40
        original_ratio = original_image.get_height() / original_image.get_width()
        target_height = int(target_width * original_ratio)
        
        # Store the original scaled image
        self.original_image = pygame.transform.scale(original_image, (target_width, target_height))
        self.image = self.original_image
        
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.position = pygame.math.Vector2(position)
        self.angle = 0
        
    def update(self):
        # Smoother direction changes
        self.direction.rotate_ip(random.uniform(-0.2, 0.2))
        self.direction = self.direction.normalize()
        
        # Update position
        next_pos = self.position + self.direction * self.speed
        
        # Bounce off walls
        if next_pos.x <= 0 or next_pos.x >= 1000:
            self.direction.x *= -1
        if next_pos.y <= 0 or next_pos.y >= 700:
            self.direction.y *= -1
            
        self.position += self.direction * self.speed
        
        # Rotate smoothly
        self.angle = (self.angle + 0.5) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.position)
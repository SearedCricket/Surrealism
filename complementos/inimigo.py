import pygame
from random import choice, randint

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, image, screen_width):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = randint(3, 7)
        self.collided = False

    def update(self):
        
        self.rect.y += self.speed
        # Remove the enemy if it goes off screen (optional)

def spawn_inimigo_aleatorio(inimigo_images, tamanho, inimigo_group, inimigoClass):
    img = choice(inimigo_images)
    inimigo = inimigoClass(img, tamanho)
    inimigo_group.add(inimigo)

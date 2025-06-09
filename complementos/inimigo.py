import pygame, random

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, image, screen_width):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        # Remove the enemy if it goes off screen (optional)
        if self.rect.top > 700:
            self.kill()

def spawn_inimigo_aleatorio(inimigo_images, tamanho, inimigo_group, inimigoClass):
    img = random.choice(inimigo_images)
    inimigo = inimigoClass(img, tamanho)
    inimigo_group.add(inimigo)
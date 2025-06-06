import pygame, random

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, images, screen_width):
        super().__init__()
        self.images = images
        self.image_index = random.randint(0, len(images) - 1)
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 700:
            self.image_index = random.randint(0, len(self.images) - 1)
            self.image = self.images[self.image_index]
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, 1000 - self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = random.randint(3, 7)

def spawn_inimigo(inimigo_images, tamanho, inimigo_index, inimigo_group, inimigoClass):
    if inimigo_index < len(inimigo_images):
        inimigo = inimigoClass([inimigo_images[inimigo_index]], tamanho[0])
        inimigo_group.add(inimigo)
        return inimigo_index + 1
    return inimigo_index
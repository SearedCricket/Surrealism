import pygame
from random import choice, randint
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, image, x, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -self.rect.height
        self.speed = speed
        self.collided = False

    def update(self):
        self.rect.y += self.speed
        # Remove the enemy if it goes off screen (optional)

def spawn_inimigo_aleatorio(inimigo_images, screen_width, inimigo_group, Inimigo, target_x, points):
    base_range = 100
    range_decrease = min(points // 1, 50)
    spawn_range = max(base_range - range_decrease, 50)

    min_x = max(0, target_x - spawn_range)
    max_x = min(screen_width, target_x + spawn_range)

    base_speed = 5
    speed_increase = min(points // 3, 30)
    current_speed = base_speed + speed_increase

    x = randint(min_x, max_x)
    img = choice(inimigo_images)

    novo_inimigo = Inimigo(img, x, current_speed)
    inimigo_group.add(novo_inimigo)
    return randint(0, len(inimigo_images) - 1)
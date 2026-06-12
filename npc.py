import pygame
from config import *

class NPC:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Arvore:
    def __init__(self, x, y, numero_arvore):
        caminho_imagem = f'assets/image/cenario/arvore{numero_arvore}.png'
        self.image = pygame.image.load(caminho_imagem).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        base_altura = max(20, self.image.get_height() // 4)
        base_largura = max(20, self.image.get_width() // 2)
        self.collision_rect = pygame.Rect(
            self.rect.x + (self.image.get_width() - base_largura) // 2,
            self.rect.bottom - base_altura,
            base_largura,
            base_altura
        )
    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
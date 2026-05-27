import pygame
from config import *

class Player:

    def __init__(self):
        self.sprite_parado = pygame.image.load('assets/image/jonsnow/jogador.png').convert_alpha()
        self.sprite_baixo1 = pygame.image.load('assets/image/jonsnow/baixo1.png').convert_alpha()
        self.sprite_baixo2 = pygame.image.load('assets/image/jonsnow/baixo2.png').convert_alpha()
        self.sprite_cima1  = pygame.image.load('assets/image/jonsnow/cima1.png').convert_alpha()
        self.sprite_cima2  = pygame.image.load('assets/image/jonsnow/cima2.png').convert_alpha()
        self.sprite_dir1   = pygame.image.load('assets/image/jonsnow/direita1.png').convert_alpha()
        self.sprite_dir2   = pygame.image.load('assets/image/jonsnow/direita2.png').convert_alpha()
        self.sprite_dir3   = pygame.image.load('assets/image/jonsnow/direita3.png').convert_alpha()
        self.sprite_esq1   = pygame.image.load('assets/image/jonsnow/esquerda1.png').convert_alpha()
        self.sprite_esq2   = pygame.image.load('assets/image/jonsnow/esquerda2.png').convert_alpha()
        self.sprite_esq3   = pygame.image.load('assets/image/jonsnow/esquerda3.png').convert_alpha()

        self.image = self.sprite_parado
        
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed = 5

        self.direcao_atual = "parado"

        self.ultimo_tempo_baixo = 0
        self.tempo_animacao_baixo = 250
        self.sprite_atual_baixo = 1

        self.ultimo_tempo_cima = 0
        self.tempo_animacao_cima = 250
        self.sprite_atual_cima = 1

        self.ultimo_tempo_dir = 0
        self.tempo_animacao_dir = 250
        self.sprite_atual_dir = 1

        self.ultimo_tempo_esq = 0
        self.tempo_animacao_esq = 250
        self.sprite_atual_esq = 1

    def movement(self):
        keys = pygame.key.get_pressed()
        
        move_x = 0
        move_y = 0

        if keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_d]:
            move_x += 1
        if keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_s]:
            move_y += 1

        if move_x != 0 and move_y != 0:
            self.rect.x += int(move_x * (self.speed * 0.8))
            self.rect.y += int(move_y * (self.speed * 0.8))
        else:
            self.rect.x += int(move_x * self.speed)
            self.rect.y += int(move_y * self.speed)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT

        if move_x == 0 and move_y == 0:
            self.image = self.sprite_parado
            self.direcao_atual = "parado"
        elif move_x != 0 and move_y != 0:
            if move_x < 0:
                self.animar_esquerda()
            else:
                self.animar_direita()
        else:
            if move_x < 0:
                self.animar_esquerda()
            elif move_x > 0:
                self.animar_direita()
            elif move_y < 0:
                self.animar_cima()
            elif move_y > 0:
                self.animar_baixo()

    def animar_baixo(self):
        tempo_atual = pygame.time.get_ticks()

        if self.direcao_atual != "baixo":
            self.direcao_atual = "baixo"
            self.sprite_atual_baixo = 1
            self.image = self.sprite_baixo1
            self.ultimo_tempo_baixo = tempo_atual
            return

        if tempo_atual - self.ultimo_tempo_baixo > self.tempo_animacao_baixo:
            self.ultimo_tempo_baixo = tempo_atual
            
            if self.sprite_atual_baixo == 1:
                self.image = self.sprite_baixo2
                self.sprite_atual_baixo = 2
            else:
                self.image = self.sprite_baixo1
                self.sprite_atual_baixo = 1

    def animar_cima(self):
        tempo_atual = pygame.time.get_ticks()

        if self.direcao_atual != "cima":
            self.direcao_atual = "cima"
            self.sprite_atual_cima = 1
            self.image = self.sprite_cima1
            self.ultimo_tempo_cima = tempo_atual
            return

        if tempo_atual - self.ultimo_tempo_cima > self.tempo_animacao_cima:
            self.ultimo_tempo_cima = tempo_atual 
            
            if self.sprite_atual_cima == 1:
                self.image = self.sprite_cima2
                self.sprite_atual_cima = 2
            else:
                self.image = self.sprite_cima1
                self.sprite_atual_cima = 1

    def animar_direita(self):
        tempo_atual = pygame.time.get_ticks()

        if self.direcao_atual != "direita":
            self.direcao_atual = "direita"
            self.sprite_atual_dir = 1
            self.image = self.sprite_dir1
            self.ultimo_tempo_dir = tempo_atual
            return

        if tempo_atual - self.ultimo_tempo_dir > self.tempo_animacao_dir:
            self.ultimo_tempo_dir = tempo_atual
            
            self.sprite_atual_dir += 1
            if self.sprite_atual_dir > 3:
                self.sprite_atual_dir = 1
            
            if self.sprite_atual_dir == 1:
                self.image = self.sprite_dir1
            elif self.sprite_atual_dir == 2:
                self.image = self.sprite_dir2
            elif self.sprite_atual_dir == 3:
                self.image = self.sprite_dir3

    def animar_esquerda(self):
        tempo_atual = pygame.time.get_ticks()

        if self.direcao_atual != "esquerda":
            self.direcao_atual = "esquerda"
            self.sprite_atual_esq = 1
            self.image = self.sprite_esq1
            self.ultimo_tempo_esq = tempo_atual
            return

        if tempo_atual - self.ultimo_tempo_esq > self.tempo_animacao_esq:
            self.ultimo_tempo_esq = tempo_atual
            
            self.sprite_atual_esq += 1
            if self.sprite_atual_esq > 3:
                self.sprite_atual_esq = 1
            
            if self.sprite_atual_esq == 1:
                self.image = self.sprite_esq1
            elif self.sprite_atual_esq == 2:
                self.image = self.sprite_esq2
            elif self.sprite_atual_esq == 3:
                self.image = self.sprite_esq3

    def update(self):
        self.movement()

    def draw(self, screen, camera_x=0, camera_y=0):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
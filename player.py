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

        self.grama_image = pygame.image.load('assets/image/cenario/grama.png').convert_alpha()
        self.tile_size = self.grama_image.get_width()

        self.image = self.sprite_parado
        
        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)
        self.speed = 5

        self.direcao_atual = "parado"
        self.movendo_no_frame = False

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

#Requisito 2:
    def movement(self, arvores):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_TAB]:
            self.image = self.sprite_parado
            self.direcao_atual = "parado"
            self.movendo_no_frame = False
            return

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

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            move_x *= 1.67
            move_y *= 1.67
            self.tempo_animacao_baixo = 125
            self.tempo_animacao_cima = 125
            self.tempo_animacao_dir = 125
            self.tempo_animacao_esq = 125
        else:
            self.tempo_animacao_baixo = 250
            self.tempo_animacao_cima = 250
            self.tempo_animacao_dir = 250
            self.tempo_animacao_esq = 250

        if move_x != 0 or move_y != 0:
            self.velocidade = "andando"
        else:
            self.velocidade = "parado"

        pos_anterior_x = self.rect.x
        pos_anterior_y = self.rect.y

        if move_x != 0 and move_y != 0:
            vel_final_x = int(move_x * (self.speed * 0.75))
            vel_final_y = int(move_y * (self.speed * 0.75))
        else:
            vel_final_x = int(move_x * self.speed)
            vel_final_y = int(move_y * self.speed)

        self.rect.x += vel_final_x
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH

        self.rect.y += vel_final_y

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT

        self.check_collision(arvores)

        andou_x = self.rect.x != pos_anterior_x
        andou_y = self.rect.y != pos_anterior_y

        if andou_x or andou_y:
            self.movendo_no_frame = True
        else:
            self.movendo_no_frame = False

        if not andou_x and not andou_y:
            self.image = self.sprite_parado
            self.direcao_atual = "parado"
        else:
            if move_x < 0 and andou_x:
                self.animar_esquerda()
            elif move_x > 0 and andou_x:
                self.animar_direita()
            elif move_y < 0 and andou_y:
                self.animar_cima()
            elif move_y > 0 and andou_y:
                self.animar_baixo()
            else:
                if move_x != 0 and move_y != 0:
                    if move_x < 0:
                        self.animar_esquerda()
                    else:
                        self.animar_direita()

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
    def update(self, arvores):
        self.movement(arvores)

#Requisito 1:
    def draw_background(self, screen, camera_x, camera_y):
        start_x = max(0, (camera_x // self.tile_size) * self.tile_size)
        start_y = max(0, (camera_y // self.tile_size) * self.tile_size)

        end_x = min(WIN_WIDTH, camera_x + SCREEN_WIDTH + self.tile_size)
        end_y = min(WIN_HEIGHT, camera_y + SCREEN_HEIGHT + self.tile_size)

        for x in range(start_x, end_x, self.tile_size):
            for y in range(start_y, end_y, self.tile_size):
                largura_corte = self.tile_size
                altura_corte = self.tile_size

                if x + largura_corte > WIN_WIDTH:
                    largura_corte = WIN_WIDTH - x
                if y + altura_corte > WIN_HEIGHT:
                    altura_corte = WIN_HEIGHT - y

                if largura_corte > 0 and altura_corte > 0:
                    area_recorte = pygame.Rect(0, 0, largura_corte, altura_corte)
                    screen.blit(self.grama_image, (x - camera_x, y - camera_y), area_recorte)
    def draw(self, screen, camera_x=0, camera_y=0):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
    def check_collision(self, arvores):
        for arvore in arvores:
            
            alvo_colisao = getattr(arvore, 'hitbox', None)
            if alvo_colisao is None:
                alvo_colisao = getattr(arvore, 'collision_rect', None)
                
            if alvo_colisao and self.rect.colliderect(alvo_colisao):
                dx = self.rect.centerx - alvo_colisao.centerx
                dy = self.rect.centery - alvo_colisao.centery

                overlap_x = (self.rect.width // 2 + alvo_colisao.width // 2) - abs(dx)
                overlap_y = (self.rect.height // 2 + alvo_colisao.height // 2) - abs(dy)

                if overlap_x < overlap_y:
                    self.rect.x += int(overlap_x * (1 if dx > 0 else -1))
                else:
                    self.rect.y += int(overlap_y * (1 if dy > 0 else -1))
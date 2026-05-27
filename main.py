import pygame
import sys

from config import *
from player import *

class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = "menu" 
        
        self.player = Player()

        self.camera_x = 0
        self.camera_y = 0
        
        self.font = pygame.font.SysFont("Arial", 40, bold=True)

        self.music_menu = pygame.mixer.Sound('assets/audio/music/menu.mp3')
        self.music_jogo = pygame.mixer.Sound('assets/audio/music/jogo.mp3')

        self.channel_menu = pygame.mixer.Channel(0)
        self.channel_jogo = pygame.mixer.Channel(1)

        self.channel_menu.play(self.music_menu, loops=-1)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  
                        self.state = "game"
                        self.channel_menu.pause()
                        if not self.channel_jogo.get_busy():
                            self.channel_jogo.play(self.music_jogo, loops=-1)
                        else:
                            self.channel_jogo.unpause()
                    elif event.key == pygame.K_ESCAPE:  
                        self.running = False

            elif self.state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  
                        self.state = "menu"
                        self.channel_jogo.pause()
                        self.channel_menu.unpause()

    def update(self):
        if self.state == "game":
            self.player.update()

            keys = pygame.key.get_pressed()
            if not keys[pygame.K_TAB]:
                self.camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
                self.camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2

    def draw_menu(self):
        self.screen.fill(BLACK)
        
        titulo_texto = self.font.render(TITLE, True, RED)
        instrucao_texto = self.font.render("Pressione ENTER para Jogar", True, WHITE)
        sair_texto = self.font.render("Pressione ESC para Sair", True, GRAY)
        
        self.screen.blit(titulo_texto, (SCREEN_WIDTH // 2 - titulo_texto.get_width() // 2, 150))
        self.screen.blit(instrucao_texto, (SCREEN_WIDTH // 2 - instrucao_texto.get_width() // 2, 300))
        self.screen.blit(sair_texto, (SCREEN_WIDTH // 2 - sair_texto.get_width() // 2, 400))
        
        pygame.display.flip()

    def draw_tactical_map(self):
        self.screen.fill(BLACK)

        margem_w = 40
        margem_h = 40
        
        largura_mapa_tela = SCREEN_WIDTH - (margem_w * 2)
        altura_mapa_tela = SCREEN_HEIGHT - (margem_h * 2)

        if WIN_WIDTH > WIN_HEIGHT:
            altura_mapa_tela = int(largura_mapa_tela * (WIN_HEIGHT / WIN_WIDTH))
            margem_h = (SCREEN_HEIGHT - altura_mapa_tela) // 2
        else:
            largura_mapa_tela = int(altura_mapa_tela * (WIN_WIDTH / WIN_HEIGHT))
            margem_w = (SCREEN_WIDTH - largura_mapa_tela) // 2

        COR_GRAMA_TATICA = (34, 139, 34)
        pygame.draw.rect(self.screen, COR_GRAMA_TATICA, (margem_w, margem_h, largura_mapa_tela, altura_mapa_tela))
        pygame.draw.rect(self.screen, RED, (margem_w, margem_h, largura_mapa_tela, altura_mapa_tela), 3)

        escala_x = largura_mapa_tela / WIN_WIDTH
        escala_y = altura_mapa_tela / WIN_HEIGHT

        player_mini_x = margem_w + int(self.player.rect.x * escala_x)
        player_mini_y = margem_h + int(self.player.rect.y * escala_y)

        pygame.draw.rect(self.screen, RED, (player_mini_x - 4, player_mini_y - 4, 8, 8))

        pygame.display.flip()

    def draw_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            self.draw_tactical_map()
            return

        self.screen.fill(BLACK)

        self.player.draw_background(self.screen, self.camera_x, self.camera_y)

        borda_x = 0 - self.camera_x
        borda_y = 0 - self.camera_y
        pygame.draw.rect(self.screen, RED, (borda_x, borda_y, WIN_WIDTH, WIN_HEIGHT), 5)
        
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        
        pygame.display.flip()

    def main(self):
        while self.running:
            self.events()
            self.update()
            
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "game":
                self.draw_game()
                
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.main()

    pygame.quit()
    sys.exit()
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

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  
                        self.state = "game"
                    elif event.key == pygame.K_ESCAPE:  
                        self.running = False
            if self.state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  
                        self.state = "menu"

    def update(self):
        if self.state == "game":
            self.player.update()

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

    def draw_game(self):
            self.screen.fill(BLACK)

            self.player.draw_background(self.screen, self.camera_x, self.camera_y)

            borda_x = 0 - self.camera_x
            borda_y = 0 - self.camera_y
            
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
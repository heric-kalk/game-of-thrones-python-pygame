import pygame
import sys
import random

from config import *
from player import *
from npc import *

class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = "menu"  
        
        self.player = Player()
        self.cersei = NPC(WIN_WIDTH // 2, WIN_HEIGHT // 2, 'assets/image/cersei/parada.png')
        self.rei_noite = NPC(WIN_WIDTH - 400, WIN_HEIGHT - 400, 'assets/image/rei_noite/parado.png')

        self.selvagens = []
        for _ in range(20):
            x_aleatorio = random.randint(100, WIN_WIDTH - 100)
            y_aleatorio = random.randint(100, WIN_HEIGHT - 100)
            selvagem = NPC(x_aleatorio, y_aleatorio, 'assets/image/selvagens/parado.png')
            self.selvagens.append(selvagem)

        self.camera_x = 0
        self.camera_y = 0
        
        self.font = pygame.font.SysFont("Arial", 40, bold=True)

        self.music_menu = pygame.mixer.Sound('assets/audio/music/menu.mp3')
        self.music_jogo = pygame.mixer.Sound('assets/audio/music/jogo.mp3')

        self.channel_menu = pygame.mixer.Channel(0)
        self.channel_jogo = pygame.mixer.Channel(1)

        self.channel_menu.play(self.music_menu, loops=-1)

        self.som_andar1 = pygame.mixer.Sound('assets/audio/sound effect/andar1.mp3')
        self.som_andar2 = pygame.mixer.Sound('assets/audio/sound effect/andar2.mp3')
        self.som_andar3 = pygame.mixer.Sound('assets/audio/sound effect/andar3.mp3')
        self.sons_caminhada = [self.som_andar1, self.som_andar2, self.som_andar3]
        
        self.som_correr = pygame.mixer.Sound('assets/audio/sound effect/correr.mp3')
        
        self.passo_atual_index = 0
        self.tempo_ultimo_passo = 0
        self.tecla_pressionada_anteriormente = False
        self.correndo_anteriormente = False  

        self.vida_jon = 100
        self.vida_cersei = 100
        self.vida_rei = 200
        self.vida_sucesso = 0

        self.tempo_ultimo_turno = 0
        self.intervalo_turno = 1000  

        self.dados_rolados = []
        self.sucessos_diplomacia = 0
        self.mensagem_combate = ""
        self.turno_atual = "jon"
        self.inimigo_atual = ""

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "menu":
                self.som_correr.stop()
                self.correndo_anteriormente = False
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

            elif self.state in ["game", "diplomacy", "combat"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  
                        self.state = "menu"
                        self.channel_jogo.pause()
                        self.channel_menu.unpause()
                    
                    elif event.key == pygame.K_TAB and self.state == "game":
                        if self.correndo_anteriormente:
                            self.som_correr.stop() 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB and self.state == "game":
                        keys = pygame.key.get_pressed()
                        andando = keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]
                        correndo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
                        if andando and correndo:
                            self.som_correr.play(loops=-1)

    def gerenciar_audio_passos(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_TAB]:
            if self.correndo_anteriormente:
                self.som_correr.stop()
                self.correndo_anteriormente = False
            return

        andando = keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]
        correndo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if andando and correndo:
            if not self.correndo_anteriormente:
                self.som_correr.play(loops=-1)
                self.correndo_anteriormente = True
            self.tecla_pressionada_anteriormente = True
        else:
            if self.correndo_anteriormente:
                self.som_correr.stop()
                self.correndo_anteriormente = False

            if andando and not correndo:
                tempo_atual = pygame.time.get_ticks()
                intervalo_atual = 400
                
                if not self.tecla_pressionada_anteriormente:
                    self.sons_caminhada[self.passo_atual_index].play()
                    self.passo_atual_index = (self.passo_atual_index + 1) % len(self.sons_caminhada)
                    self.tempo_ultimo_passo = tempo_atual
                    self.tecla_pressionada_anteriormente = True
                
                elif tempo_atual - self.tempo_ultimo_passo > intervalo_atual:
                    self.sons_caminhada[self.passo_atual_index].play()
                    self.passo_atual_index = (self.passo_atual_index + 1) % len(self.sons_caminhada)
                    self.tempo_ultimo_passo = tempo_atual
            else:
                self.tecla_pressionada_anteriormente = False

    def gerenciar_encontros(self):
        for i in range(len(self.selvagens) - 1, -1, -1):
            selvagem = self.selvagens[i]
            distancia_selvagem = ((self.player.rect.x - selvagem.rect.x) ** 2 +
                                  (self.player.rect.y - selvagem.rect.y) ** 2) ** 0.5
            
            if distancia_selvagem <= 120:
                self.vida_jon -= 1  
                self.selvagens.pop(i)  
                
                if self.vida_jon <= 0:
                    self.som_correr.stop()
                    self.correndo_anteriormente = False
                    self.running = False
                return 

        distancia_cersei = ((self.player.rect.x - self.cersei.rect.x) ** 2 +
                            (self.player.rect.y - self.cersei.rect.y) ** 2) ** 0.5

        if distancia_cersei <= 80 and self.vida_cersei > 0 and self.vida_sucesso == 0:
            self.som_correr.stop()  
            self.correndo_anteriormente = False
            self.inimigo_atual = "cersei"
            self.state = "diplomacy"
            self.dados_rolados = []
            self.sucessos_diplomacia = 0
            self.tempo_ultimo_turno = pygame.time.get_ticks()
            return

        distancia_rei = ((self.player.rect.x - self.rei_noite.rect.x) ** 2 +
                         (self.player.rect.y - self.rei_noite.rect.y) ** 2) ** 0.5

        if distancia_rei <= 80 and self.vida_rei > 0:
            self.som_correr.stop()  
            self.correndo_anteriormente = False
            self.inimigo_atual = "rei"
            self.mensagem_combate = "O REI DA NOITE SE APROXIMA!"
            self.state = "combat"
            self.turno_atual = "jon"
            self.tempo_ultimo_turno = pygame.time.get_ticks()

    def atualizar_diplomacia(self):
        tempo_atual = pygame.time.get_ticks()

        if len(self.dados_rolados) < 5:
            if tempo_atual - self.tempo_ultimo_turno > 1000:
                self.tempo_ultimo_turno = tempo_atual
                dado = random.randint(1, 20)
                sucesso = dado >= 12
                if sucesso:
                    self.sucessos_diplomacia += 1
                self.dados_rolados.append((dado, sucesso))
        else:
            if tempo_atual - self.tempo_ultimo_turno > 2000:
                if self.sucessos_diplomacia >= 3:
                    self.vida_jon = 200
                    self.vida_sucesso = 1
                    self.player.rect.x += 120
                    self.state = "game"
                else:
                    self.mensagem_combate = "FALHA! O COMBATE COMEÇOU"
                    self.state = "combat"
                    self.turno_atual = "jon"
                    self.tempo_ultimo_turno = pygame.time.get_ticks()

    def atualizar_combate(self):
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.tempo_ultimo_turno > self.intervalo_turno:
            self.tempo_ultimo_turno = tempo_atual

            if self.turno_atual == "jon":
                ataque_jon = random.randint(1, 20)
                if ataque_jon >= 10:
                    if self.inimigo_atual == "cersei":
                        self.vida_cersei -= 10
                        self.mensagem_combate = f"Jon tirou {ataque_jon} [ACERTOU] Cersei HP: {self.vida_cersei}"
                    elif self.inimigo_atual == "rei":
                        self.vida_rei -= 10
                        self.mensagem_combate = f"Jon tirou {ataque_jon} [ACERTOU] Rei da Noite HP: {self.vida_rei}"
                else:
                    self.mensagem_combate = f"Jon tirou {ataque_jon} [ERROU]"
                
                if self.inimigo_atual == "cersei" and self.vida_cersei <= 0:
                    self.mensagem_combate = "Cersei Lannister foi derrotada!"
                    self.player.rect.x += 120  
                    self.state = "game"        
                    return
                elif self.inimigo_atual == "rei" and self.vida_rei <= 0:
                    self.mensagem_combate = "O Rei da Noite foi derrotado!"
                    self.player.rect.x += 120  
                    self.state = "game"        
                    return
                
                self.turno_atual = "inimigo"

            elif self.turno_atual == "inimigo":
                ataque_inimigo = random.randint(1, 20)
                
                if self.inimigo_atual == "cersei":
                    if ataque_inimigo >= 10:
                        self.vida_jon -= 10
                        self.mensagem_combate = f"Cersei tirou {ataque_inimigo} [ACERTOU] Jon HP: {self.vida_jon}"
                    else:
                        self.mensagem_combate = f"Cersei tirou {ataque_inimigo} [ERROU]"
                        
                elif self.inimigo_atual == "rei":
                    if ataque_inimigo >= 10:
                        self.vida_jon -= 5
                        self.vida_rei += 5
                        self.mensagem_combate = f"Rei da Noite tirou {ataque_inimigo} [ROUBOU VIDA] Rei: {self.vida_rei} | Jon: {self.vida_jon}"
                    else:
                        self.mensagem_combate = f"Rei da Noite tirou {ataque_inimigo} [ERROU]"
                
                if self.vida_jon <= 0:
                    self.mensagem_combate = "Jon Snow caiu em combate... Game Over!"
                    self.running = False
                
                self.turno_atual = "jon"

    def update(self):
        if self.state == "game":
            self.player.update()
            self.gerenciar_audio_passos()
            self.gerenciar_encontros()

            keys = pygame.key.get_pressed()
            if not keys[pygame.K_TAB]:
                self.camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
                self.camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2
                
        elif self.state == "diplomacy":
            self.atualizar_diplomacia()
        elif self.state == "combat":
            self.atualizar_combate()

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

        COR_SELVAGEM_MINI = (205, 133, 63)
        for selvagem in self.selvagens:
            s_mini_x = margem_w + int(selvagem.rect.x * escala_x)
            s_mini_y = margem_h + int(selvagem.rect.y * escala_y)
            pygame.draw.rect(self.screen, BLACK, (s_mini_x - 5, s_mini_y - 5, 10, 10))
            pygame.draw.rect(self.screen, COR_SELVAGEM_MINI, (s_mini_x - 4, s_mini_y - 4, 8, 8))

        if self.vida_rei > 0:
            rn_mini_x = margem_w + int(self.rei_noite.rect.x * escala_x)
            rn_mini_y = margem_h + int(self.rei_noite.rect.y * escala_y)
            COR_RN_MINI = (0, 0, 139)
            pygame.draw.rect(self.screen, BLACK, (rn_mini_x - 9, rn_mini_y - 9, 18, 18))
            pygame.draw.rect(self.screen, COR_RN_MINI, (rn_mini_x - 7, rn_mini_y - 7, 14, 14))

        if self.vida_cersei > 0:
            npc_mini_x = margem_w + int(self.cersei.rect.x * escala_x)
            npc_mini_y = margem_h + int(self.cersei.rect.y * escala_y)
            COR_CERSEI_MINI = (255, 0, 0)
            pygame.draw.rect(self.screen, BLACK, (npc_mini_x - 9, npc_mini_y - 9, 18, 18))
            pygame.draw.rect(self.screen, COR_CERSEI_MINI, (npc_mini_x - 7, npc_mini_y - 7, 14, 14))

        player_mini_x = margem_w + int(self.player.rect.x * escala_x)
        player_mini_y = margem_h + int(self.player.rect.y * escala_y)
        COR_JON_MINI = (128, 128, 128)
        pygame.draw.rect(self.screen, BLACK, (player_mini_x - 9, player_mini_y - 9, 18, 18))
        pygame.draw.rect(self.screen, COR_JON_MINI, (player_mini_x - 7, player_mini_y - 7, 14, 14))

        pygame.display.flip()

    def draw_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            self.draw_tactical_map()
            return

        self.screen.fill(BLACK)

        self.player.draw_background(self.screen, self.camera_x, self.camera_y)
        
        for selvagem in self.selvagens:
            selvagem.draw(self.screen, self.camera_x, self.camera_y)

        if self.vida_cersei > 0:
            self.cersei.draw(self.screen, self.camera_x, self.camera_y)
            
        if self.vida_rei > 0:
            self.rei_noite.draw(self.screen, self.camera_x, self.camera_y)
            
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        if self.state == "game":
            hud_vida = self.font.render(f"Jon Snow HP: {self.vida_jon}", True, WHITE)
            self.screen.blit(hud_vida, (SCREEN_WIDTH - hud_vida.get_width() - 30, 30))
        
        if self.state == "diplomacy":
            fundo_interface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fundo_interface.fill((0, 0, 0, 180))
            self.screen.blit(fundo_interface, (0, 0))
            
            titulo = self.font.render("Teste de Diplomacia (5d20 >= 12)", True, WHITE)
            self.screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 50))
            
            pos_y = 150
            for idx, (valor, sucesso) in enumerate(self.dados_rolados):
                cor = GREEN if sucesso else RED
                status = "SUCESSO" if sucesso else "FALHA"
                txt = self.font.render(f"Dado {idx+1}: {valor} ({status})", True, cor)
                self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, pos_y))
                pos_y += 60
                
            if len(self.dados_rolados) == 5:
                if self.sucessos_diplomacia >= 3:
                    resultado_txt = self.font.render(f"SUCESSO TOTAL! ({self.sucessos_diplomacia}/3) HP JON = 200", True, GREEN)
                else:
                    resultado_txt = self.font.render(f"FALHA TOTAL! ({self.sucessos_diplomacia}/3)", True, RED)
                self.screen.blit(resultado_txt, (SCREEN_WIDTH // 2 - resultado_txt.get_width() // 2, pos_y + 20))

        elif self.state == "combat":
            fundo_interface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fundo_interface.fill((0, 0, 0, 150))
            self.screen.blit(fundo_interface, (0, 0))
            
            hud_jon = self.font.render(f"Jon Snow HP: {self.vida_jon}", True, WHITE)
            
            if self.inimigo_atual == "cersei":
                hud_inimigo = self.font.render(f"Cersei HP: {self.vida_cersei}", True, RED)
            else:
                hud_inimigo = self.font.render(f"Rei da Noite HP: {self.vida_rei}", True, CYAN)
                
            self.screen.blit(hud_jon, (50, 40))
            self.screen.blit(hud_inimigo, (SCREEN_WIDTH - hud_inimigo.get_width() - 50, 40))
            
            if self.mensagem_combate:
                txt_combate = self.font.render(self.mensagem_combate, True, YELLOW)
                self.screen.blit(txt_combate, (SCREEN_WIDTH // 2 - txt_combate.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def main(self):
        while self.running:
            self.events()
            self.update()
            
            if self.state == "menu":
                self.draw_menu()
            elif self.state in ["game", "diplomacy", "combat"]:
                self.draw_game()
                
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.main()

    pygame.quit()
    sys.exit()
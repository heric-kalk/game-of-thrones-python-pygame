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
        self.luluzinha = NPC(WIN_WIDTH - 19600, WIN_HEIGHT - 550, 'assets/image/cenario/luluzinha.png')

        self.selvagens = []
        for _ in range(20):
            x_aleatorio = random.randint(100, WIN_WIDTH - 100)
            y_aleatorio = random.randint(100, WIN_HEIGHT - 100)
            selvagem = NPC(x_aleatorio, y_aleatorio, 'assets/image/selvagens/parado.png')
            self.selvagens.append(selvagem)

        self.arvores = []

        posicoes_arvores = {
        1: [
            (13537, 12776), (6856, 6158), (7845, 8440), (4666, 3137), (8529, 12852),
            (17693, 17949), (3243, 16332), (6836, 14116), (19580, 7400), (12554, 13017),
            (7266, 5289), (15421, 6165), (18876, 11402), (3018, 17624), (3177, 15669),
            (10667, 13493), (1697, 9127), (18582, 549), (14233, 6976), (12179, 17808),
            (2948, 15441), (17295, 6790), (15461, 1981), (12015, 4531), (7372, 5569),
            (14774, 6120), (16788, 6067), (1514, 3897), (1063, 5909), (15823, 14030),
            (2959, 14240), (3118, 4982), (10451, 485), (12786, 11103), (4750, 17450),
            (13581, 6879), (2115, 7228), (14815, 8740), (18173, 13540), (4440, 11893),
            (15902, 2129), (4590, 5229), (13679, 4375), (3461, 4190), (5007, 9998),
            (6006, 6121), (13730, 5068), (7101, 18681), (10756, 16655), (7964, 8740),
            (4140, 12152), (6393, 2672), (16724, 9727), (665, 19491), (1862, 11357),
            (7388, 12652), (13377, 11334), (13868, 12456), (17810, 3336), (6238, 1531),
            (12522, 13360), (14848, 7843), (10504, 7707), (10479, 3765), (10011, 14656),
            (2925, 14646), (14098, 8695), (2583, 16787), (9902, 10805), (15933, 17773),
            (4470, 8715), (14420, 9831), (13713, 5523), (9550, 12717), (14719, 6672),
            (6776, 11617), (441, 11942), (9979, 6633), (5924, 8851), (13954, 7877),
            (13677, 11622), (13403, 418), (3980, 16738), (17724, 6935), (342, 17408),
            (10475, 5784), (17048, 14852), (7027, 8947), (13958, 15636), (18662, 17700),
        ],
        2: [
            (9720, 6862), (975, 3745), (10376, 2776), (19322, 1347), (2210, 13956),
            (10121, 12398), (18559, 19567), (19138, 9972), (6657, 3580), (13232, 13356),
            (15400, 11082), (4509, 4581), (14932, 13047), (14002, 18711), (6160, 12091),
            (8497, 7103), (9264, 15476), (19065, 12838), (6318, 16001), (19069, 15909),
            (5853, 2749), (17721, 8150), (15369, 17443), (805, 4063), (11105, 16491),
            (2664, 11301), (429, 18965), (17765, 9322), (10755, 13863), (8870, 5738),
            (4761, 19572), (1856, 13317), (1484, 1864), (11519, 17055), (7835, 18494),
            (9873, 5494), (14687, 2184), (6476, 4139), (16181, 5930), (9239, 9327),
            (12265, 2614), (18640, 6795), (18617, 5989), (11889, 17829), (2969, 4021),
            (5221, 18169), (3134, 1384), (17101, 12727), (5757, 11896), (7887, 5579),
            (11444, 2030), (11519, 14591), (6460, 10375), (6184, 3941), (5102, 16571),
            (17380, 710), (7872, 12648), (3477, 8012), (18871, 14844), (2927, 5589),
            (5754, 14846), (12526, 8590), (10569, 19610), (1794, 19447), (13293, 967),
            (4649, 669), (9659, 18519), (4350, 16436), (14308, 2669), (1620, 11891),
            (5672, 10698), (11262, 11013), (1432, 12642), (9169, 7726), (18256, 5239),
            (907, 9762), (13392, 14033), (17086, 7765), (6006, 17474), (13612, 2088),
            (7252, 8222), (18885, 3378), (14544, 441), (18832, 1240), (6920, 4617),
            (6189, 10145), (2307, 8642), (6304, 19297), (14410, 5177),
        ],
        3: [
            (405, 1466), (16781, 13270), (14922, 2725), (5727, 19575), (7945, 11484),
            (14543, 4628), (15968, 3281), (12410, 16748), (5538, 7922), (7128, 3591),
            (5987, 4711), (15878, 8440), (5799, 17202), (16831, 18100), (2831, 7991),
            (8180, 17486), (7730, 14095), (13257, 17482), (18696, 2675), (8217, 8508),
            (10918, 18800), (1269, 1553), (10628, 6513), (1937, 9896), (6365, 9089),
            (8653, 632), (19215, 17677), (12245, 4038), (5519, 11590), (13054, 4962),
            (10296, 17695), (8832, 6791), (15124, 2126), (1191, 11930), (7889, 4924),
            (2866, 12738), (891, 12058), (10719, 12596), (8326, 17939), (5327, 2726),
            (1005, 1251), (6065, 7242), (7578, 11557), (8685, 2608), (324, 14523),
            (4034, 14581), (2953, 12416), (16591, 14185), (18595, 12615), (18624, 8912),
            (11017, 11600), (4123, 9254), (2411, 1388), (7499, 9051), (10984, 3657),
            (9179, 10353), (8266, 7267), (14792, 14872), (8882, 2843), (12864, 4296),
            (16493, 14769), (14253, 10815), (17817, 3768), (9689, 13353), (7129, 2532),
            (19666, 9467), (15169, 16359), (11391, 3089), (950, 1858), (18751, 3039),
            (4550, 13735), (17512, 19263), (880, 941), (4276, 10799), (7445, 6974),
            (3803, 716), (6301, 4718), (9699, 6107), (13910, 3730), (14017, 12953),
            (3455, 2845), (9113, 17548), (10257, 8498), (5487, 9282), (4351, 1451),
            (2588, 8518), (15814, 13117), (4508, 9827), (16171, 7427), (16736, 10347),
        ],
        4: [
            (16687, 8588), (6341, 15355), (9580, 5182), (6536, 11084), (17024, 4518),
            (16765, 7835), (11934, 17209), (2612, 7731), (18511, 14554), (5037, 19073),
            (310, 11367), (13392, 19329), (2998, 645), (14131, 3197), (14251, 15304),
            (3794, 3041), (457, 6693), (3186, 8219), (4052, 5103), (8748, 10474),
            (5976, 18485), (6524, 3216), (3955, 10904), (1123, 7443), (10057, 13555),
            (11270, 16812), (1703, 14816), (8495, 16012), (18068, 11750), (4583, 1709),
            (10952, 18430), (7887, 7138), (17441, 14215), (15904, 5660), (11688, 18564),
            (17794, 10351), (11573, 5307), (4504, 14590), (1800, 2538), (17795, 10771),
            (18586, 9897), (12192, 5968), (18439, 11077), (3593, 18296), (9985, 1378),
            (11544, 14181), (6809, 5463), (1619, 6052), (13112, 14348), (18129, 18151),
            (12734, 12510), (3743, 6977), (3531, 447), (10569, 8062), (9348, 13663),
            (1187, 18260), (16941, 17832), (8893, 4966), (8391, 13777), (17458, 18401),
            (12879, 3330), (11625, 1262), (16420, 7786), (15967, 2472), (8219, 16928),
            (1540, 4457), (11934, 18699), (17850, 1616), (2417, 792), (7381, 811),
            (15079, 6936), (17492, 15312), (16573, 402), (7398, 1763), (14436, 6344),
            (4415, 18299), (15296, 9754), (10182, 2152), (1367, 8464), (18963, 13192),
            (4762, 9613), (19104, 11723), (5203, 1345), (11102, 19175), (12519, 17872),
            (8948, 6118), (17091, 8625), (15983, 2900), (13051, 13815), (16009, 303),
        ],
        5: [
            (7895, 5965), (882, 5523), (17620, 7587), (10846, 13191), (12046, 13443),
            (5587, 8988), (12572, 5736), (498, 5403), (18222, 15493), (15525, 9397),
            (16072, 10737), (6111, 11039), (18872, 4922), (1881, 16794), (13372, 18477),
            (19550, 5324), (15605, 7246), (16688, 4157), (14178, 17731), (10662, 11064),
            (3232, 7634), (5434, 8310), (13655, 7839), (6347, 2250), (2151, 3123),
            (15724, 12743), (14642, 11416), (16869, 526), (6279, 18524), (14346, 14539),
            (10754, 9377), (5825, 4998), (16068, 18935), (12567, 4750), (16142, 14848),
            (16264, 10128), (17855, 14937), (15503, 3515), (16156, 1396), (15193, 6616),
            (4274, 11619), (16350, 680), (12784, 14585), (10601, 2260), (6700, 4441),
            (14378, 18027), (310, 4002), (4439, 19591), (7531, 8617), (962, 11635),
            (2271, 1723), (6876, 1577), (6608, 7499), (7071, 7291), (8962, 15906),
            (11849, 12317), (11662, 11364), (8291, 9877), (869, 15106), (3730, 5786),
            (19361, 1647), (7295, 13405), (9552, 12384), (11445, 6400), (15728, 11253),
            (10182, 16031), (15685, 1239), (8655, 17861), (3255, 11178), (3841, 1225),
            (14217, 12525), (415, 6031), (12511, 12061), (12272, 19619), (11411, 9133),
            (10782, 8993), (13083, 5782), (7862, 10416), (17946, 2881), (2661, 2972),
            (6925, 3952), (11574, 13039), (10813, 7537), (8347, 2060), (8530, 18722),
            (12654, 9100), (5853, 19280), (1050, 2325), (10300, 11884), (15678, 5050),
        ],
        6: [
            (2257, 4785), (9724, 11897), (19250, 8782), (8401, 10622), (8135, 2344),
            (14442, 4002), (3049, 18644), (6066, 332), (19688, 6619), (10678, 16344),
            (12898, 12091), (4878, 7924), (7334, 14328), (16998, 15165), (9500, 13942),
            (6741, 14924), (7729, 9520), (17292, 1526), (1325, 6784), (9214, 14631),
            (783, 2616), (3153, 5867), (814, 8453), (3170, 4341), (2741, 2556),
            (2887, 922), (9119, 12471), (1837, 14336), (6188, 15673), (6720, 17096),
            (15475, 10806), (2796, 11915), (6004, 10490), (10368, 1699), (1759, 17182),
            (18370, 10660), (8013, 15608), (18440, 13942), (7226, 4356), (1404, 5655),
            (16044, 4205), (6286, 6911), (4571, 5911), (19566, 8977), (7144, 17259),
            (17854, 891), (14740, 15168), (9176, 19218), (8616, 17307), (18637, 15526),
            (17072, 3862), (4728, 2539), (2580, 5915), (4407, 17452), (19487, 14036),
            (9838, 837), (8559, 12137), (16105, 11735), (18937, 15477), (5816, 11551),
            (12508, 8247), (7172, 9415), (9411, 7575), (4401, 15890), (9416, 8725),
            (7346, 10268), (1257, 17397), (767, 12715), (4476, 17885), (9218, 18699),
            (13050, 17113), (19075, 6253), (17899, 12490), (1095, 17070), (3673, 16089),
            (3728, 14517), (10294, 16870), (17329, 16236), (396, 3047), (15209, 19251),
            (19561, 12381), (8303, 11596), (1111, 4210), (7139, 7797), (1754, 10425),
            (15446, 8667), (2170, 6082), (7062, 19624), (3140, 3039), (12802, 6333),
        ],
        7: [
            (17760, 14618), (5102, 7158), (18946, 14306), (10073, 3784), (3033, 2544),
            (16835, 2859), (2562, 13387), (9879, 15805), (11120, 19523), (14447, 19601),
            (10987, 5897), (14999, 4750), (13670, 15509), (12547, 12737), (11790, 2770),
            (17170, 1809), (7305, 16381), (17333, 17801), (1003, 14791), (3358, 14772),
            (19642, 13746), (16024, 905), (17758, 13027), (2382, 19465), (13533, 4695),
            (631, 10631), (6687, 9133), (9990, 15367), (5453, 1214), (2717, 19386),
            (17435, 10702), (15477, 1484), (1784, 15786), (6399, 5434), (11065, 1495),
            (18954, 19303), (19645, 13288), (3160, 16638), (17669, 5332), (15105, 5065),
            (2215, 17612), (5357, 13159), (7808, 7701), (8623, 4769), (4980, 996),
            (8735, 9448), (11679, 15674), (6811, 12828), (14803, 18860), (10475, 3454),
            (17214, 16672), (2026, 12424), (7730, 4492), (10738, 660), (301, 4649),
            (14447, 17104), (576, 11502), (17385, 14554), (7813, 2503), (11604, 19230),
            (3844, 1558), (13438, 1500), (11014, 9773), (2852, 8320), (3482, 17731),
            (17389, 3760), (3520, 15451), (7604, 5379), (4755, 12139), (3653, 10976),
            (16378, 6426), (11564, 18069), (19625, 12871), (6777, 16634), (11336, 10412),
            (15015, 4320), (328, 19597), (13210, 8609), (8167, 10132), (7753, 14387),
            (1813, 404), (14423, 14963), (8779, 12459), (6611, 17876), (8423, 19313),
            (3807, 11328), (6272, 7630), (18009, 18812), (11742, 14769), (19338, 13660),
        ],
        8: [
            (14986, 10406), (12848, 15271), (8847, 11724), (16379, 17341), (18360, 4858),
            (12523, 7368), (19271, 18624), (14001, 8962), (14703, 17399), (6009, 9730),
            (3466, 10048), (4311, 13437), (6071, 13105), (15396, 7887), (2054, 1197),
            (18722, 16476), (19426, 18106), (7428, 1429), (3809, 2219), (17419, 7888),
            (8790, 11173), (19356, 13192), (4228, 3497), (4255, 15394), (5949, 6981),
            (487, 5071), (16939, 7367), (1144, 12325), (4064, 2422), (12230, 9927),
            (13587, 6503), (19077, 13516), (352, 16655), (18592, 3732), (11922, 4845),
            (6351, 14498), (15568, 11713), (10809, 15073), (19540, 16119), (8841, 4161),
            (5369, 16457), (9953, 5847), (14848, 17919), (517, 2011), (17916, 5061),
            (14707, 4388), (2269, 16170), (325, 8830), (1545, 2747), (2451, 10877),
            (7464, 7709), (9410, 19544), (4258, 17197), (2290, 11304), (539, 14941),
            (15856, 19550), (18207, 6244), (13162, 9123), (15361, 13136), (6514, 11755),
            (10984, 1189), (5830, 10200), (13041, 2169), (2174, 18405), (4065, 17664),
            (5323, 12579), (5981, 12558), (2614, 3610), (4741, 12598), (9267, 6830),
            (18307, 6781), (9461, 16181), (4522, 18609), (5361, 13870), (10225, 10930),
            (1176, 13205), (13232, 13045), (13817, 17273), (3872, 9806), (7766, 8113),
            (13196, 16002), (16934, 14034), (922, 16839), (17485, 10367), (4038, 6278),
            (1423, 16928), (10688, 7060), (7386, 2104), (3388, 6451),
        ],
    }

        for numero, posicoes in posicoes_arvores.items():
            for (x, y) in posicoes:
                nova_arvore = Arvore(x, y, numero)
                self.arvores.append(nova_arvore)

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
                    
                    elif event.key == pygame.K_TAB and self.state == "game":
                        if self.correndo_anteriormente:
                            self.som_correr.stop() 

                    elif event.key == pygame.K_RETURN:
                        if self.state == "diplomacy" and len(self.dados_rolados) < 5:
                            self.rolar_dado_diplomacia()
                        
                        elif self.state == "combat" and self.turno_atual == "jon":
                            self.executar_ataque_jon()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB and self.state == "game":
                        keys = pygame.key.get_pressed()
                        andando = keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]
                        correndo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
                        if andando and correndo:
                            self.som_correr.play(loops=-1)

    def rolar_dado_diplomacia(self):
        dado = random.randint(1, 20)
        sucesso = dado >= 12
        if sucesso:
            self.sucessos_diplomacia += 1
        self.dados_rolados.append((dado, sucesso))
        self.tempo_ultimo_turno = pygame.time.get_ticks()

    def executar_ataque_jon(self):
        ataque_jon = random.randint(1, 20)
        if ataque_jon >= 10:
            if self.inimigo_atual == "cersei":
                self.vida_cersei -= 10
                self.mensagem_combate = f"Jon tirou {ataque_jon} ACERTOU Cersei HP: {self.vida_cersei}"
            elif self.inimigo_atual == "rei":
                self.vida_rei -= 10
                self.mensagem_combate = f"Jon tirou {ataque_jon} ACERTOU Rei da Noite HP: {self.vida_rei}"
        else:
            self.mensagem_combate = f"Jon tirou {ataque_jon} ERROU"
        
        self.turno_atual = "inimigo"
        self.tempo_ultimo_turno = pygame.time.get_ticks()

    def gerenciar_audio_passos(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_TAB]:
            if self.correndo_anteriormente:
                self.som_correr.stop()
                self.correndo_anteriormente = False
            return

        correndo = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        se_mexeu = self.player.movendo_no_frame

        if se_mexeu and correndo:
            if not self.correndo_anteriormente:
                self.som_correr.play(loops=-1)
                self.correndo_anteriormente = True
            self.tecla_pressionada_anteriormente = True
        else:
            if self.correndo_anteriormente:
                self.som_correr.stop()
                self.correndo_anteriormente = False

            if se_mexeu and not correndo:
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

        if len(self.dados_rolados) == 5:
            if tempo_atual - self.tempo_ultimo_turno > 2000:
                if self.sucessos_diplomacia >= 3:
                    self.vida_jon += 100
                    self.vida_sucesso = 1
                    self.player.rect.x += 120
                    self.state = "game"
                else:
                    self.mensagem_combate = "FALHA O COMBATE COMECOU"
                    self.state = "combat"
                    self.turno_atual = "jon"
                    self.tempo_ultimo_turno = pygame.time.get_ticks()

    def atualizar_combate(self):
        tempo_atual = pygame.time.get_ticks()

        if self.turno_atual == "jon":
            if self.inimigo_atual == "cersei" and self.vida_cersei <= 0:
                self.mensagem_combate = "Cersei Lannister foi derrotada!"
                self.player.rect.x -= 120  
                self.state = "game"        
                return
            elif self.inimigo_atual == "rei" and self.vida_rei <= 0:
                self.mensagem_combate = "O Rei da Noite foi derrotado!"
                self.player.rect.x += 120
                self.state = "game"
                return

        elif self.turno_atual == "inimigo":
            if tempo_atual - self.tempo_ultimo_turno > self.intervalo_turno:
                self.tempo_ultimo_turno = tempo_atual
                
                ataque_inimigo = random.randint(1, 20)
                
                if self.inimigo_atual == "cersei":
                    if ataque_inimigo >= 10:
                        self.vida_jon -= 10
                        self.mensagem_combate = f"Cersei tirou {ataque_inimigo} ACERTOU Jon HP: {self.vida_jon}"
                    else:
                        self.mensagem_combate = f"Cersei tirou {ataque_inimigo} ERROU"
                        
                elif self.inimigo_atual == "rei":
                    if ataque_inimigo >= 10:
                        self.vida_jon -= 5
                        self.vida_rei += 5
                        self.mensagem_combate = f"Rei da Noite tirou {ataque_inimigo} ROUBOU VIDA Rei: {self.vida_rei} | Jon: {self.vida_jon}"
                    else:
                        self.mensagem_combate = f"Rei da Noite tirou {ataque_inimigo} ERROU"
                
                if self.vida_jon <= 0:
                    self.mensagem_combate = "Jon Snow caiu em combate... Game Over!"
                    self.running = False
                
                self.turno_atual = "jon"

    def update(self):
        if self.state == "game":
            self.player.update(self.arvores)
            self.gerenciar_audio_passos()
            self.gerenciar_encontros()
            self.player.check_collision(self.arvores)

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

        COR_ARVORE_MINI = (0, 100, 0)
        for arvore in self.arvores:
            a_mini_x = margem_w + int(arvore.rect.x * escala_x)
            a_mini_y = margem_h + int(arvore.rect.y * escala_y)
            pygame.draw.circle(self.screen, COR_ARVORE_MINI, (a_mini_x, a_mini_y), 4)

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
        
        self.luluzinha.draw(self.screen, self.camera_x, self.camera_y)

        self.player.draw(self.screen, self.camera_x, self.camera_y)

        for arvore in self.arvores:
            arvore.draw(self.screen, self.camera_x, self.camera_y)

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
                    resultado_txt = self.font.render(f"SUCESSO TOTAL! ({self.sucessos_diplomacia}/3) HP JON = {self.vida_jon + 100}", True, GREEN)
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
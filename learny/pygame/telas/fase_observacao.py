import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class FaseObservacao:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tempo_inicio_tela = None  # Armazena o tempo de início da tela

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-fase-observacao.png')
        )
        self.painel_jacare_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'jacare-apagado.png')
        )
        self.painel_jacare_aceso_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'jacare-aceso.png')
        )
        self.painel_macaco_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'macaco-apagado.png')
        )
        self.painel_macaco_aceso_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'macaco-aceso.png')
        )
        self.painel_formiga_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'formiga-apagada.png')
        )
        self.painel_formiga_acesa_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'formiga-acesa.png')
        )
        self.painel_alpaca_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'alpaca-apagada.png')
        )
        self.painel_alpaca_acesa_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'alpaca-acesa.png')
        )
        self.icon_confirmar_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icone-confirmar-vermelho.png')
        )
        self.audio_jacare = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'alligator.wav')
        )
        self.audio_macaco = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'ape.wav')
        )
        self.audio_formiga = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'ant.wav')
        )
        self.audio_alpaca = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'alpaca.wav')
        )
        
        self.estados_paineis = {
            "jacare": False,
            "macaco": False,
            "formiga": False,
            "alpaca": False
        }

    icon_confirmar = None
    painel_jacare = None
    painel_macaco = None
    painel_formiga = None
    painel_alpaca = None

    def desenhar(self, tela):
        if self.tempo_inicio_tela is None:  # Só define no início
            self.tempo_inicio_tela = pygame.time.get_ticks()
        
        tela.blit(self.background_image, (0, 0))
        
        painel_jacare_img = self.painel_jacare_aceso_image if self.estados_paineis["jacare"] else self.painel_jacare_image
        painel_macaco_img = self.painel_macaco_aceso_image if self.estados_paineis["macaco"] else self.painel_macaco_image
        painel_formiga_img = self.painel_formiga_acesa_image if self.estados_paineis["formiga"] else self.painel_formiga_image
        painel_alpaca_img = self.painel_alpaca_acesa_image if self.estados_paineis["alpaca"] else self.painel_alpaca_image
    
    
        self.painel_jacare = tela.blit(painel_jacare_img, (35, 365)) 
        self.painel_macaco = tela.blit(painel_macaco_img, (223, 365))
        self.painel_formiga = tela.blit(painel_formiga_img, (35, 520))
        self.painel_alpaca = tela.blit(painel_alpaca_img, (223, 520))
        
        self.icon_confirmar = tela.blit(self.icon_confirmar_image, (180, 640))

        # Atualizar a tela
        pygame.display.flip()

    def trocar_tela(self):
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - self.tempo_inicio_tela) / 1000  # Em segundos
        
        # Formata o tempo para MM:SS
        minutos, segundos = divmod(int(tempo_decorrido), 60)
        tempo_formatado = f"{minutos:02}:{segundos:02}"
        
        self.gerenciador.trocar_tela("conclusao_fase", tempo_formatado)

        self.tempo_inicio_tela = None
        
    def ativar_painel(self, painel, audio):
        self.estados_paineis[painel] = True  # Marca o painel como ativado (colorido)
        audio.play()  # Toca o áudio

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == QUIT:
                self.running = False
            
            # Detecta clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clique esquerdo
                        # Detecta cliques nos painel dos numeros
                        x, y = evento.pos

                        # Lista de áreas clicáveis e ações associadas
                        areas_clicaveis = [
                            {"area": self.painel_jacare, "acao": lambda: self.ativar_painel("jacare", self.audio_jacare)},
                            {"area": self.painel_macaco, "acao": lambda: self.ativar_painel("macaco", self.audio_macaco)},
                            {"area": self.painel_formiga, "acao": lambda: self.ativar_painel("formiga", self.audio_formiga)},
                            {"area": self.painel_alpaca, "acao": lambda: self.ativar_painel("alpaca", self.audio_alpaca)},
                            {"area": self.icon_confirmar, "acao": self.trocar_tela}
                        ]


                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                item["acao"]()  # Executa a ação associada
                                break


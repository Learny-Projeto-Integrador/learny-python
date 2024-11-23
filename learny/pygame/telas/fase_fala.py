import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class FaseFala:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tempo_inicio_tela = None  # Armazena o tempo de início da tela

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-fase-fala.png')
        )
        self.painel_red_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-red.png')
        )
        self.painel_head_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-head.png')
        )
        self.painel_heard_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-heard.png')
        )
        self.painel_read_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-read.png')
        )
        self.icon_audio_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icone-audio.png')
        )
        self.icon_confirmar_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icone-confirmar-vermelho.png')
        )
        self.audio_red = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'red.wav')
        )
        
    icon_audio = None
    icon_confirmar = None
    painel_red = None
    painel_head = None
    painel_heard = None
    painel_red = None

    def desenhar(self, tela):
        if self.tempo_inicio_tela is None:  # Só define no início
            self.tempo_inicio_tela = pygame.time.get_ticks()
        
        tela.blit(self.background_image, (0, 0))
        
        self.icon_audio = tela.blit(self.icon_audio_image, (45, 290))
    
        self.painel_red = tela.blit(self.painel_red_image, (50, 435)) 
        self.painel_head = tela.blit(self.painel_head_image, (208, 435))
        self.painel_heard = tela.blit(self.painel_heard_image, (50, 520))
        self.painel_read = tela.blit(self.painel_read_image, (208, 520))
        
        self.icon_confirmar = tela.blit(self.icon_confirmar_image, (180, 630))

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
                            {"area": self.icon_audio},
                            {"area": self.painel_red},
                            {"area": self.painel_head},
                            {"area": self.painel_heard},
                            {"area": self.painel_read},
                            {"area": self.icon_confirmar}
                        ]


                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                if item["area"] == self.icon_audio:
                                    self.audio_red.play()
                                elif item["area"] == self.icon_confirmar:
                                    self.trocar_tela()
                                break


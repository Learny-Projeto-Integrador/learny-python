import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class FaseNumeros:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tempo_inicio_tela = None  # Armazena o tempo de início da tela

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-fase-numeros.png')
        )
        self.painel_n5_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-num-5.png')
        )
        self.painel_n10_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-num-10.png')
        )
        self.painel_n20_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-num-20.png')
        )
        self.painel_n30_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-num-30.png')
        )
        self.audio_n5 = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'five.wav')
        )
        self.audio_n10 = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'ten.wav')
        )
        self.audio_n20 = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'twenty.wav')
        )
        self.audio_n30 = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'thirty.wav')
        )


    painel5_esquerda = None
    painel5_direita = None
    painel10 = None
    painel20 = None
    painel30 = None

    def desenhar(self, tela):
        if self.tempo_inicio_tela is None:  # Só define no início
            self.tempo_inicio_tela = pygame.time.get_ticks()
        
        tela.blit(self.background_image, (0, 0))  # Redesenhar a imagem de fundo
        self.painel5_esquerda = tela.blit(self.painel_n5_image, (60, 287))  # Redesenhar a imagem de fundo
        self.painel5_direita = tela.blit(self.painel_n5_image, (250, 287))  # Redesenhar a imagem de fundo
        self.painel10 = tela.blit(self.painel_n10_image, (35, 560))  # Redesenhar a imagem de fundo
        self.painel20 = tela.blit(self.painel_n20_image, (147, 560))  # Redesenhar a imagem de fundo
        self.painel30 = tela.blit(self.painel_n30_image, (260, 560))  # Redesenhar a imagem de fundo

        # Atualizar a tela
        pygame.display.flip()

    def trocar_tela(self, tela_destino):
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - self.tempo_inicio_tela) / 1000  # Em segundos

        print(f"Tempo na tela atual: {tempo_decorrido:.2f} segundos")
        
        self.gerenciador.trocar_tela("tela_inicial")

        self.tempo_inicio_tela = None

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
                            {"area": self.painel5_esquerda, "acao": lambda: self.audio_n5.play()},
                            {"area": self.painel5_direita, "acao": lambda: self.audio_n5.play()},
                            {"area": self.painel10, "acao": lambda: self.audio_n10.play()},
                            {"area": self.painel20, "acao": lambda: self.audio_n20.play()},
                            {"area": self.painel30, "acao": lambda: self.audio_n30.play()},
                        ]

                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                if item["area"] == self.painel10:
                                    item["acao"]()  # Executa a ação associada
                                    self.trocar_tela("tela-conclusao")
                                item["acao"]()  # Executa a ação associada
                                break


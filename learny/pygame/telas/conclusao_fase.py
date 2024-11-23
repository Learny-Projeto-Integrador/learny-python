import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class ConclusaoFase:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tempo_conclusao = None  # Armazena o tempo de início da tela

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-conclusao.png')
        )
        self.icon_fechar_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-fechar.png')
        )


    icon_fechar = None

    def desenhar(self, tela):
        
        tela.blit(self.background_image, (0, 0))  # Redesenhar a imagem de fundo
        self.icon_fechar = tela.blit(self.icon_fechar_image, (175, 625))  # Redesenhar a imagem de fundo

        # Atualizar a tela
        pygame.display.flip()

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
                        {"area": self.icon_fechar}
                    ]

                    # Verifica em qual área o clique ocorreu
                    for item in areas_clicaveis:
                        if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                            self.gerenciador.trocar_tela("tela_inicial")
                            break


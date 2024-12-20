import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class ConclusaoFase:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tempo = None 
        self.pontos = None

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-conclusao.png')
        )
        self.icon_fechar_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-fechar.png')
        )
        self.font = pygame.font.Font(
            os.path.join(self.assets_dir, 'assets', 'fonts', 'montserrat', 'Montserrat-Bold.ttf'), 20
        )



    def receber_dados(self, dados):
        self.tempo = dados[0]
        self.pontos = dados[1]
        self.porcentagem_acertos = "100%"
        if len(dados) > 2:
            self.porcentagem_acertos = dados[2]

    icon_fechar = None

    def desenhar(self, tela):
        
        tela.blit(self.background_image, (0, 0))  # Redesenhar a imagem de fundo
        self.icon_fechar = tela.blit(self.icon_fechar_image, (175, 625))  # Redesenhar a imagem de fundo
        
        pontos_fase = str(self.pontos)
        tempo_conclusao = str(self.tempo)
        porc_acertos = self.porcentagem_acertos
        
        texto_pontos = self.font.render(pontos_fase, True, (0,0,0))
        texto_tempo = self.font.render(tempo_conclusao, True, (0,0,0))
        texto_porc = self.font.render(porc_acertos, True, (0,0,0))

        # Centralizar os textos com base na posição especificada
        pos_pontos = self._centralizar_texto(115, 453, texto_pontos)
        pos_tempo = self._centralizar_texto(193, 562, texto_tempo)
        pos_porc = self._centralizar_texto(280, 453, texto_porc)

        tela.blit(texto_pontos, pos_pontos)
        tela.blit(texto_tempo, pos_tempo)
        tela.blit(texto_porc, pos_porc)

        # Atualizar a tela
        pygame.display.flip()
        
    def _centralizar_texto(self, x, y, texto):
        largura_texto = texto.get_width()
        altura_texto = texto.get_height()

        # Centraliza em relação ao ponto x, y
        return x - largura_texto // 2, y - altura_texto // 2

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


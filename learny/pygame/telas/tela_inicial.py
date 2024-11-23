import pygame
import os
import sys
import math
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class TelaInicial:
    def __init__(self, gerenciador, create_connection, close_connection, usuario_ativo):
        self.gerenciador = gerenciador  # Armazena a referência do gerenciador
        self.create_connection = create_connection
        self.close_connection = close_connection
        self.usuario_ativo = usuario_ativo
        self.dados_usuario = None
        self.scroll_y = 0

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-fase.png')
        )
        self.menu_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'retangulo-menu.png')
        )
        self.menu_image = pygame.transform.scale(self.menu_image, (LARGURA, 58))
        self.font = pygame.font.Font(
            os.path.join(self.assets_dir, 'assets', 'fonts', 'montserrat', 'Montserrat-Bold.ttf'), 20
        )

        # Configurações do personagem
        self.personagem = self.criar_personagem()
        self.todas_as_sprites = pygame.sprite.Group()
        self.todas_as_sprites.add(self.personagem)

        # Variáveis de rolagem
        self.scroll_y = 0
        self.scroll_speed = 10
        self.is_scrolling = False

        # Dimensões da superfície maior que a tela
        self.scrollable_height = 1000
        self.content_surface = pygame.Surface((LARGURA, self.scrollable_height))

        # Dimensões da barra de rolagem
        self.scrollbar_width = 10
        self.scrollbar_height = ALTURA * (ALTURA / self.scrollable_height)
        self.scrollbar_x = LARGURA - self.scrollbar_width
        self.scrollbar_y = 0

        # Configurações de menu
        self.menu_height = 58
        self.menu_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'retangulo-menu.png')
        )
        self.menu_image = pygame.transform.scale(self.menu_image, (LARGURA, self.menu_height))

        self.icone_perfil = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-perfil.png')
        )
        self.icone_home = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-home.png')
        )
        self.icone_menu_hamburguer = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-menu-hamburguer.png')
        )

        self.acessar_banco()

    def criar_personagem(self):
        sprite_sheet_path = os.path.join(self.assets_dir, 'assets', 'sprites', 'george.png')
        correndo_direita = [(144, 0), (144, 48), (144, 96), (144, 144)]
        correndo_esquerda = [(48, 0), (48, 48), (48, 96), (48, 144)]
        frame_size = (48, 48)
        scale_factor = 1.5
        return Personagem(sprite_sheet_path, correndo_direita, correndo_esquerda, frame_size, scale_factor, self.gerenciador)

    def desenhar(self, tela):
        # Atualiza os sprites no content_surface
        self.content_surface.fill((255, 255, 255))  # Preencher com fundo transparente ou branco
        self.content_surface.blit(self.background_image, (0, 0))  # Redesenhar a imagem de fundo
        self.todas_as_sprites.draw(self.content_surface)  # Desenha o personagem no content_surface

        pontos = str(self.dados_usuario["pontos"])
        medalhas = str(len(self.dados_usuario["medalhas"]))
        ranking = str(self.dados_usuario["rankAtual"])

        texto_pontos = self.font.render(pontos, True, (0,0,0))
        texto_medalhas = self.font.render(medalhas, True, (0,0,0))
        texto_ranking = self.font.render(ranking, True, (0,0,0))
        
        # Centralizar os textos com base na posição especificada
        pos_pontos = self._centralizar_texto(97, 102, texto_pontos)
        pos_medalhas = self._centralizar_texto(212, 102, texto_medalhas)
        pos_ranking = self._centralizar_texto(320, 101, texto_ranking)

        self.content_surface.blit(texto_pontos, pos_pontos)
        self.content_surface.blit(texto_medalhas, pos_medalhas)
        self.content_surface.blit(texto_ranking, pos_ranking)

        # Desenhar o content_surface na tela com o deslocamento do scroll
        tela.blit(self.content_surface, (0, -self.scroll_y))

        # Desenhar a barra de rolagem
        pygame.draw.rect(
            tela, (150, 150, 150), (self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height)
        )

        # Desenhar o menu fixo
        tela.blit(self.menu_image, (0, ALTURA - self.menu_height - 20))

        # Desenhar ícones do menu
        tela.blit(self.icone_perfil, (50, ALTURA - self.menu_height - 30))
        tela.blit(self.icone_home, (170, ALTURA - self.menu_height - 40))
        tela.blit(self.icone_menu_hamburguer, (300, ALTURA - self.menu_height - 30))

        # Atualizar a tela
        pygame.display.flip()
        
    def _centralizar_texto(self, x, y, texto):
        largura_texto = texto.get_width()
        altura_texto = texto.get_height()

        # Centraliza em relação ao ponto x, y
        return x - largura_texto // 2, y - altura_texto // 2
    
    def buscar_dados_crianca(self, usuario_banco):
        # Busca os dados da crianca ativa             
        if usuario_banco:
            return {
                'pontos': usuario_banco["pontos"],
                'medalhas': usuario_banco["medalhas"],
                'rankAtual': usuario_banco["rankAtual"],
            }
        return None
    
    def acessar_banco(self):
        # Exemplo de uso
        try:
            client, db = self.create_connection()
            if db is not None:

                criancas = db["criancas"]
                usuario_banco_crianca = criancas.find_one({"usuario": self.usuario_ativo})
                self.dados_usuario = self.buscar_dados_crianca(usuario_banco_crianca)
                
            else:
                print("Erro na conexão com o banco de dados.")
        finally:
            self.close_connection(client)
            print("Conexão fechada.")

    def atualizar(self, eventos):
        for evento in eventos:
            # Detecta clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clique esquerdo
                    # Detecta clique sobre a barra de rolagem
                    if (
                        self.scrollbar_x <= evento.pos[0] <= self.scrollbar_x + self.scrollbar_width and
                        self.scrollbar_y <= evento.pos[1] <= self.scrollbar_y + self.scrollbar_height
                    ):
                        self.is_scrolling = True
                    else:
                        # Detecta clique em círculos ou ícones do menu
                        x, y = evento.pos
                        menu_y = ALTURA - self.menu_height

                        # Lista de áreas clicáveis e ações associadas
                        areas_clicaveis = [
                            # Ícones do menu
                            {
                                "area": (50, menu_y - 30, 50 + self.icone_perfil.get_width(), menu_y - 30 + self.icone_perfil.get_height()),
                                "acao": lambda: self.retornar_para_kivy('TelaPerfil'),
                                "tipo": "retangulo",
                            },
                            {
                                "area": (170, menu_y - 40, 170 + self.icone_home.get_width(), menu_y - 40 + self.icone_home.get_height()),
                                "acao": lambda: self.retornar_para_kivy('TelaHome'),
                                "tipo": "retangulo",
                            },
                            {
                                "area": (300, menu_y - 30, 300 + self.icone_menu_hamburguer.get_width(), menu_y - 30 + self.icone_menu_hamburguer.get_height()),
                                "acao": lambda: self.retornar_para_kivy('TelaAtalhos'),
                                "tipo": "retangulo",
                            },
                            # Áreas circulares para movimentação do personagem
                            {
                                "area": (225, 675, 40),
                                "acao": lambda: self.personagem.mover_para((190, 635),"fase_observacao") or self.personagem.set_estado("correndo_direita"),
                                "tipo": "circulo",
                            },
                            {
                                "area": (290, 527, 40),
                                "acao": lambda: self.personagem.mover_para((253, 488),"fase_numeros") or self.personagem.set_estado("correndo_direita"),
                                "tipo": "circulo",
                            },
                            {
                                "area": (227, 390, 40),
                                "acao": lambda: self.personagem.mover_para((190, 350),"fase_fala") or self.personagem.set_estado("correndo_esquerda"),
                                "tipo": "circulo",
                            },
                            {
                                "area": (100, 313, 50),
                                "acao": lambda: self.personagem.mover_para((65, 275)) or self.personagem.set_estado("correndo_esquerda"),
                                "tipo": "circulo",
                            }
                        ]

                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["tipo"] == "retangulo":
                                x1, y1, x2, y2 = item["area"]
                                if x1 <= x <= x2 and y1 <= y <= y2:
                                    item["acao"]()  # Executa a ação associada
                                    break
                            elif item["tipo"] == "circulo":
                                # Posição e raio do círculo na superfície rolável
                                cx, cy, raio = item["area"]

                                # Compensar o deslocamento da superfície rolável
                                y_superficie = y + self.scroll_y

                                # Calcula a distância entre o clique ajustado e o centro do círculo
                                distancia = math.sqrt((x - cx) ** 2 + (y_superficie - cy) ** 2)

                                # Verifica se o clique está dentro do círculo
                                if distancia <= raio:
                                    item["acao"]()  # Executa a ação associada
                                    break

            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:  # Solta o clique esquerdo
                    self.is_scrolling = False

            if evento.type == pygame.MOUSEMOTION and self.is_scrolling:
                # Move a barra de rolagem com o mouse
                mouse_y = evento.pos[1]
                self.scrollbar_y = max(0, min(mouse_y - self.scrollbar_height // 2, ALTURA - self.scrollbar_height))
                self.scroll_y = self.scrollbar_y * (self.scrollable_height / ALTURA)

            if evento.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(0, min(self.scroll_y - evento.y * self.scroll_speed, self.scrollable_height - ALTURA))
                self.atualizar_scrollbar()

        self.todas_as_sprites.update()

    def retornar_para_kivy(self, tela_destino):
        parent_dir = os.path.dirname(self.assets_dir)
        tela_destino_file = os.path.join(parent_dir, 'tela_destino.txt')
        with open(tela_destino_file, 'w') as f:
            f.write(tela_destino)
        pygame.quit()
        sys.exit()

    def atualizar_scrollbar(self):
        self.scrollbar_y = self.scroll_y * (ALTURA / self.scrollable_height)

class Personagem(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, correndo_direita, correndo_esquerda, frame_size, scale_factor, gerenciador):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        # Animações
        self.animacoes = {
            "correndo_direita": self.carregar_frames(correndo_direita, frame_size, scale_factor),
            "correndo_esquerda": self.carregar_frames(correndo_esquerda, frame_size, scale_factor),
        }

        # Estado inicial
        self.estado = "correndo_direita"  # Estado inicial
        self.sprites = self.animacoes[self.estado]
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = (75, 720)  # Posição inicial
        self.animar = False
        self.velocidade = 2

        # Referência ao gerenciador
        self.gerenciador = gerenciador
        self.fase_destino = None  # Nova variável para armazenar a fase de destino

    def carregar_frames(self, frame_positions, frame_size, scale_factor):
        frames = []
        for pos in frame_positions:
            x, y = pos
            frame = pygame.Surface(frame_size, pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (x, y, *frame_size))
            frame = pygame.transform.scale(frame, (int(frame_size[0] * scale_factor), int(frame_size[1] * scale_factor)))
            frames.append(frame)
        return frames

    def set_estado(self, estado):
        if estado in self.animacoes and estado != self.estado:
            self.estado = estado
            self.sprites = self.animacoes[estado]
            self.atual = 0

    def mover_para(self, destino, fase_destino):
        self.destino = destino
        self.fase_destino = fase_destino  # Define a fase de destino
        self.animar = True

    def update(self):
        # Animação
        if self.animar:
            self.atual += 0.2  # Velocidade da animação
            if self.atual >= len(self.sprites):
                self.atual = 0
            self.image = self.sprites[int(self.atual)]

        # Movimento
        if hasattr(self, "destino"):
            destino_x, destino_y = self.destino
            dx = destino_x - self.rect.x
            dy = destino_y - self.rect.y
            distancia = (dx**2 + dy**2)**0.5
            if distancia > self.velocidade:
                deslocamento_x = (dx / distancia) * self.velocidade
                deslocamento_y = (dy / distancia) * self.velocidade
                self.rect.x += deslocamento_x
                self.rect.y += deslocamento_y
            else:
                # Chegou ao destino
                self.rect.topleft = self.destino
                self.animar = False
                self.atual = 0  # Volta para o primeiro frame da animação
                self.image = self.sprites[self.atual]  # Garante que o frame inicial é exibido

                # Troca para a fase de destino usando o gerenciador
                if self.fase_destino:
                    self.gerenciador.trocar_tela(self.fase_destino)
                    self.fase_destino = None  # Reseta a fase destino para evitar novas trocas


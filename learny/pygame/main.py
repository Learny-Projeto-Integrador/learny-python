import pygame
import os
import sys
import subprocess
from pygame.locals import *

pygame.init()

largura = 400
altura = 700
tela = pygame.display.set_mode((largura, altura))

pygame.display.set_caption("Learny")

# Obtendo o caminho absoluto para a pasta atual (onde o script está localizado)
base_dir = os.path.dirname(os.path.abspath(__file__))
# obtendo o caminho absoluto da pasta pai learny
parent_dir = os.path.join(base_dir, '..')

# Construindo o caminho absoluto para a fonte
montserrat_bold = os.path.join(base_dir, 'assets', 'fonts', 'montserrat', 'Montserrat-Bold.ttf')

# Carrega a fonte (tamanho 20, por exemplo)
fonte_personalizada = pygame.font.Font(montserrat_bold, 20)

# Definindo a superfície maior que a tela
scrollable_height = 1000  # Por exemplo, o dobro da altura da tela
content_surface = pygame.Surface((largura, scrollable_height))

# Variável de controle da rolagem
scroll_y = 0
scroll_speed = 10  # A velocidade da rolagem
is_scrolling = False

# Dimensões da barra de rolagem
scrollbar_width = 10
scrollbar_height = altura * (altura / scrollable_height)  # Proporcional ao conteúdo
scrollbar_x = largura - scrollbar_width
scrollbar_y = 0

# Dimensões e posição do menu inferior fixo
menu_height = 58
menu_image = pygame.image.load(os.path.join(base_dir, 'assets', 'imagens', 'retangulo-menu.png'))
menu_image = pygame.transform.scale(menu_image, (largura, menu_height))  # Redimensiona para caber no menu

# itens do menu
icone_perfil = pygame.image.load(os.path.join(base_dir, 'assets', 'icons', 'icon-perfil.png'))
icone_home = pygame.image.load(os.path.join(base_dir, 'assets', 'icons', 'icon-home.png'))
icone_menu_hamburguer = pygame.image.load(os.path.join(base_dir, 'assets', 'icons', 'icon-menu-hamburguer.png'))

# Função para salvar a tela selecionada e sair
def retornar_para_kivy(tela_destino):
    tela_destino_file = os.path.join(parent_dir, 'tela_destino.txt')
    with open(tela_destino_file, 'w') as f:
        f.write(tela_destino)  # Salva a tela de destino
    
    pygame.quit()  # Sai do Pygame  
    sys.exit()  # Sai completamente do script do Pygame

# Cor de fundo
background_color = (255, 255, 255)  # Branco
# Imagem de fundo
background_image = pygame.image.load(os.path.join(base_dir, 'assets', 'imagens', 'tela-fase.png'))

# Desenhar conteúdo na superfície maior
content_surface.fill(background_color)
content_surface.blit(background_image, (0, 0))

# Variáveis para armazenar a pontuação
pontos = 0
medalhas = 0
ranking = 10

# Renderizando a pontuação
texto_pontos = fonte_personalizada.render(str(pontos), True, (76,76,76))
texto_medalhas = fonte_personalizada.render(str(medalhas), True, (76,76,76))
texto_ranking = fonte_personalizada.render(str(ranking), True, (76,76,76))

# Colocando a pontuação na tela
content_surface.blit(texto_ranking, (315,89))
content_surface.blit(texto_pontos, (85,90))
content_surface.blit(texto_medalhas, (200,90))

class Personagem(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frame_positions, frame_size, scale_factor):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        # Carrega o sprite sheet
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        # Extrai os frames do sprite sheet
        for pos in frame_positions:
            x, y = pos
            frame = pygame.Surface(frame_size, pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), (x, y, *frame_size))
            frame = pygame.transform.scale(frame, (int(frame_size[0] * scale_factor), int(frame_size[1] * scale_factor)))
            self.sprites.append(frame)

        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = (75, 720)  # Posição inicial

        self.animar = False
        self.movendo = False
        self.velocidade = 2  # Velocidade do movimento
        self.destino = self.rect.topleft  # Ponto final do movimento

    def mover_para(self, destino):
        self.destino = destino
        self.movendo = True
        self.animar = True  # Ativa a animação enquanto o personagem se move

    def update(self):
        if self.animar:
            self.atual += 0.2  # Velocidade da animação
            if self.atual >= len(self.sprites):
                self.atual = 0
            self.image = self.sprites[int(self.atual)]

        if self.movendo:
            # Calcula a direção do movimento usando vetores normalizados
            destino_x, destino_y = self.destino
            dx = destino_x - self.rect.x
            dy = destino_y - self.rect.y
            distancia = (dx**2 + dy**2)**0.5  # Distância total até o destino

            if distancia > self.velocidade:
                # Calcula o deslocamento proporcional em cada eixo
                deslocamento_x = (dx / distancia) * self.velocidade
                deslocamento_y = (dy / distancia) * self.velocidade
                self.rect.x += deslocamento_x
                self.rect.y += deslocamento_y
            else:
                # Chegou ao destino
                self.rect.topleft = self.destino
                self.movendo = False
                self.animar = False


# Configurações do sprite sheet e animação
sprite_sheet_path = os.path.join(base_dir, 'assets', 'sprites', 'george.png')
frame_positions = [(144, 0), (144, 48), (144, 96), (144, 144)]  # Posições dos frames no sprite sheet
frame_size = (48, 48)  # Tamanho de cada frame
scale_factor = 1.5  # Escala para o tamanho do sprite

# Cria o personagem
todas_as_sprites = pygame.sprite.Group()
personagem = Personagem(sprite_sheet_path, frame_positions, frame_size, scale_factor)
todas_as_sprites.add(personagem)

# Loop principal
relogio = pygame.time.Clock()

# Função para atualizar a posição da barra de rolagem
def update_scrollbar():
    global scrollbar_y
    scrollbar_y = scroll_y * (altura / scrollable_height)

while True:
    relogio.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        # Detecta o movimento do mouse sobre a barra de rolagem
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                # Detecta clique sobre a barra de rolagem
                if scrollbar_x <= event.pos[0] <= scrollbar_x + scrollbar_width and scrollbar_y <= event.pos[1] <= scrollbar_y + scrollbar_height:
                    is_scrolling = True
                else:
                    # Detecta clique nos ícones
                    x, y = event.pos
                    menu_y = altura - menu_height  # Posição base do menu

                    if 50 <= x <= 50 + icone_perfil.get_width() and menu_y - 30 <= y <= menu_y - 30 + icone_perfil.get_height():  # Ícone de perfil
                        retornar_para_kivy('TelaPerfil')
                    elif 170 <= x <= 170 + icone_home.get_width() and menu_y - 40 <= y <= menu_y - 40 + icone_home.get_height():  # Ícone de home
                        retornar_para_kivy('TelaHome')
                    elif 300 <= x <= 300 + icone_menu_hamburguer.get_width() and menu_y - 30 <= y <= menu_y - 30 + icone_menu_hamburguer.get_height():  # Ícone do menu
                        retornar_para_kivy('TelaAtalhos')

        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Solta o clique esquerdo
                is_scrolling = False
        
        if event.type == pygame.MOUSEMOTION and is_scrolling:
            # Mover a barra de rolagem com o mouse
            mouse_y = event.pos[1]
            scrollbar_y = max(0, min(mouse_y - scrollbar_height // 2, altura - scrollbar_height))
            scroll_y = scrollbar_y * (scrollable_height / altura)

        # Detecta o movimento da roda do mouse
        if event.type == pygame.MOUSEWHEEL:
            scroll_y = max(0, min(scroll_y - event.y * scroll_speed, scrollable_height - altura))
            update_scrollbar()
        
        if event.type == KEYDOWN:
            personagem.mover_para((190, 635))

    # Preencher o fundo da tela com a cor branca
    tela.fill(background_color)

    # Desenhar a parte visível da superfície
    tela.blit(content_surface, (0, -scroll_y))

    # Desenhar a barra de rolagem
    pygame.draw.rect(tela, (150, 150, 150), (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))

    # Desenhar o menu fixo na parte inferior
    tela.blit(menu_image, (0, altura - menu_height - 20))  # Desenha a imagem do menu na parte inferior

    # Desenhar os icones do menu
    tela.blit(icone_perfil, (50, altura - menu_height - 30))  # Desenha a imagem do menu na parte inferior
    tela.blit(icone_home, (170, altura - menu_height - 40))  # Desenha a imagem do menu na parte inferior
    tela.blit(icone_menu_hamburguer, (300, altura - menu_height - 30))  # Desenha a imagem do menu na parte inferior

    # Antes de redesenhar o personagem, limpe sua área com transparência
    content_surface.fill((255, 255, 255, 0), personagem.rect)

    # Redesenha o fundo para garantir que ele permanece visível
    content_surface.blit(background_image, (0, 0))

    # Atualiza o personagem
    todas_as_sprites.update()
    todas_as_sprites.draw(content_surface)


    # Atualizar a tela
    pygame.display.flip()
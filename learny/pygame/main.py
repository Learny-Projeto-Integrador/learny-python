import pygame
from gerenciador_telas import GerenciadorTelas
from telas.tela_inicial import TelaInicial
from telas.fase_numeros import FaseNumeros
from telas.conclusao_fase import ConclusaoFase

def main():
    pygame.init()
    tela_principal = pygame.display.set_mode((400, 700))
    pygame.display.set_caption("Learny")
    clock = pygame.time.Clock()

    # Inicializa o gerenciador de telas
    gerenciador = GerenciadorTelas()

    # Registra as telas
    gerenciador.registrar_tela("tela_inicial", TelaInicial(gerenciador))
    gerenciador.registrar_tela("fase_numeros", FaseNumeros(gerenciador))
    gerenciador.registrar_tela("conclusao_fase", ConclusaoFase(gerenciador))

    # Define a tela inicial
    gerenciador.trocar_tela("tela_inicial")

    # Loop principal do jogo
    rodando = True
    while rodando:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False

        # Atualiza a lógica da tela atual
        gerenciador.atualizar(eventos)

        # Desenha a tela atual
        gerenciador.desenhar(tela_principal)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
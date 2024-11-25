import pygame
import sys
from gerenciador_telas import GerenciadorTelas
from telas.tela_inicial import TelaInicial
from telas.fase_numeros import FaseNumeros
from telas.fase_observacao import FaseObservacao
from telas.fase_fala import FaseFala
from telas.conclusao_fase import ConclusaoFase
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Função para conectar ao MongoDB local
def create_local_connection():
    try:
        # Conectar ao servidor MongoDB local na porta padrão (27017)
        client = MongoClient('mongodb://localhost:27017/')
        
        # Nome do banco de dados
        db = client['learny-bd']
        
        return client, db  # Retornar também o client para poder fechar depois
        
    except PyMongoError as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None, None

# Função para fechar a conexão
def close_connection(client):
    if client:
        client.close()
    else:
        print("Nenhuma conexão ativa para fechar.")


def main():
    pygame.init()
    tela_principal = pygame.display.set_mode((400, 700))
    pygame.display.set_caption("Learny")
    clock = pygame.time.Clock()

    # Verifica se um argumento foi passado
    if len(sys.argv) > 1:
        usuario_ativo = sys.argv[1]  # Primeiro argumento após o script
    else:
        usuario_ativo = None

    # Inicializa o gerenciador de telas
    gerenciador = GerenciadorTelas()

    # Registra as telas
    gerenciador.registrar_tela("tela_inicial", TelaInicial(gerenciador, create_local_connection, close_connection, usuario_ativo))
    gerenciador.registrar_tela("fase_numeros", FaseNumeros(gerenciador, create_local_connection, close_connection, usuario_ativo))
    gerenciador.registrar_tela("fase_observacao", FaseObservacao(gerenciador, create_local_connection, close_connection, usuario_ativo))
    gerenciador.registrar_tela("fase_fala", FaseFala(gerenciador, create_local_connection, close_connection, usuario_ativo))
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
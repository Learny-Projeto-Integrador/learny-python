import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class FaseNumeros:
    def __init__(self, gerenciador, create_connection, close_connection, usuario_ativo):
        self.gerenciador = gerenciador
        self.create_connection = create_connection
        self.close_connection = close_connection
        self.usuario_ativo = usuario_ativo
        self.audio = None
        # Inicialize o atributo no construtor da classe (init)
        self.mostrar_painel30 = True
        self.medalha_ativa = None
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
        self.icon_dica_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-dica2.png')
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
    icon_dica = None

    def receber_dados(self, dados):
        self.audio = dados[0]
        self.medalha_ativa = dados[1]

    def desenhar(self, tela):
        if self.tempo_inicio_tela is None:  # Só define no início
            self.tempo_inicio_tela = pygame.time.get_ticks()
        
        tela.blit(self.background_image, (0, 0))  # Redesenhar a imagem de fundo
        self.painel5_esquerda = tela.blit(self.painel_n5_image, (60, 287))
        self.painel5_direita = tela.blit(self.painel_n5_image, (250, 287)) 
        self.painel10 = tela.blit(self.painel_n10_image, (35, 560))
        self.painel20 = tela.blit(self.painel_n20_image, (147, 560))
        if self.mostrar_painel30:
            self.painel30 = tela.blit(self.painel_n30_image, (260, 560))
        
        self.icon_dica = tela.blit(self.icon_dica_image, (325, 497))

        # Atualizar a tela
        pygame.display.flip()

    # Função para inserir pontuação
    def inserir_pontuacao(self, pontos_fase):
        client, db = self.create_connection()  # Obter conexão existente
        
        try:
            if db is not None:
                # Buscando a coleção de usuários (no caso, a coleção "criancas")
                criancas = db["criancas"]
                
                self.caminho_imagem = 'assets/imagens/btn-atividade-amarelo.png'
                self.caminho_icone = 'assets/imagens/notificacao-atividade-amarela.png'

                self.notificacao = {
                    'nome': 'Atividade Concluída',
                    'imgNotificacao': self.caminho_imagem,
                    'mensagem': "Concluiu a fase de números",
                    'icone': self.caminho_icone,
                }

                # Buscar o usuário na coleção pelo nome de usuário
                crianca_ativa = criancas.find_one({"usuario": self.usuario_ativo})

                if crianca_ativa:
                    missoes = crianca_ativa["missoesDiarias"]
                    missao_encontrada = any(
                        missao["nome"] == "Conclua a fase de números" for missao in missoes
                    )

                    if crianca_ativa["medalhaAtiva"] == "Iniciando!":
                        pontos_fase = pontos_fase + 50
                    elif crianca_ativa["medalhaAtiva"] == "A todo o vapor!":
                        pontos_fase = pontos_fase * 2
                    
                    # Base da atualização
                    atualizacao = {
                        "$set": {
                            "pontos": crianca_ativa["pontos"] + pontos_fase,
                            "fasesConcluidas": crianca_ativa["fasesConcluidas"] + 1,
                            "faseAtual": 2,
                        },
                        "$push": {
                            "notificacoes": self.notificacao,  # Adiciona apenas um item
                        },
                    }

                    # Adicionar exclusão da missão, se encontrada
                    if missao_encontrada:
                        atualizacao["$pull"] = {"missoesDiarias": {"nome": "Conclua a fase de números"}}
                    
                    # Verifica o progresso do primeiro mundo
                    progresso_primeiro_mundo = crianca_ativa["progressoMundos"][0].get("mundo1", 0)  # Pega o progresso ou 0, se não existir

                    if progresso_primeiro_mundo <= 100:
                        progresso_atualizado = progresso_primeiro_mundo + 25
                        # Garante que o progresso não ultrapasse 100
                        progresso_atualizado = min(progresso_atualizado, 100)
                        
                        # Atualiza o progresso no banco
                        atualizacao["$set"]["progressoMundos.0.mundo1"] = progresso_atualizado

                    # Aplicar a atualização no banco
                    criancas.update_one({"_id": crianca_ativa["_id"]}, atualizacao)

                    return pontos_fase
                    
                else:
                    print(f"Usuário '{self.usuario_ativo}' não encontrado na coleção 'criancas'.")
            else:
                print("Erro ao acessar o banco de dados.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            
        finally:
            self.close_connection(client)

    def atualizar_ranking(self):
        client, db = self.create_connection()  # Obter conexão existente

        try:
            if db is not None:
                criancas = db["criancas"]
                ranking = db["ranking"]

                ranking_atualizado = []

                # Ordenando as crianças por pontos em ordem decrescente
                top_criancas = list(criancas.find().sort("pontos", -1))

                # Atualizando o ranking atual das crianças e criando o ranking atualizado
                for i, crianca in enumerate(top_criancas):
                    # Atualiza o rankAtual de todas as crianças na coleção "criancas"
                    criancas.update_one({"_id": crianca["_id"]}, {"$set": {"rankAtual": i + 1}})
                    
                    # Adiciona apenas as 7 primeiras ao ranking atualizado
                    if i < 7:  # Corrigido para limitar a 7 crianças
                        crianca_ranking = {"foto": crianca["foto"], "nome": crianca["nome"], "pontos": crianca["pontos"]}
                        ranking_atualizado.append(crianca_ranking)

                # Substituir todo o conteúdo da coleção "ranking" pelo novo ranking
                ranking.delete_many({})  # Remove todos os documentos existentes
                if ranking_atualizado:
                    ranking.insert_many(ranking_atualizado)  # Insere os novos dados

            else:
                print("Erro na conexão com o banco de dados.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

        finally:
            self.close_connection(client)

    def trocar_tela(self, num_painel):
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - self.tempo_inicio_tela) / 1000  # Em segundos
        
        # Formata o tempo para MM:SS
        minutos, segundos = divmod(int(tempo_decorrido), 60)
        tempo_formatado = f"{minutos:02}:{segundos:02}"

        pontos_fase = 0
        porcentagem_acertos = "0%"
        
        if num_painel == 10:
            pontos_fase = 100
            porcentagem_acertos = "100%"
            if self.audio == "ativado":
                self.audio_n10.play()   
        elif num_painel == 20 and self.audio == "ativado":
            self.audio_n20.play() 
        elif num_painel == 30 and self.audio == "ativado":
            self.audio_n30.play() 

        pontos_atualizados = self.inserir_pontuacao(pontos_fase)
        self.atualizar_ranking()
        
        self.gerenciador.trocar_tela("conclusao_fase", [tempo_formatado, pontos_atualizados, porcentagem_acertos])

        self.tempo_inicio_tela = None
        
    def ativar_dica(self):
        if self.medalha_ativa == "Mundo Concluído!":
            self.mostrar_painel30 = False  # Desative a exibição do painel 30

    def tocar_audio(self):
        if self.audio == "ativado":
            self.audio_n5.play()
            

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
                            {"area": self.painel5_esquerda, "acao": lambda: self.tocar_audio()},
                            {"area": self.painel5_direita, "acao": lambda: self.tocar_audio()},
                            {"area": self.painel10, "acao": lambda: self.trocar_tela(10)},
                            {"area": self.painel20, "acao": lambda: self.trocar_tela(20)},
                            {"area": self.painel30, "acao": lambda: self.trocar_tela(30)},
                            {"area": self.icon_dica, "acao": lambda: self.ativar_dica()},
                        ]

                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                item["acao"]()  # Executa a ação associada
                                break


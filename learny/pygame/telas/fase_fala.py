import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class FaseFala:
    def __init__(self, gerenciador, create_connection, close_connection, usuario_ativo):
        self.gerenciador = gerenciador
        self.create_connection = create_connection
        self.close_connection = close_connection
        self.usuario_ativo = usuario_ativo
        self.mostrar_painel_read = True
        self.medalha_ativa = None
        self.audio = None
        self.tempo_inicio_tela = None  # Armazena o tempo de início da tela

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-fase-fala.png')
        )
        self.painel_red_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-red.png')
        )
        self.painel_red_selecionado_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-red-selecionado.png')
        )
        self.painel_head_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-head.png')
        )
        self.painel_head_selecionado_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-head-selecionado.png')
        )
        self.painel_heard_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-heard.png')
        )
        self.painel_heard_selecionado_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-heard-selecionado.png')
        )
        self.painel_read_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-read.png')
        )
        self.painel_read_selecionado_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'painel-read-selecionado.png')
        )
        self.icon_audio_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icone-audio.png')
        )
        self.icon_confirmar_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icone-confirmar-vermelho.png')
        )
        self.icon_dica_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-dica2.png')
        )
        self.audio_red = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'red.wav')
        )

        self.estados_paineis = {
            "red": False,
            "head": False,
            "heard": False,
            "read": False
        }
        
    icon_audio = None
    icon_confirmar = None
    painel_red = None
    painel_head = None
    painel_heard = None

    def receber_dados(self, dados):
        self.audio = dados[0]
        self.medalha_ativa = dados[1]

    def desenhar(self, tela):
        if self.tempo_inicio_tela is None:  # Só define no início
            self.tempo_inicio_tela = pygame.time.get_ticks()
        
        tela.blit(self.background_image, (0, 0))
        
        self.icon_audio = tela.blit(self.icon_audio_image, (45, 290))

        painel_red_img = self.painel_red_selecionado_image if self.estados_paineis["red"] else self.painel_red_image
        painel_head_img = self.painel_head_selecionado_image if self.estados_paineis["head"] else self.painel_head_image
        painel_heard_img = self.painel_heard_selecionado_image if self.estados_paineis["heard"] else self.painel_heard_image
        painel_read_img = self.painel_read_selecionado_image if self.estados_paineis["read"] else self.painel_read_image
    
        self.painel_red = tela.blit(painel_red_img, (50, 435)) 
        self.painel_head = tela.blit(painel_head_img, (208, 435))
        self.painel_heard = tela.blit(painel_heard_img, (50, 520))
        if self.mostrar_painel_read:
            self.painel_read = tela.blit(painel_read_img, (208, 520))
        
        self.icon_confirmar = tela.blit(self.icon_confirmar_image, (180, 630))
        self.icon_dica = tela.blit(self.icon_dica_image, (135, 635))

        # Atualizar a tela
        pygame.display.flip()

    # Função para inserir pontuação
    def inserir_pontuacao(self, pontos_fase):
        client, db = self.create_connection()  # Obter conexão existente
        
        try:
            if db is not None:
                # Buscando a coleção de usuários (no caso, a coleção "criancas")
                criancas = db["criancas"]
                
                self.caminho_imagem = 'assets/imagens/btn-atividade-vermelho.png'

                self.notificacao = {
                    'nome': 'Atividade Concluída',
                    'imgNotificacao': self.caminho_imagem,
                }

                # Buscar o usuário na coleção pelo nome de usuário
                crianca_ativa = criancas.find_one({"usuario": self.usuario_ativo})

                if crianca_ativa:
                    missoes = crianca_ativa["missoesDiarias"]
                    missao_encontrada = any(
                        missao["nome"] == "Conclua a fase de escuta" for missao in missoes
                    )
                    
                    print(pontos_fase)
                    print(crianca_ativa["pontos"] + pontos_fase)
                    # Base da atualização
                    atualizacao = {
                        "$set": {
                            "pontos": crianca_ativa["pontos"] + pontos_fase,
                            "fasesConcluidas": crianca_ativa["fasesConcluidas"] + 1,
                            "faseAtual": 3,
                        },
                        "$push": {
                            "notificacoes": self.notificacao,  # Adiciona apenas um item
                        },
                    }

                    # Adicionar exclusão da missão, se encontrada
                    if missao_encontrada:
                        atualizacao["$pull"] = {"missoesDiarias": {"nome": "Conclua a fase de escuta"}}
                    
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

    def trocar_tela(self):
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - self.tempo_inicio_tela) / 1000  # Em segundos
        
        # Formata o tempo para MM:SS
        minutos, segundos = divmod(int(tempo_decorrido), 60)
        tempo_formatado = f"{minutos:02}:{segundos:02}"
        
        pontos_fase = 0
        porcentagem_acertos = "0%"
        
        if self.estados_paineis["red"]:
            pontos_fase = 100
            porcentagem_acertos = "100%" 
            
        self.inserir_pontuacao(pontos_fase)
        self.atualizar_ranking()
        
        self.gerenciador.trocar_tela("conclusao_fase", [tempo_formatado, pontos_fase, porcentagem_acertos])

        self.tempo_inicio_tela = None
        
    def ativar_painel(self, painel): 
        for i in self.estados_paineis:
            if i == painel:
                self.estados_paineis[i] = True  # Atribuição correta
            else:
                self.estados_paineis[i] = False  # Atribuição correta

    def tocar_audio(self):
        if self.audio:
            self.audio_red.play()
            
    def ativar_dica(self):
        #if self.medalha_ativa == "Mundo Concluído!":
        self.mostrar_painel_read = False  # Desative a exibição do painel 30

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
                            {"area": self.icon_audio, "acao": lambda: self.tocar_audio()},
                            {"area": self.painel_red, "acao": lambda: self.ativar_painel("red")},
                            {"area": self.painel_head, "acao": lambda: self.ativar_painel("head")},
                            {"area": self.painel_heard, "acao": lambda: self.ativar_painel("heard")},
                            {"area": self.painel_read, "acao": lambda: self.ativar_painel("read")},
                            {"area": self.icon_confirmar, "acao": lambda: self.trocar_tela()},
                            {"area": self.icon_dica, "acao": lambda: self.ativar_dica()}
                        ]


                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                item["acao"]()  # Executa a ação associada
                                break


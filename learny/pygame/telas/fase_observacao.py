import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class FaseObservacao:
    def __init__(self, gerenciador, create_connection, close_connection, usuario_ativo):
        self.gerenciador = gerenciador
        self.create_connection = create_connection
        self.close_connection = close_connection
        self.usuario_ativo = usuario_ativo
        self.audio = None
        self.tempo_inicio_tela = None  # Armazena o tempo de início da tela

        # Configurações de assets
        self.assets_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-fase-observacao.png')
        )
        self.painel_jacare_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'jacare-apagado.png')
        )
        self.painel_jacare_aceso_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'jacare-aceso.png')
        )
        self.painel_macaco_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'macaco-apagado.png')
        )
        self.painel_macaco_aceso_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'macaco-aceso.png')
        )
        self.painel_formiga_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'formiga-apagada.png')
        )
        self.painel_formiga_acesa_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'formiga-acesa.png')
        )
        self.painel_alpaca_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'alpaca-apagada.png')
        )
        self.painel_alpaca_acesa_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'alpaca-acesa.png')
        )
        self.icon_confirmar_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icone-confirmar-vermelho.png')
        )
        self.audio_jacare = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'alligator.wav')
        )
        self.audio_macaco = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'ape.wav')
        )
        self.audio_formiga = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'ant.wav')
        )
        self.audio_alpaca = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'alpaca.wav')
        )
        
        self.estados_paineis = {
            "jacare": False,
            "macaco": False,
            "formiga": False,
            "alpaca": False
        }

    icon_confirmar = None
    painel_jacare = None
    painel_macaco = None
    painel_formiga = None
    painel_alpaca = None

    def receber_dados(self, dados):
        self.audio = dados[0]

    def desenhar(self, tela):
        if self.tempo_inicio_tela is None:  # Só define no início
            self.tempo_inicio_tela = pygame.time.get_ticks()
        
        tela.blit(self.background_image, (0, 0))
        
        painel_jacare_img = self.painel_jacare_aceso_image if self.estados_paineis["jacare"] else self.painel_jacare_image
        painel_macaco_img = self.painel_macaco_aceso_image if self.estados_paineis["macaco"] else self.painel_macaco_image
        painel_formiga_img = self.painel_formiga_acesa_image if self.estados_paineis["formiga"] else self.painel_formiga_image
        painel_alpaca_img = self.painel_alpaca_acesa_image if self.estados_paineis["alpaca"] else self.painel_alpaca_image
    
    
        self.painel_jacare = tela.blit(painel_jacare_img, (35, 365)) 
        self.painel_macaco = tela.blit(painel_macaco_img, (223, 365))
        self.painel_formiga = tela.blit(painel_formiga_img, (35, 520))
        self.painel_alpaca = tela.blit(painel_alpaca_img, (223, 520))
        
        self.icon_confirmar = tela.blit(self.icon_confirmar_image, (180, 640))

        # Atualizar a tela
        pygame.display.flip()

    # Função para inserir pontuação
    def inserir_pontuacao(self, pontos_fase):
        client, db = self.create_connection()  # Obter conexão existente

        try:
            if db is not None:
                # Buscando a coleção de usuários (no caso, a coleção "criancas")
                criancas = db["criancas"]
                medalhas = db["medalhas"]

                medalha_iniciando = medalhas.find_one({"nome": "Iniciando!"})

                self.caminho_imagem = 'assets/imagens/btn-atividade-verde.png'
                self.caminho_imagem2 = 'assets/imagens/btn-conquista.png'

                self.notificacao = {
                    'nome': 'Atividade Concluída',
                    'imgNotificacao': self.caminho_imagem,
                }

                # Buscar o usuário na coleção pelo nome de usuário
                crianca_ativa = criancas.find_one({"usuario": self.usuario_ativo})

                if crianca_ativa:
                    missoes = crianca_ativa["missoesDiarias"]
                    missao_encontrada = any(
                        missao["nome"] == "Conclua a fase de observação" for missao in missoes
                    )
                    self.notificacao = [
                        {
                            'nome': 'Atividade Concluída',
                            'imgNotificacao': self.caminho_imagem,
                        },
                        {
                            'nome': 'Conquista Desbloqueada',
                            'imgNotificacao': self.caminho_imagem2,
                        }
                    ]

                    # Verifica se a medalha já existe na lista
                    medalha_existe = any(
                        medalha.get("nome") == medalha_iniciando["nome"] for medalha in crianca_ativa["medalhas"]
                    )

                    # Base da atualização
                    atualizacao = {
                        "$set": {
                            "pontos": crianca_ativa["pontos"] + pontos_fase,
                            "fasesConcluidas": crianca_ativa["fasesConcluidas"] + 1,
                            "faseAtual": 1,
                        },
                        "$push": {
                            "notificacoes": {
                                "$each": self.notificacao  # Adiciona todos os itens da lista
                            },
                        },
                    }

                    if len(crianca_ativa["medalhas"]) == 0:
                        atualizacao["$set"]["medalhaAtiva"] = medalha_iniciando["nome"]

                    # Adiciona a medalha apenas se ela ainda não existir
                    if not medalha_existe:
                        atualizacao["$push"]["medalhas"] = medalha_iniciando

                    # Adicionar exclusão da missão, se encontrada
                    if missao_encontrada:
                        atualizacao["$pull"] = {"missoesDiarias": {"nome": "Conclua a fase de observação"}}
                    
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
        
        pontos_fase = 100
        self.inserir_pontuacao(pontos_fase)
        self.atualizar_ranking()
        
        self.gerenciador.trocar_tela("conclusao_fase", [tempo_formatado, pontos_fase])

        self.tempo_inicio_tela = None
        
    def ativar_painel(self, painel, audio):
        self.estados_paineis[painel] = True  # Marca o painel como ativado (colorido)

        if self.audio == "ativado":
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
                            {"area": self.painel_jacare, "acao": lambda: self.ativar_painel("jacare", self.audio_jacare)},
                            {"area": self.painel_macaco, "acao": lambda: self.ativar_painel("macaco", self.audio_macaco)},
                            {"area": self.painel_formiga, "acao": lambda: self.ativar_painel("formiga", self.audio_formiga)},
                            {"area": self.painel_alpaca, "acao": lambda: self.ativar_painel("alpaca", self.audio_alpaca)},
                            {"area": self.icon_confirmar, "acao": self.trocar_tela}
                        ]


                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                item["acao"]()  # Executa a ação associada
                                break


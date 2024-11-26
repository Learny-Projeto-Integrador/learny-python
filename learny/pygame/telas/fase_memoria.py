import pygame
import os
from pygame.locals import *

# Configurações gerais
LARGURA = 400
ALTURA = 700

class FaseMemoria:
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
            os.path.join(self.assets_dir, 'assets', 'imagens', 'tela-fase-memoria.png')
        )
        self.card_vermelho_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-vermelho.png')
        )
        self.card_verde_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-verde.png')
        )
        self.card_amarelo_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-amarelo.png')
        )
        self.card_azul_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-azul.png')
        )
        self.card_macaco_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-macaco.png')
        )
        self.card_macaco_texto_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-macaco-texto.png')
        )
        self.card_macaco_figura_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-macaco-figura.png')
        )
        self.card_passaro_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-passaro.png')
        )
        self.card_passaro_texto_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-passaro-texto.png')
        )
        self.card_passaro_figura_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-passaro-figura.png')
        )
        self.card_cobra_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-cobra.png')
        )
        self.card_cobra_texto_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-cobra-texto.png')
        )
        self.card_cobra_figura_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'imagens', 'card-cobra-figura.png')
        )
        self.audio_macaco = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'monkey.wav')
        )
        self.audio_passaro = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'bird.wav')
        )
        self.audio_cobra = pygame.mixer.Sound(
            os.path.join(self.assets_dir, 'assets', 'audios', 'snake.wav')
        )
        
        self.estados_paineis = {
            "vermelho": False,
            "vermelho2": False,
            "verde": False,
            "amarelo": False,
            "amarelo2": False,
            "azul": False
        }
        self.cartas_ativas = []  # Lista para rastrear as duas últimas cartas viradas
        self.pares_travados = set()  # Armazena os pares já travados

    def verificar_par(self):
        """Verifica se as duas cartas viradas são um par."""
        if len(self.cartas_ativas) == 2:
            carta1, carta2 = self.cartas_ativas
            # Verifica se as duas cartas são do mesmo tipo (pares)
            pares_correspondentes = [
                ("vermelho", "amarelo"),
                ("amarelo", "vermelho"),
                ("vermelho2", "azul"),
                ("azul", "vermelho2"),
                ("verde", "amarelo2"),
                ("amarelo2", "verde")
            ]

            if (carta1, carta2) in pares_correspondentes or (carta2, carta1) in pares_correspondentes:
                self.pares_travados.add(carta1)
                self.pares_travados.add(carta2)
            else:
                # Adiciona as cartas para serem desviradas
                self.cartas_para_desvirar = [carta1, carta2]
                pygame.time.set_timer(pygame.USEREVENT, 1000)  # Configura o atraso de 1 segundo

            self.cartas_ativas = []  # Limpa as cartas ativas

            # Verifica se todas as cartas estão travadas
            if len(self.pares_travados) == len(self.estados_paineis):
                self.trocar_tela()

    def receber_dados(self, dados):
        self.audio = dados

    def desenhar(self, tela):
        if self.tempo_inicio_tela is None:  # Só define no início
            self.tempo_inicio_tela = pygame.time.get_ticks()
        
        tela.blit(self.background_image, (0, 0))
        
        if self.audio == "ativado":
            card_vermelho_img = self.card_macaco_figura_image if self.estados_paineis["vermelho"] else self.card_vermelho_image
            card_vermelho2_img = self.card_passaro_figura_image if self.estados_paineis["vermelho2"] else self.card_vermelho_image
            card_verde_img = self.card_cobra_figura_image if self.estados_paineis["verde"] else self.card_verde_image
            card_amarelo_img = self.card_macaco_texto_image if self.estados_paineis["amarelo"] else self.card_amarelo_image
            card_amarelo2_img = self.card_cobra_texto_image if self.estados_paineis["amarelo2"] else self.card_amarelo_image
            card_azul_img = self.card_passaro_texto_image if self.estados_paineis["azul"] else self.card_azul_image
        else:
            card_vermelho_img = self.card_macaco_image if self.estados_paineis["vermelho"] else self.card_vermelho_image
            card_vermelho2_img = self.card_passaro_image if self.estados_paineis["vermelho2"] else self.card_vermelho_image
            card_verde_img = self.card_cobra_image if self.estados_paineis["verde"] else self.card_verde_image
            card_amarelo_img = self.card_macaco_image if self.estados_paineis["amarelo"] else self.card_amarelo_image
            card_amarelo2_img = self.card_cobra_image if self.estados_paineis["amarelo2"] else self.card_amarelo_image
            card_azul_img = self.card_passaro_image if self.estados_paineis["azul"] else self.card_azul_image
        
        self.card_amarelo = tela.blit(card_amarelo_img, (65, 270))
        self.card_verde = tela.blit(card_verde_img, (65, 405)) 
        self.card_vermelho = tela.blit(card_vermelho_img, (65, 540))
        self.card_vermelho2 = tela.blit(card_vermelho2_img, (220, 270))
        self.card_azul = tela.blit(card_azul_img, (220, 405)) 
        self.card_amarelo2 = tela.blit(card_amarelo2_img, (220, 540))

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
                            "faseAtual": 4,
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
                        progresso_atualizado = progresso_primeiro_mundo + 20
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
        #self.inserir_pontuacao(pontos_fase)
        #self.atualizar_ranking()
        
        self.gerenciador.trocar_tela("conclusao_fase", [tempo_formatado, pontos_fase])

        self.tempo_inicio_tela = None
        
    def ativar_painel(self, painel, audio):
        """Ativa o painel clicado e verifica se há dois ativos."""
        if painel in self.pares_travados or len(self.cartas_ativas) == 2:
            return  # Ignora cliques em cartas já travadas ou se duas cartas já estão viradas

        self.estados_paineis[painel] = True
        self.cartas_ativas.append(painel)
        audio.play()  # Toca o áudio

        # Verifica se há um par formado
        self.verificar_par()

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == QUIT:
                self.running = False
                
            elif evento.type == pygame.USEREVENT:
                # Desvira as cartas armazenadas em cartas_para_desvirar
                for carta in self.cartas_para_desvirar:
                    self.estados_paineis[carta] = False
                self.cartas_para_desvirar = []  # Limpa a lista após desvirar
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Cancela o timer
            
            # Detecta clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clique esquerdo
                        # Detecta cliques nos painel dos numeros
                        x, y = evento.pos

                        # Lista de áreas clicáveis e ações associadas
                        areas_clicaveis = [
                            {"area": self.card_vermelho, "acao": lambda: self.ativar_painel("vermelho", self.audio_macaco)},
                            {"area": self.card_vermelho2, "acao": lambda: self.ativar_painel("vermelho2", self.audio_passaro)},
                            {"area": self.card_verde, "acao": lambda: self.ativar_painel("verde", self.audio_cobra)},
                            {"area": self.card_amarelo, "acao": lambda: self.ativar_painel("amarelo", self.audio_macaco)},
                            {"area": self.card_amarelo2, "acao": lambda: self.ativar_painel("amarelo2", self.audio_cobra)},
                            {"area": self.card_azul, "acao": lambda: self.ativar_painel("azul", self.audio_passaro)},
                        ]


                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                item["acao"]()  # Executa a ação associada
                                break


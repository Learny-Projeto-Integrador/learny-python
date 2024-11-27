import pygame
import os
from pygame.locals import *
import random

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
        self.icon_dica_image = pygame.image.load(
            os.path.join(self.assets_dir, 'assets', 'icons', 'icon-dica2.png')
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
                self.cartas_ativas = []  # Limpa as cartas ativas

                # Verifica se todas as cartas estão travadas
                if len(self.pares_travados) == len(self.estados_paineis):
                    # Configura o atraso de 1 segundo antes de trocar a tela
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Define um evento exclusivo para troca de tela
            else:
                # Adiciona as cartas para serem desviradas
                self.cartas_para_desvirar = [carta1, carta2]
                pygame.time.set_timer(pygame.USEREVENT, 1000)  # Configura o atraso de 1 segundo para desvirar as cartas

            self.cartas_ativas = []  # Limpa as cartas ativas


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
            card_vermelho_img = self.card_macaco_texto_image if self.estados_paineis["vermelho"] else self.card_vermelho_image
            card_vermelho2_img = self.card_passaro_texto_image if self.estados_paineis["vermelho2"] else self.card_vermelho_image
            card_verde_img = self.card_cobra_texto_image if self.estados_paineis["verde"] else self.card_verde_image
            card_amarelo_img = self.card_macaco_image if self.estados_paineis["amarelo"] else self.card_amarelo_image
            card_amarelo2_img = self.card_cobra_image if self.estados_paineis["amarelo2"] else self.card_amarelo_image
            card_azul_img = self.card_passaro_image if self.estados_paineis["azul"] else self.card_azul_image
        
        self.card_amarelo = tela.blit(card_amarelo_img, (65, 270))
        self.card_verde = tela.blit(card_verde_img, (65, 405)) 
        self.card_vermelho = tela.blit(card_vermelho_img, (65, 540))
        self.card_vermelho2 = tela.blit(card_vermelho2_img, (220, 270))
        self.card_azul = tela.blit(card_azul_img, (220, 405)) 
        self.card_amarelo2 = tela.blit(card_amarelo2_img, (220, 540))
        
        self.icon_dica = tela.blit(self.icon_dica_image, (175, 655))

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

                medalha_vapor = medalhas.find_one({"nome": "A todo o vapor!"})
                medalha_mundo = medalhas.find_one({"nome": "Mundo Concluído!"})

                self.caminho_imagem = 'assets/imagens/btn-atividade-azul.png'
                self.caminho_imagem2 = 'assets/imagens/btn-conquista-vermelha.png'
                self.caminho_imagem3 = 'assets/imagens/btn-conquista-azul.png'

                self.caminho_icone = 'assets/imagens/notificacao-atividade-azul.png'
                self.caminho_icone2 = 'assets/imagens/notificacao-medalha-vermelha.png'
                self.caminho_icone3 = 'assets/imagens/notificacao-medalha-azul.png'

                self.notificacao = {
                    'nome': 'Atividade Concluída',
                    'imgNotificacao': self.caminho_imagem,
                }

                # Buscar o usuário na coleção pelo nome de usuário
                crianca_ativa = criancas.find_one({"usuario": self.usuario_ativo})

                if crianca_ativa:
                    missoes = crianca_ativa["missoesDiarias"]
                    missao_encontrada = any(
                        missao["nome"] == "Conclua a fase de memória" for missao in missoes
                    )
                    self.notificacao = [
                        {
                            'nome': 'Atividade Concluída',
                            'imgNotificacao': self.caminho_imagem,
                            'mensagem': "Concluiu a fase de memória",
                            'icone': self.caminho_icone,
                        },
                        {
                            'nome': 'Conquista Desbloqueada',
                            'imgNotificacao': self.caminho_imagem2,
                            'mensagem': "Conseguiu a conquista a todo o vapor!",
                            'icone': self.caminho_icone2,
                        },
                        {
                            'nome': 'Conquista Desbloqueada',
                            'imgNotificacao': self.caminho_imagem3,
                            'mensagem': "Conseguiu a conquista mundo concluído!",
                            'icone': self.caminho_icone3,
                        }
                    ]

                    # Lista de medalhas que deseja verificar
                    medalhas_a_verificar = [medalha_vapor["nome"], medalha_mundo["nome"]]

                    # Verifica se alguma das medalhas já existe na lista
                    medalha_existe = any(
                        medalha.get("nome") in medalhas_a_verificar for medalha in crianca_ativa["medalhas"]
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
                            "faseAtual": 0,
                        },
                        "$push": {
                            "notificacoes": {
                                "$each": self.notificacao  # Adiciona todos os itens da lista
                            },
                        },
                    }

                    # Adicionar exclusão da missão, se encontrada
                    if missao_encontrada:
                        atualizacao["$pull"] = {"missoesDiarias": {"nome": "Conclua a fase de memória"}}
                        
                    # Adiciona as medalhas apenas se elas ainda não existirem
                    if not medalha_existe:
                        atualizacao["$push"] = {
                            "medalhas": {
                                "$each": [medalha_vapor, medalha_mundo]
                            }
                        }

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

    def trocar_tela(self):
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - self.tempo_inicio_tela) / 1000  # Em segundos
        
        # Formata o tempo para MM:SS
        minutos, segundos = divmod(int(tempo_decorrido), 60)
        tempo_formatado = f"{minutos:02}:{segundos:02}"
        
        pontos_fase = 100
        pontos_atualizados = self.inserir_pontuacao(pontos_fase)
        self.atualizar_ranking()
        
        self.gerenciador.trocar_tela("conclusao_fase", [tempo_formatado, pontos_atualizados])

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
        
    def ativar_dica(self):
        # Verifica se a medalha foi concluída e se a dica já não foi usada
        if self.medalha_ativa == "Mundo Concluído!" and not getattr(self, "dica_usada", False):
            # Lista de pares possíveis com seus áudios correspondentes
            pares_correspondentes = {
                ("vermelho", "amarelo"): self.audio_macaco,
                ("amarelo", "vermelho"): self.audio_macaco,
                ("vermelho2", "azul"): self.audio_passaro,
                ("azul", "vermelho2"): self.audio_passaro,
                ("verde", "amarelo2"): self.audio_cobra,
                ("amarelo2", "verde"): self.audio_cobra
            }

            # Identifica pares não travados
            pares_disponiveis = [
                (carta1, carta2) for carta1, carta2 in pares_correspondentes.keys()
                if carta1 not in self.pares_travados and carta2 not in self.pares_travados
            ]

            if pares_disponiveis:
                # Seleciona um par aleatório
                carta1, carta2 = random.choice(pares_disponiveis)

                # Ativa os dois painéis correspondentes
                self.estados_paineis[carta1] = True
                self.estados_paineis[carta2] = True

                # Adiciona ao conjunto de pares travados
                self.pares_travados.add(carta1)
                self.pares_travados.add(carta2)

                # Toca o áudio correspondente
                audio = pares_correspondentes.get((carta1, carta2))
                if audio:
                    audio.play()

                # Marca a dica como usada
                self.dica_usada = True



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
                
            elif evento.type == pygame.USEREVENT + 1:
                # Troca a tela após o atraso
                self.trocar_tela()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancela o timer
            
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
                            {"area": self.icon_dica, "acao": lambda: self.ativar_dica()},
                        ]


                        # Verifica em qual área o clique ocorreu
                        for item in areas_clicaveis:
                            if item["area"].collidepoint(x, y):  # Verifica se o clique foi na área
                                item["acao"]()  # Executa a ação associada
                                break


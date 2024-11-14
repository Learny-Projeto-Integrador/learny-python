# Instale as bibliotecas
# pip install pymongo | pip install kivy | pip install kivymd | pip install pygame (ainda não está sendo usado)

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.widget import Widget
from config.conexao import *
from config.conexao_local import *
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from os.path import expanduser, join
import shutil
import os
import logging

logging.getLogger('pymongo').setLevel(logging.WARNING)  # Reduz os logs de monitoramento de topologia

# Define o tamanho da janela
Window.size = (400, 700)
Window.left = 550  # Distância da janela para a esquerda da tela
Window.top = 75   # Distância da janela para o topo da tela

# Gerenciador das telas
class WindowManager(ScreenManager):
    tipo_cadastro = ""
    pass

class GradienteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preload_background()

    def preload_background(self):
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Altere para a cor desejada se precisar
            self.bg_rect = Rectangle(source='assets/imagens/fundo-gradiente.png', size=self.size)

    def on_size(self, *args):
        self.bg_rect.size = self.size  # Atualiza o tamanho do retângulo quando a tela muda

class GradienteScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preload_background()

    def preload_background(self):
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Altere para a cor desejada se precisar
            self.bg_rect = Rectangle(source='assets/imagens/fundo-gradiente2.png', size=self.size)

    def on_size(self, *args):
        self.bg_rect.size = self.size  # Atualiza o tamanho do retângulo quando a tela muda

class TelaAzul(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preload_background()

    def preload_background(self):
        with self.canvas.before:
            Color(0.42, 0.82, 1, 1)  # Altere para a cor desejada se precisar
            self.bg_rect = Rectangle(size=self.size)

    def on_size(self, *args):
        self.bg_rect.size = self.size  # Atualiza o tamanho do retângulo quando a tela muda

class TelaLogin(GradienteScreen):
    def buscar_dados_crianca(self, usuario_banco):
        # Busca os dados do usuário ativo              
        if usuario_banco:
            return {
                'usuario': usuario_banco["usuario"],
                'senha': usuario_banco["senha"],
                'nome': usuario_banco["nome"],
                'data_de_nascimento': usuario_banco["data_de_nascimento"],
                'foto': usuario_banco["foto"],
                'pai': usuario_banco["pai"],
                'pontos': usuario_banco["pontos"],
                'nivel': usuario_banco["nivel"],
                'medalhas': usuario_banco["medalhas"],
                'fasesConcluidas': usuario_banco["fasesConcluidas"],
                'conquistas': usuario_banco["conquistas"],
                'missoesDiarias': usuario_banco["missoesDiarias"],
                'notificaoes': usuario_banco["notificacoes"],
                'ranking': usuario_banco["ranking"],
                'desafios': usuario_banco["desafios"],
                'progressoMundos': usuario_banco["progressoMundos"]
            }
        return None
    
    def buscar_dados_pai(self, usuario_banco):
        # Busca os dados do usuário ativo              
        if usuario_banco:
            return {
                'id': usuario_banco["_id"],
                'usuario': usuario_banco["usuario"],
                'senha': usuario_banco["senha"],
                'nome': usuario_banco["nome"],
                'email': usuario_banco["email"],
                'foto': usuario_banco["foto"],
                'pontos': usuario_banco["pontos"],
                'nivel': usuario_banco["nivel"],
                'titulo': usuario_banco["titulo"],
                'notificacoes': usuario_banco["notificacoes"],
                'frustracaoCrianca': usuario_banco["frustracaoCrianca"]
            }
        return None
    
    # Função onclick para o botão entrar
    def on_enter_button_click(self):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção de usuários (no caso, as coleções "criancas" e "pais")
                criancas = db["criancas"]
                pais = db["pais"]
                
                # Variáveis que armazenam os valores obtidos nos campos
                usuario = self.ids.txt_usuario.text
                senha = self.ids.txt_senha.text

                # Buscar o usuário na coleção pelo nome de usuário
                usuario_banco_crianca = criancas.find_one({"usuario": usuario})
                usuario_banco_pai = pais.find_one({"usuario": usuario})

                app = MDApp.get_running_app()
                
                # Verificar se o usuário foi encontrado e se a senha está correta
                if usuario_banco_crianca and usuario_banco_crianca['senha'] == senha:
                    dados_usuario = self.buscar_dados_crianca(usuario_banco_crianca)
                    self.origem_usuario = 'crianca'  # Define a origem como 'crianca'
                    
                    if dados_usuario:
                        # Passa os dados para a MainApp
                        MDApp.get_running_app().set_dados_usuario(dados_usuario)
                        
                        # Atualiza os dados das telas antes da transição
                        tela_home = app.root.get_screen("TelaHome")
                        tela_perfil = app.root.get_screen("TelaPerfil")
                        tela_ranking = app.root.get_screen("TelaRanking")
                        
                        tela_home.atualizar_dados()
                        tela_perfil.atualizar_dados()
                        tela_ranking.atualizar_ranking()
                        
                        self.go_bem_vindo(usuario_banco_crianca["nome"])  # Trocar o nome pelo nome do usuário autenticado
                        Clock.schedule_once(self.go_home, 2)  # Aguarda 2 segundos e vai para a tela Home
                    else:
                        self.show_popup("Erro de Login", "Usuário e/ou senha inválidos!", "nao")

                elif usuario_banco_pai and usuario_banco_pai['senha'] == senha:
                    dados_usuario = self.buscar_dados_pai(usuario_banco_pai)
                    self.origem_usuario = 'pai'  # Define a origem como 'pai'
                    
                    if dados_usuario:
                        # Passa os dados para a MainApp
                        MDApp.get_running_app().set_dados_usuario(dados_usuario)
                        
                        # Atualiza os dados da tela antes da transição
                        tela_perfil_pais = app.root.get_screen("TelaPerfilPais")
                        tela_perfil_pais.atualizar_dados()
                        
                        self.go_bem_vindo(usuario_banco_pai["nome"])  # Trocar o nome pelo nome do usuário autenticado
                        Clock.schedule_once(self.go_home, 2)  # Aguarda 2 segundos e vai para a tela Home
                    else:
                        self.show_popup("Erro de Login", "Usuário e/ou senha inválidos!", "nao")
                
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao fazer login:", e)

        finally:
            close_connection(client)

    # Função para mostrar o popup
    def show_popup(self, title, message):
        self.popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        self.popup.open()

    # Função para ir para a tela de boas-vindas e mudar o nome de acordo com o usuário autenticado
    def go_bem_vindo(self, usuario):
        self.manager.get_screen('TelaBemVindo').ids.lbl_transicao.text = f"Bem-vindo, {usuario}!"
        self.manager.transition.direction = 'left'  # Define a direção para a transição entre as telas
        self.manager.current = 'TelaBemVindo'  # Muda para a tela de transição do login

    # Função para ir para a tela Home
    def go_home(self, dt):
        self.manager.transition.direction = 'left'  # Define a direção para a transição
        
        # Redireciona para uma tela diferente dependendo se é 'crianca' ou 'pai'
        if self.origem_usuario == 'crianca':
            self.manager.current = 'TelaHome'  # Tela específica para a criança
            
        elif self.origem_usuario == 'pai':
            self.manager.current = 'TelaPerfilPais'  # Tela específica para o pai

class TelaCadastroPais(GradienteScreen):
    # Define o nível de frustração que vai ser cadastrado
    nivel_frustracao = None
    id_pai_cadastro = None
    # Função para obter os nível de frustração clicados
    def check_box_click(self, checkbox, valor, nivel):
        if valor:  # Se o checkbox está ativo
            self.nivel_frustracao = nivel # muda o nível de frustração de acordo com o checkbox clicado

    # Função onclick para o botão cadastrar
    def on_register_button_click(self):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção para adicionar
                pais = db["pais"]
                criancas = db["criancas"]
                
                # Variáveis que armazenam os valores obtidos nos campos
                usuario = self.ids.txt_usuario_cadastro.text
                senha = self.ids.txt_senha_cadastro.text
                nome = self.ids.txt_nome_cadastro.text  # Novo campo de nome
                email = self.ids.txt_email_cadastro.text  # Novo campo de nome
                
                # verifica se já existe um usuário com esse nome no banco
                buscar_existente_pais = pais.find_one({"usuario": usuario})
                buscar_existente_criancas = criancas.find_one({"usuario": usuario})
                
                # Acessar a tela de seleção de imagem através do ScreenManager
                tela_selecionar_imagem = self.manager.get_screen('TelaSelecionarImagem')

                # Obter o caminho da imagem copiada
                # Obtendo caminho relativo a partir do diretório do projeto
                projeto_dir = os.path.dirname(os.path.abspath(__file__))
                caminho_imagem = None
                if tela_selecionar_imagem.destino_imagem:
                    caminho_imagem = os.path.relpath(tela_selecionar_imagem.destino_imagem, projeto_dir)
                
                if buscar_existente_pais or buscar_existente_criancas:
                    self.show_popup("Erro de Cadastro", "Nome de usuário já existente!", "nao")
                
                else:
                    # Lógica de Cadastro
                    if usuario != "" and senha != "" and nome != "" and email != "" and self.nivel_frustracao != None and caminho_imagem is not None:
                        pai = {
                            'usuario': usuario,
                            'senha': senha,
                            'nome': nome,
                            'email': email,
                            'foto': caminho_imagem,
                            'pontos': 0,
                            'nivel': 0,
                            'titulo': '',
                            'notificacoes': [],
                            'frustracaoCrianca': self.nivel_frustracao
                        }
                        resultado_insercao = pais.insert_one(pai)
                        self.id_pai_cadastro = resultado_insercao.inserted_id  # Obter o ID do pai recém-cadastrado
                        
                        # Exibir popup de sucesso
                        self.show_popup("Dados Cadastrados", "Seus dados foram cadastrados com sucesso!", "ok")
                    else:
                        # Exibir popup de erro se faltar dados
                        self.show_popup("Erro de Cadastro", "Preencha todos os campos!", "nao")
                        
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao cadastrar o pai:", e)

        finally:
            close_connection(client)


    # Função para mostrar o popup
    def show_popup(self, title, message, status):
        self.popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        # Conecta a função de transição ao evento de fechamento do popup
        if status == "ok":
            self.popup.bind(on_dismiss=self.go_filho_after_popup) # Se deu certo o cadastro ele vai para o cadastro filho ao fechar o popup
        else:
            pass
        self.popup.open()
    
    # Função para ir para o login
    def go_filho_after_popup(self, instance):
        self.manager.transition.direction = 'left'  # Define a direção para a transição
        tela_cadastro_filho = self.manager.get_screen('TelaCadastro')
        tela_cadastro_filho.id_pai = self.id_pai_cadastro  # Define o id do pai na tela do filho
        self.manager.current = 'TelaCadastro'  # Muda para a tela de cadastro dos filhos

class TelaCadastro(GradienteScreen):
    id_pai = None
    # Função onclick para o botão cadastrar
    def on_register_button_click(self):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção para adicionar
                criancas = db["criancas"]
                pais = db["pais"]
                
                # Variáveis que armazenam os valores obtidos nos campos
                usuario = self.ids.txt_usuario_cadastro.text
                senha = self.ids.txt_senha_cadastro.text
                nome = self.ids.txt_nome_cadastro.text  # Novo campo de nome
                data_nasc = self.ids.txt_data_nasc.text
                
                # verifica se já existe um usuário com esse nome no banco
                buscar_existente_criancas = criancas.find_one({"usuario": usuario})
                buscar_existente_pais = pais.find_one({"usuario": usuario})
                
                # Acessar a tela de seleção de imagem através do ScreenManager
                tela_selecionar_imagem = self.manager.get_screen('TelaSelecionarImagem')

                # Obter o caminho da imagem copiada
                # Obtendo caminho relativo a partir do diretório do projeto
                projeto_dir = os.path.dirname(os.path.abspath(__file__))
                caminho_imagem = None
                if tela_selecionar_imagem.destino_imagem:
                    caminho_imagem = os.path.relpath(tela_selecionar_imagem.destino_imagem, projeto_dir)
                
                if buscar_existente_criancas or buscar_existente_pais:
                    self.show_popup("Erro de Cadastro", "Nome de usuário já existente!", "nao")
                
                else:
                    # Lógica de Cadastro
                    if usuario != "" and senha != "" and nome != "" and data_nasc != "" and caminho_imagem is not None:
                        crianca = {
                            'usuario': usuario,
                            'senha': senha,
                            'nome': nome,
                            'data_de_nascimento': data_nasc,
                            'foto': caminho_imagem,
                            'pai': self.id_pai,
                            'pontos': 0,
                            'nivel': 0,
                            'medalhas': 0,
                            'fasesConcluidas': 0,
                            'conquistas': 0,
                            'missoesDiarias': [],
                            'notificacoes': [],
                            'ranking': 'habilitado',
                            'desafios': 'permitidos',
                            'progressoMundos': [
                                {'mundo1': 0},
                                {'mundo2': 0},
                                {'mundo3': 0},
                                {'mundo4': 0}
                            ]
                        }
                        criancas.insert_one(crianca)
                        
                        # Exibir popup de sucesso
                        self.show_popup("Dados Cadastrados", "Seus dados foram cadastrados com sucesso!", "ok")
                    else:
                        # Exibir popup de erro se faltar dados
                        self.show_popup("Erro de Cadastro", "Preencha todos os campos!", "nao")
                        
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao cadastrar a criança:", e)

        finally:
            close_connection(client)


    # Função para mostrar o popup
    def show_popup(self, title, message, status):
        self.popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        # Conecta a função de transição ao evento de fechamento do popup
        if status == "ok":
            self.popup.bind(on_dismiss=self.go_login_after_popup) # Se deu certo o cadastro ele vai para o login ao fechar o popup
        else:
            pass
        self.popup.open()
    
    # Função para ir para o login
    def go_login_after_popup(self, instance):
        self.manager.transition.direction = 'right'  # Define a direção para a transição
        self.manager.current = 'TelaLogin'  # Muda para a tela de login

class TelaSelecionarImagem(GradienteScreen, Widget):
    
    destino_imagem = None  # Variável para armazenar o caminho da imagem copiada
    
    # Função para mostrar a imagem selecionada, sem copiar
    def mostrar_imagem(self, filename):
        if filename:
            try:
                # Exibe a imagem selecionada
                self.ids.exibe_imagem.source = filename[0]
                self.ids.exibe_imagem.reload()  # Recarregar a imagem
            except Exception as e:
                print(f"Erro ao exibir a imagem: {e}")
    
    # Função para copiar a imagem selecionada
    def selected(self, filename):
        if filename:
            try:
                # Caminho do arquivo original (imagem selecionada)
                origem = filename[0]

                # Diretório do projeto
                projeto_dir = os.path.dirname(os.path.abspath(__file__))

                # Define a pasta de destino para fotos-criancas dentro do diretório do projeto
                destino_dir = os.path.join(projeto_dir, 'assets/imagens/fotos-criancas')

                # Certifique-se de que o diretório de destino existe
                if not os.path.exists(destino_dir):
                    os.makedirs(destino_dir)

                # Caminho completo do arquivo no destino
                destino = os.path.join(destino_dir, os.path.basename(origem))

                # Verificar se o arquivo já existe no destino
                if not os.path.exists(destino):
                    # Copiar o arquivo se ele ainda não foi copiado
                    shutil.copy(origem, destino)
                    print(f"Imagem copiada para: {destino}")
                else:
                    print(f"Arquivo já existe em: {destino}")

                # Armazena o caminho da imagem copiada
                self.destino_imagem = destino

                tipo_cadastro = self.manager.tipo_cadastro
                if tipo_cadastro == "criancas":
                    # Acessa a tela de cadastro
                    tela_cadastro = self.manager.get_screen('TelaCadastro')
                    # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                    tela_cadastro.ids.img_cadastro.source = self.destino_imagem
                    # Remove o texto "+" do botão
                    tela_cadastro.ids.image_button.text = ""  
                    # Mantém o botão transparente e sem imagem de fundo
                    tela_cadastro.ids.image_button.background_normal = ""  # Certifique-se de que o fundo continua transparente

                    # Volta para a TelaCadastro com a transição
                    self.manager.transition.direction = 'right'
                    self.manager.current = 'TelaCadastro'
                    
                elif tipo_cadastro == "pais":
                    # Acessa a tela de cadastro
                    tela_cadastro = self.manager.get_screen('TelaCadastroPais')
                    # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                    tela_cadastro.ids.img_cadastro.source = self.destino_imagem
                    # Remove o texto "+" do botão
                    tela_cadastro.ids.image_button.text = ""  
                    # Mantém o botão transparente e sem imagem de fundo
                    tela_cadastro.ids.image_button.background_normal = ""  # Certifique-se de que o fundo continua transparente

                    # Volta para a TelaCadastro com a transição
                    self.manager.transition.direction = 'right'
                    self.manager.current = 'TelaCadastroPais'

            except Exception as e:
                print(f"Erro ao copiar a imagem: {e}")

class TelaBemVindo(GradienteScreen):
    pass

class TelaHome(GradienteScreen):
    fator_progresso1 = 0
    fator_progresso2 = 0 
    fator_progresso3 = 0 
    fator_progresso4 = 0  
    
    def atualizar_dados(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        self.ids.lbl_pontos.text = str(dados_usuario["pontos"])
        self.ids.lbl_medalhas.text = str(dados_usuario["medalhas"])
        self.ids.lbl_ranking.text = str(dados_usuario["fasesConcluidas"])
        
        # Obtendo os valores dos mundos
        valores_mundos = [list(mundo.values())[0] for mundo in dados_usuario["progressoMundos"]]
        
        # Atauliza as labels de porcentagem
        self.ids.lbl_porc_mundo1.text = str(valores_mundos[0]) + "%"
        self.ids.lbl_porc_mundo2.text = str(valores_mundos[1]) + "%"
        self.ids.lbl_porc_mundo3.text = str(valores_mundos[2]) + "%"
        self.ids.lbl_porc_mundo4.text = str(valores_mundos[3]) + "%"
        
        # Atualiza as barras de progresso
        self.fator_progresso1 = (valores_mundos[0] / 100)
        self.fator_progresso2 = (valores_mundos[1] / 100)
        self.fator_progresso3 = (valores_mundos[2] / 100)
        self.fator_progresso4 = (valores_mundos[3] / 100)
        
class TelaPerfil(Screen):
    def atualizar_dados(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        self.ids.foto_perfil.source = dados_usuario["foto"]
        self.ids.lbl_nome_perfil.text = dados_usuario["nome"]
        self.ids.lbl_nivel.text = str(dados_usuario["nivel"])
        self.ids.lbl_pontos.text = str(dados_usuario["pontos"])
        
    def on_switch_active(self, switch, active):
        if active:
            print("O switch está ativado")
        else:
            print("O switch está desativado")
            
class TelaPerfilPais(Screen):
    id_filho = None
    def buscar_dados_crianca(self, usuario_banco):
        # Busca os dados do usuário ativo              
        if usuario_banco:
            return {
                'id': usuario_banco["_id"],
                'nome': usuario_banco["nome"],
                'foto': usuario_banco["foto"],
                'pontos': usuario_banco["pontos"],
                'nivel': usuario_banco["nivel"],
                'medalhas': usuario_banco["medalhas"],
                'fasesConcluidas': usuario_banco["fasesConcluidas"],
                'ranking': usuario_banco["ranking"],
                'conquistas': usuario_banco["conquistas"],
                'missoesDiarias': usuario_banco["missoesDiarias"],
                'progressoMundos': usuario_banco["progressoMundos"]
            }
        return None
    
    def atualizar_dados(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        id_pai = dados_usuario["id"]
        self.ids.foto_perfil_pai.source = dados_usuario["foto"]
        self.ids.lbl_nome_pai.text = dados_usuario["nome"]
        # self.ids.lbl_pontos.text = str(dados_usuario["pontos"])
        
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção para adicionar
                criancas = db["criancas"]
                
                # verifica se já existe um usuário com esse nome no banco
                buscar_filho = criancas.find_one({"pai": id_pai})
                
                if buscar_filho:
                    dados_filho = self.buscar_dados_crianca(buscar_filho)
                    self.id_filho = dados_filho["id"]
                    self.ids.img_filho.source = dados_filho["foto"]
                    self.ids.lbl_nome_filho.text = dados_filho["nome"]
                    
                    # Muda o estado do switch de acordo com a informação do banco
                    ranking = dados_filho["ranking"]
                    self.ids.switch_ranking.active = (ranking.lower() == "habilitado")
                    
                else:
                    print("Erro")
                        
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao buscar os dados da criança:", e)

        finally:
            close_connection(client)

    def atualizar_estado_ranking(self, estado):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção para adicionar
                criancas = db["criancas"]
                novo_valor = "habilitado" if estado else "desabilitado"
                criancas.update_one({"_id": self.id_filho}, {"$set": {"ranking": novo_valor}})
        
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao buscar os dados da criança:", e)

        finally:
            close_connection(client)
        
    def on_switch_active(self, instance, value):
       # Atualizar o banco de dados quando o switch for alternado
       self.atualizar_estado_ranking(value)
       
    def on_enter(self):
        # Exemplo de chamada para adicionar uma imagem ao entrar na tela
        self.adicionar_notificacao("assets/imagens/btn-conquista.png")
        self.adicionar_notificacao("assets/imagens/btn-atividade-amarelo.png")
        self.adicionar_notificacao("assets/imagens/btn-atividade-azul.png")
        '''self.adicionar_filho("assets/imagens/btn-cadastrar-filho.png")'''

    #Função para adicionar os paineis de notificação
    def adicionar_notificacao(self, image_path):
        # Adiciona o layout do item ao BoxLayout principal
        self.ids.medalhas.add_widget(FitImage(source=image_path, size_hint=(None, None), size=(358, 104)))

    #Função para adicionar os paineis de notificação
    '''def adicionar_filho(self, image_path):
        # Adiciona o layout do item ao BoxLayout principal
        self.ids.filhos.add_widget(FitImage(source=image_path, size_hint=(None, None), size=(300, 60)))'''
 
 
class TelaEditarPerfil(GradienteScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dados_carregados = False  # Variável para controlar se a foto foi carregada
        self.id_crianca = None
        self.foto = None
        
    def on_enter(self, *args):
        # Verifica se o 'usuario_ativo' está definido
        app = MDApp.get_running_app()
        usuario = app.usuario_ativo
        if usuario:
            try:
                client, db = create_local_connection()
                if db is not None:
                    criancas = db["criancas"]
                    usuario_banco = criancas.find_one({"usuario": usuario})
                    
                    # armazena os dados vindos do banco em variáveis
                    self.id_crianca = usuario_banco["_id"]
                    senha = usuario_banco["senha"]
                    nome = usuario_banco["nome"]
                    data_nasc = usuario_banco["data_de_nascimento"]
                    self.foto = usuario_banco["foto"]
                    
                    if not self.dados_carregados:
                        # Exibe a imagem do usuário ativo
                        try:
                            self.ids.img_editar_perfil.source = self.foto
                            self.ids.exibe_imagem.reload()  # Recarregar a imagem
                        except Exception as e:
                            print(f"Erro ao exibir a imagem: {e}")
                        
                        # Exibe os dados do usuário ativo
                        self.ids.txt_usuario_editar.text = usuario
                        self.ids.txt_senha_editar.text = senha
                        self.ids.txt_nome_editar.text = nome
                        self.ids.txt_data_nasc.text = data_nasc

                    # Troca para True para carregar apenas uma vez os dados
                    self.dados_carregados = True

            except PyMongoError as e:
                print("Erro ao buscar o usuário ativo:", e)
            finally:
                close_connection(client)
        else:
            print("Nenhum usuário ativo encontrado.")
            
    # Função onclick para o botão cadastrar
    def on_edit_button_click(self):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção para adicionar
                criancas = db["criancas"]
                
                # Variáveis que armazenam os valores obtidos nos campos
                usuario = self.ids.txt_usuario_editar.text
                senha = self.ids.txt_senha_editar.text
                nome = self.ids.txt_nome_editar.text  # Novo campo de nome
                data_nasc = self.ids.txt_data_nasc.text
                
                # Acessar a tela de edição de imagem através do ScreenManager
                tela_editar_foto_perfil = self.manager.get_screen('TelaEditarFotoPerfil')

                # Obter o caminho da imagem copiada
                # Obtendo caminho relativo a partir do diretório do projeto
                projeto_dir = os.path.dirname(os.path.abspath(__file__))
                caminho_imagem = None
                if tela_editar_foto_perfil.destino_imagem:
                    caminho_imagem = os.path.relpath(tela_editar_foto_perfil.destino_imagem, projeto_dir)
                if caminho_imagem == None:
                    caminho_imagem = self.foto
                
                # Lógica de Edição
                if usuario != "" and senha != "" and nome != "" and data_nasc != "" and caminho_imagem is not None:
                    crianca = {
                        'usuario': usuario,
                        'senha': senha,
                        'nome': nome,
                        'data_de_nascimento': data_nasc,
                        'foto': caminho_imagem
                    }
                    # Atualizar os dados da criança pelo ID
                    resultado = criancas.update_one(
                        {"_id": self.id_crianca},  # Filtro para encontrar a criança pelo ID
                        {"$set": crianca}     # Atualiza os campos fornecidos
                    )
                    
                    if resultado.modified_count > 0:
                        # Exibir popup de sucesso
                        self.show_popup("Dados Atualizados", "Seus dados foram atualizados com sucesso!", "ok")
                    else:
                        # Exibir popup se não houver mudanças (por exemplo, se os dados forem os mesmos)
                        self.show_popup("Sem Mudanças", "Nenhuma alteração foi feita nos dados.", "nao")
                else:
                    # Exibir popup de erro se faltar dados
                    self.show_popup("Erro de Edição", "Preencha todos os campos!", "nao")
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao atualizar a criança:", e)

        finally:
            close_connection(client)


    # Função para mostrar o popup
    def show_popup(self, title, message, status):
        self.popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        # Conecta a função de transição ao evento de fechamento do popup
        if status == "ok":
            self.popup.bind(on_dismiss=self.go_login_after_popup) # Se deu certo o cadastro ele vai para o login ao fechar o popup
        else:
            pass
        self.popup.open()
    
    # Função para ir para o login
    def go_login_after_popup(self, instance):
        self.manager.transition.direction = 'right'  # Define a direção para a transição
        self.manager.current = 'TelaLogin'  # Muda para a tela de login
    

class TelaEditarFotoPerfil(GradienteScreen):    
    def on_enter(self, *args):
        # Verifique se o `usuario_ativo` está definido
        app = MDApp.get_running_app()
        usuario = app.usuario_ativo
        if usuario:
            # Realize operações de consulta usando `usuario`
            try:
                client, db = create_local_connection()
                if db is not None:
                    criancas = db["criancas"]
                    usuario_banco = criancas.find_one({"usuario": usuario})
                    foto = usuario_banco["foto"]
                    try:
                        # Exibe a imagem do usuário ativo
                        self.ids.exibe_imagem.source = foto
                        self.ids.exibe_imagem.reload()  # Recarregar a imagem
                    except Exception as e:
                        print(f"Erro ao exibir a imagem: {e}")
                    
            except PyMongoError as e:
                print("Erro ao buscar o usuário ativo:", e)
            finally:
                close_connection(client)
        else:
            print("Nenhum usuário ativo encontrado.")
    
    destino_imagem = None  # Variável para armazenar o caminho da imagem copiada
    
    # Função para mostrar a imagem selecionada, sem copiar
    def mostrar_imagem(self, filename):
        if filename:
            try:
                # Exibe a imagem selecionada
                self.ids.exibe_imagem.source = filename[0]
                self.ids.exibe_imagem.reload()  # Recarregar a imagem
            except Exception as e:
                print(f"Erro ao exibir a imagem: {e}")
    
    # Função para copiar a imagem selecionada
    def selected(self, filename):
        if filename:
            try:
                # Caminho do arquivo original (imagem selecionada)
                origem = filename[0]

                # Diretório do projeto
                projeto_dir = os.path.dirname(os.path.abspath(__file__))

                # Define a pasta de destino para fotos-criancas dentro do diretório do projeto
                destino_dir = os.path.join(projeto_dir, 'assets/imagens/fotos-criancas')

                # Certifique-se de que o diretório de destino existe
                if not os.path.exists(destino_dir):
                    os.makedirs(destino_dir)

                # Caminho completo do arquivo no destino
                destino = os.path.join(destino_dir, os.path.basename(origem))

                # Verificar se o arquivo já existe no destino
                if not os.path.exists(destino):
                    # Copiar o arquivo se ele ainda não foi copiado
                    shutil.copy(origem, destino)
                    print(f"Imagem copiada para: {destino}")
                else:
                    print(f"Arquivo já existe em: {destino}")

                # Armazena o caminho da imagem copiada
                self.destino_imagem = destino

                # Acessa a tela de edição do perfil
                tela_editar_perfil = self.manager.get_screen('TelaEditarPerfil')
                # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                tela_editar_perfil.ids.img_editar_perfil.source = self.destino_imagem 
                # Mantém o botão transparente e sem imagem de fundo
                tela_editar_perfil.ids.image_button.background_normal = ""  # Certifique-se de que o fundo continua transparente
                
                # Volta para a TelaCadastro com a transição
                self.manager.transition.direction = 'right'
                self.manager.current = 'TelaEditarPerfil'

            except Exception as e:
                print(f"Erro ao copiar a imagem: {e}")    

class TelaAtalhos(GradienteScreen2):
    # Função para verificar o clique no botão de ir para o ranking
    def btn_ranking_click(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        ranking = dados_usuario["ranking"]
        print(ranking)
        if ranking.lower() == "habilitado":
            self.manager.current = "TelaRanking"
            self.manager.transition.direction = "left"
            
        else:
            self.show_popup("Erro!", "Você está com o ranking desabilitado!", "erro")
         
    # Função para mostrar o popup
    def show_popup(self, title, message, status):
        self.popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        self.popup.open()
    
         
         

class TelaNotificacoes(GradienteScreen2):
    def on_enter(self):
        # Exemplo de chamada para adicionar uma imagem ao entrar na tela
        self.adicionar_notificacao("assets/imagens/btn-conquista.png")
        self.adicionar_notificacao("assets/imagens/btn-atividade-amarelo.png")
        self.adicionar_notificacao("assets/imagens/btn-atividade-azul.png")

    #Função para adicionar os paineis de notificação
    def adicionar_notificacao(self, image_path):
        # Adiciona o layout do item ao BoxLayout principal
        self.ids.notificacoes.add_widget(FitImage(source=image_path, size_hint=(None, None), size=(358, 104)))

class TelaRanking(TelaAzul):
    def atualizar_dados(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        self.ids.lbl_pontos.text = str(dados_usuario["pontos"])
        self.ids.lbl_medalhas.text = str(dados_usuario["medalhas"])
        self.ids.lbl_ranking.text = str(dados_usuario["fasesConcluidas"])
        
    def atualizar_ranking(self):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                criancas = db["criancas"]
                
                # Ordenando as crianças por pontos em ordem decrescente e limitando a 7 resultados
                top_criancas = list(criancas.find().sort("pontos", -1).limit(7))
                
                # Iterando sobre os resultados e atualizando a interface
                for i, crianca in enumerate(top_criancas):
                    # Exibindo a foto apenas para os três primeiros colocados
                    if i < 3:
                        self.ids[f'img_rank{i+1}'].source = crianca["foto"]
                    
                    # Atualizando nome e pontos para os 7 primeiros colocados
                    self.ids[f'lbl_nome_rank{i+1}'].text = crianca["nome"]
                    self.ids[f'lbl_pts_rank{i+1}'].text = str(crianca["pontos"])
                    
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao atualizar o ranking:", e)

        finally:
            close_connection(client)

class Learny(MDApp):
    dados_usuario = {}
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Definindo o caminho da área de trabalho no momento da inicialização
        self.desktop_path = join(expanduser("~"), "Desktop")
        self.usuario_ativo = None  # Inicializa o usuário ativo como None
    def build(self):
        # Criando uma instãncia do ScreenManager
        sm = ScreenManager()
        # Adicionando as telas no ScreenManager
        sm.add_widget(TelaPerfilPais(name="TelaPerfilPais"))
        '''sm.add_widget(TelaLogin(name="TelaLogin"))
        sm.add_widget(TelaHome(name="TelaHome"))
        sm.add_widget(TelaCadastroPais(name="TelaCadastroPais"))
        sm.add_widget(TelaPerfil(name="TelaPerfil"))
        sm.add_widget(TelaRanking(name="TelaRanking"))
        sm.add_widget(TelaNotificacoes(name="TelaNotificacoes"))
        sm.add_widget(TelaAtalhos(name="TelaAtalhos"))
        sm.add_widget(TelaEditarFotoPerfil(name="TelaEditarFotoPerfil"))
        sm.add_widget(TelaEditarPerfil(name="TelaEditarPerfil"))
        sm.add_widget(TelaCadastro(name="TelaCadastro"))
        sm.add_widget(TelaSelecionarImagem(name="TelaSelecionarImagem"))
        sm.add_widget(TelaBemVindo(name="TelaBemVindo"))'''
        
        return sm

    def on_stop(self):
        # Limpa a variável ao fechar o aplicativo
        self.dados_usuario = None
        
    def set_dados_usuario(self, dados_usuario):
        self.dados_usuario = dados_usuario
        
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
             
        # Armazena a data selecionada em uma variável
        selected_date = value.strftime('%d/%m/%Y')  # Formata a data como dd/mm/yyyy

        # Verifica a tela atual usando o ScreenManager
        tela_atual = self.root.current

        if tela_atual == 'TelaCadastro':
            # Atualiza o campo de data de nascimento na tela de cadastro
            self.root.get_screen('TelaCadastro').ids.txt_data_nasc.text = selected_date
        elif tela_atual == 'TelaEditarPerfil':
            # Atualiza o campo de data de nascimento na tela de edição de perfil
            self.root.get_screen('TelaEditarPerfil').ids.txt_data_nasc.text = selected_date
        
        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker(
            title="Selecione a Data",
            title_input="Digite a Data",
            helper_text=""
        )
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


if __name__ == "__main__":
    Learny().run()
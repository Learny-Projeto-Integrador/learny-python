# Instale as bibliotecas
# pip install pymongo | pip install kivy | pip install kivymd | pip install pygame (ainda não está sendo usado)

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.widget import Widget
from config.conexao import *
from config.conexao_local import *
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty
from os.path import expanduser, join
import shutil
import os
import logging

logging.getLogger('pymongo').setLevel(logging.WARNING)  # Reduz os logs de monitoramento de topologia

# Define o tamanho da janela
Window.size = (400, 700)
Window.left = 550
Window.top = 75

# Gerenciador das telas
class WindowManager(ScreenManager):
    pass

class GradienteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preload_background()

    def preload_background(self):
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(source='assets/imagens/fundo-gradiente.png', size=self.size)

    def on_size(self, *args):
        self.bg_rect.size = self.size  # Atualiza o tamanho do retângulo quando a tela muda

class GradienteScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preload_background()

    def preload_background(self):
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(source='assets/imagens/fundo-gradiente2.png', size=self.size)

    def on_size(self, *args):
        self.bg_rect.size = self.size  # Atualiza o tamanho do retângulo quando a tela muda

class TelaAzul(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preload_background()

    def preload_background(self):
        with self.canvas.before:
            Color(0.42, 0.82, 1, 1)
            self.bg_rect = Rectangle(size=self.size)

    def on_size(self, *args):
        self.bg_rect.size = self.size  # Atualiza o tamanho do retângulo quando a tela muda

class CustomPopup:
    def __init__(self, title, message, icon_path, bg_color, on_dismiss_callback=None, manager=None):
        self.manager = manager  # Salva o manager para uso posterior

        # Layout principal do conteúdo
        content = BoxLayout(orientation="vertical", padding=[10, 0, 10, 20])

        # Adicionando mensagem central
        title_label = Label(
            text="[b]" + title + "[/b]",
            font_size="22sp",
            halign="center",
            valign="top",
            color=(1, 1, 1, 1),
            markup=True  # Ativa o recurso de markup
        )

        # Adicionando mensagem central
        message_label = Label(
            text=message,
            font_size="18sp",
            halign="center",
            valign="top",
            color=(1, 1, 1, 1)
        )
        message_label.bind(size=message_label.setter('text_size'))

        # Adicionando o botão "Fechar" logo abaixo da mensagem
        close_button = Button(
            text="OK",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.5},
            background_color=(0.9, 0.9, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        close_button.bind(on_release=lambda *args: self.close_popup())

        # Adiciona elementos ao layout principal
        content.add_widget(Image(source=icon_path, size_hint_x=None, width=100, pos_hint={"center_x": 0.5}))
        content.add_widget(Widget(size_hint_y=None, height=10))
        content.add_widget(title_label)
        content.add_widget(message_label)
        content.add_widget(Widget(size_hint_y=None, height=20))
        content.add_widget(close_button)

        # Cria o popup com fundo customizado
        self.popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.4),
            background="",
            background_color=bg_color,
            separator_height=0  # Remove o separador
        )
        # Se uma função de callback foi fornecida, associa ao evento de dismiss
        if on_dismiss_callback:
            self.popup.bind(on_dismiss=on_dismiss_callback)

    def open_popup(self):
        self.popup.open()

    def close_popup(self, *args):
        self.popup.dismiss()

class TelaLogin(GradienteScreen):
    def limpar_campos(self, *args):
        # Limpa os campos de texto
        self.ids.txt_usuario.text = ""
        self.ids.txt_senha.text = ""

    def buscar_dados_crianca(self, usuario_banco):
        # Busca os dados da crianca ativa             
        if usuario_banco:
            return {
                'usuario': usuario_banco["usuario"],
                'senha': usuario_banco["senha"],
                'nome': usuario_banco["nome"],
                'data_de_nascimento': usuario_banco["data_de_nascimento"],
                'foto': usuario_banco["foto"],
                'pai': usuario_banco["pai"],
                'pontos': usuario_banco["pontos"],
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
        # Busca os dados do pai ativo             
        if usuario_banco:
            return {
                'id': usuario_banco["_id"],
                'usuario': usuario_banco["usuario"],
                'senha': usuario_banco["senha"],
                'nome': usuario_banco["nome"],
                'email': usuario_banco["email"],
                'foto': usuario_banco["foto"],
                'pontos': usuario_banco["pontos"],
                'titulo': usuario_banco["titulo"],
                'notificacoes': usuario_banco["notificacoes"],
                'frustracaoCrianca': usuario_banco["frustracaoCrianca"],
                'filhoSelecionado': usuario_banco["filhoSelecionado"]
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
                        tela_ranking.atualizar_dados()
                        tela_ranking.atualizar_ranking()
                        
                        self.go_bem_vindo(usuario_banco_crianca["nome"])
                        Clock.schedule_once(self.go_home, 2)  # Aguarda 2 segundos e vai para a tela Home

                elif usuario_banco_pai and usuario_banco_pai['senha'] == senha:
                    dados_usuario = self.buscar_dados_pai(usuario_banco_pai)
                    self.origem_usuario = 'pai'  # Define a origem como 'pai'
                    
                    if dados_usuario:
                        # Passa os dados para a MainApp
                        MDApp.get_running_app().set_dados_usuario(dados_usuario)
                        
                        # Atualiza os dados da tela antes da transição
                        tela_perfil_pais = app.root.get_screen("TelaPerfilPais")
                        tela_perfil_pais.atualizar_dados()
                        
                        self.go_bem_vindo(usuario_banco_pai["nome"])
                        Clock.schedule_once(self.go_home, 2)  # Aguarda 2 segundos e vai para a tela Home
                
                else:
                    # Exibir popup
                    self.show_popup("Erro de Login", "Usuário e/ou senha inválidos!")
                
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao fazer login:", e)

        finally:
            close_connection(client)

    # Função para mostrar o popup
    def show_popup(self, title, message):
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-erro-logar.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
        )
        popup.open_popup()

    # Função para ir para a tela de boas-vindas e mudar o nome de acordo com o usuário autenticado
    def go_bem_vindo(self, usuario):
        self.manager.get_screen('TelaBemVindo').ids.lbl_transicao.text = f"Bem-vindo, {usuario}!"
        self.manager.transition.direction = 'left'
        self.manager.current = 'TelaBemVindo'

    # Função para ir para a tela Home
    def go_home(self, dt):
        self.manager.transition.direction = 'left'
        
        # Redireciona para telas diferentes dependendo se é 'crianca' ou 'pai'
        if self.origem_usuario == 'crianca':
            self.manager.current = 'TelaHome'
            
        elif self.origem_usuario == 'pai':
            self.manager.current = 'TelaPerfilPais' 
    
    def go_cadastro_pais(self):
        tela_cadastro_pais = self.manager.get_screen("TelaCadastroPais")
        tela_cadastro_pais.limpar_campos()
        self.manager.current = "TelaCadastroPais"
        self.manager.transition.direction = "left"

class TelaCadastroPais(GradienteScreen):
    def limpar_campos(self, *args):
        # Limpa os campos de texto
        self.ids.txt_usuario_cadastro.text = ""
        self.ids.txt_senha_cadastro.text = ""
        self.ids.txt_nome_cadastro.text = ""
        self.ids.txt_email_cadastro.text = ""
        self.ids.check1.active = False
        self.ids.check2.active = False
        self.ids.check3.active = False
        self.ids.check4.active = False
        self.ids.check5.active = False

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
                nome = self.ids.txt_nome_cadastro.text 
                email = self.ids.txt_email_cadastro.text
                
                # Verifica se já existe um usuário com esse nome no banco
                buscar_existente_pais = pais.find_one({"usuario": usuario})
                buscar_existente_criancas = criancas.find_one({"usuario": usuario})
                
                # Acessar a tela de seleção de imagem através do ScreenManager
                tela_selecionar_imagem = self.manager.get_screen('TelaSelecionarImagem')

                # Obter o caminho da imagem copiada
                projeto_dir = os.path.dirname(os.path.abspath(__file__))
                caminho_imagem = None
                if tela_selecionar_imagem.destino_imagem:
                    caminho_imagem = os.path.relpath(tela_selecionar_imagem.destino_imagem, projeto_dir)
                
                if buscar_existente_pais or buscar_existente_criancas:
                    self.show_popup_erro("Erro de Cadastro", "Nome de usuário já existente!")
                
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
                            'titulo': '',
                            'notificacoes': [],
                            'frustracaoCrianca': self.nivel_frustracao,
                            'filhoSelecionado': ""
                        }
                        resultado_insercao = pais.insert_one(pai)
                        self.id_pai_cadastro = resultado_insercao.inserted_id  # Obter o ID do pai recém-cadastrado
                        
                        # Exibir popup de sucesso
                        self.show_popup("Dados Cadastrados", "Seus dados foram cadastrados com sucesso!")
                    else:
                        # Exibir popup de erro se faltar dados
                        self.show_popup_erro("Erro de Cadastro", "Preencha todos os campos!")
                        
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao cadastrar o pai:", e)

        finally:
            close_connection(client)


    def go_selecionar_foto(self):
        tela_selecionar_foto = self.manager.get_screen("TelaSelecionarImagem")
        tela_selecionar_foto.tipo_usuario = "pai"
        self.manager.transition.direction = 'left'
        self.manager.current = "TelaSelecionarImagem"

    # Função para mostrar o popup
    def show_popup(self, title, message):
        # Função de redirecionamento após o fechamento do popup
        def go_login_after_popup(*args):
            if self.manager:  # Verifica se o manager foi passado
                tela_login = self.manager.get_screen("TelaLogin")
                tela_login.limpar_campos()
                self.manager.transition.direction = 'right'
                self.manager.current = 'TelaLogin'

        # Cria o popup
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-sucesso.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
            on_dismiss_callback=go_login_after_popup,  # Só adiciona a callback se for sucesso
            manager=self.manager  # Passa o manager para o popup
        )
        popup.open_popup()
    
    # Função para mostrar o popup
    def show_popup_erro(self, title, message):
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-erro.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
        )
        popup.open_popup()

class TelaCadastro(GradienteScreen):
    id_pai = None

    def limpar_campos(self, *args):
        # Limpa os campos de texto
        self.ids.txt_usuario_cadastro.text = ""
        self.ids.txt_senha_cadastro.text = ""
        self.ids.txt_nome_cadastro.text = ""
        self.ids.txt_data_nasc.text = ""

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
                nome = self.ids.txt_nome_cadastro.text
                data_nasc = self.ids.txt_data_nasc.text
                
                # verifica se já existe um usuário com esse nome no banco
                buscar_existente_criancas = criancas.find_one({"usuario": usuario})
                buscar_existente_pais = pais.find_one({"usuario": usuario})
                
                # Acessar a tela de seleção de imagem através do ScreenManager
                tela_selecionar_imagem = self.manager.get_screen('TelaSelecionarImagem')

                # Obter o caminho da imagem copiada
                projeto_dir = os.path.dirname(os.path.abspath(__file__))
                caminho_imagem = None
                if tela_selecionar_imagem.destino_imagem:
                    caminho_imagem = os.path.relpath(tela_selecionar_imagem.destino_imagem, projeto_dir)
                
                if buscar_existente_criancas or buscar_existente_pais:
                    self.show_popup_erro("Erro de Cadastro", "Nome de usuário já existente!")
                
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
                        self.show_popup("Dados Cadastrados", "Seus dados foram cadastrados com sucesso!")
                    else:
                        # Exibir popup de erro se faltar dados
                        self.show_popup_erro("Erro de Cadastro", "Preencha todos os campos!")
                        
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao cadastrar a criança:", e)

        finally:
            close_connection(client)


    # Função para mostrar o popup
    def show_popup(self, title, message):
        # Função para ir para o login
        def go_pai_after_popup(*args):
            if self.manager:  # Verifica se o manager foi passado
                tela_perfil_pais = self.manager.get_screen("TelaPerfilPais")
                tela_perfil_pais.atualizar_dados()
                self.manager.transition.direction = 'right'
                self.manager.current = 'TelaPerfilPais'

        # Cria o popup
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-sucesso.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
            on_dismiss_callback=go_pai_after_popup,  # Só adiciona a callback se for sucesso
            manager=self.manager  # Passa o manager para o popup
        )
        popup.open_popup()

    # Função para mostrar o popup
    def show_popup_erro(self, title, message):
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-erro.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
        )
        popup.open_popup()
        
    
    def go_selecionar_foto(self):
        tela_selecionar_foto = self.manager.get_screen("TelaSelecionarImagem")
        tela_selecionar_foto.tipo_usuario = "crianca"
        self.manager.transition.direction = 'left'
        self.manager.current = "TelaSelecionarImagem"

class TelaSelecionarImagem(GradienteScreen, Widget):
    
    tipo_usuario = None
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

                # Certificando de que o diretório de destino existe
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

                if self.tipo_usuario == "crianca":
                    tela_cadastro = self.manager.get_screen('TelaCadastro')
                    # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                    tela_cadastro.ids.img_cadastro.source = self.destino_imagem
                    # Remove o texto "+" do botão
                    tela_cadastro.ids.image_button.text = ""  
                    # Mantém o botão transparente e sem imagem de fundo
                    tela_cadastro.ids.image_button.background_normal = ""  # Certificando de que o fundo continua transparente

                    self.manager.transition.direction = 'right'
                    self.manager.current = 'TelaCadastro'
                    
                elif self.tipo_usuario == "pai":
                    tela_cadastro = self.manager.get_screen('TelaCadastroPais')
                    # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                    tela_cadastro.ids.img_cadastro.source = self.destino_imagem
                    # Remove o texto "+" do botão
                    tela_cadastro.ids.image_button.text = ""  
                    # Mantém o botão transparente e sem imagem de fundo
                    tela_cadastro.ids.image_button.background_normal = ""  # Certificando de que o fundo continua transparente

                    self.manager.transition.direction = 'right'
                    self.manager.current = 'TelaCadastroPais'

            except Exception as e:
                print(f"Erro ao copiar a imagem: {e}")

    # Função para o botão de voltar
    def voltar(self):
        if self.tipo_usuario == "crianca":
            self.manager.transition.direction = 'right'
            self.manager.current = 'TelaCadastro'
        elif self.tipo_usuario == "pai":
            self.manager.transition.direction = 'right'
            self.manager.current = 'TelaCadastroPais'

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
    fator_progresso = 0
    def atualizar_dados(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        self.ids.foto_perfil.source = dados_usuario["foto"]
        self.ids.lbl_nome_perfil.text = dados_usuario["nome"]

        nivel = int(dados_usuario["pontos"] / 100)
        self.ids.lbl_nivel.text = str(nivel)

        pontos_mostrar = dados_usuario["pontos"] % 100
        self.ids.lbl_pontos.text = str(pontos_mostrar)
        self.fator_progresso = (pontos_mostrar/100)
    
    # Função para verificar o clique no botão de ir para o ranking
    def go_ranking(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        ranking = dados_usuario["ranking"]
        if ranking.lower() == "habilitado":
            tela_ranking = self.manager.get_screen("TelaRanking")
            tela_ranking.tela_anterior = "perfil"
            self.manager.transition.direction = "left"
            self.manager.current = "TelaRanking"
            
        else:
            self.show_popup("Erro!", "Você está com o ranking desabilitado!")
        
    def on_switch_active(self, switch, active):
        pass

    # Função para mostrar o popup
    def show_popup(self, title, message):
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-erro.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
        )
        popup.open_popup()

            
# Definindo uma classe para adicionar os paineis dos filhos no dropdown
class PainelFilho(ButtonBehavior, BoxLayout):
    image_path = StringProperty("assets/imagens/fotos-criancas/joana.jpg")
    nome_filho = StringProperty("Luiza Carla")
    border_radius = ListProperty([20])  # Define o radius padrão para 20

    
# Código kv do painel
Builder.load_string("""
<PainelFilho>:
    orientation: 'horizontal'
    size_hint_y: None
    height: 100
    padding: [30, 0, 0, 0]
    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.border_radius
            source: 'assets/imagens/fundo-gradiente.png'

    MDCard:
        size_hint: None, None
        width: 60
        height: 60
        radius: [100]
        pos_hint: {'center_y': 0.5}
        elevation: 0
        shadow_color: (0, 0, 0, 0.3)

        FloatLayout:
            FitImage:
                source: root.image_path
                size_hint: (1, 1)
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [100]

    Widget:
        size_hint_x: None
        width: 20

    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        spacing: 5
        pos_hint: {'center_y': 0.5}

        MDLabel:
            text: "Filha:"
            font_name: "assets/fontes/montserrat/Montserrat-Regular.ttf"
            font_size: "14sp"
            halign: "left"
            size_hint_y: None
            height: self.texture_size[1]
            theme_text_color: "Custom"
            text_color: (1, 1, 1, 1)

        MDLabel:
            text: root.nome_filho
            font_name: "assets/fontes/montserrat/Montserrat-Bold.ttf"
            font_size: "18sp"
            halign: "left"
            size_hint_y: None
            height: self.texture_size[1]
            theme_text_color: "Custom"
            text_color: (1, 1, 1, 1)
""")
    
class TelaPerfilPais(Screen):
    id_pai = None
    lista_filhos = []
    filho_selecionado = ""
    fator_progresso = 0
    foto_pai = None
    trocar = True # Variável para controlar a chamada da função atualizar_rankig no MDSwitch
    
    def buscar_dados_crianca(self, usuario_banco):
        # Busca os dados do usuário ativo               
        if usuario_banco:
            return {
                'id': usuario_banco["_id"],
                'nome': usuario_banco["nome"],
                'foto': usuario_banco["foto"],
                'pontos': usuario_banco["pontos"],
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
        self.id_pai = dados_usuario["id"]
        self.foto_pai = dados_usuario["foto"]
        self.ids.foto_perfil_pai.source = self.foto_pai
        self.ids.lbl_nome_pai.text = dados_usuario["nome"]
        self.filho_selecionado = dados_usuario["filhoSelecionado"]
        
        pontos_titulo = dados_usuario["pontos"] / 100
        if pontos_titulo >= 0 and pontos_titulo < 2:
            self.ids.lbl_titulo_pai.text = "OWL PARENT"
            self.ids.lbl_titulo_pai.text_color = (1, 0.8, 0.3, 1)

        elif pontos_titulo >= 2 and pontos_titulo < 3:
            self.ids.lbl_titulo_pai.text = "SUPER PARENT"
            self.ids.lbl_titulo_pai.text_color = (0.93, 0.35, 0.41, 1)

        elif pontos_titulo >= 3:
            self.ids.lbl_titulo_pai.text = "WONDERFUL PARENT"
            self.ids.lbl_titulo_pai.text_color = (1, 0.8, 0.3, 1)

        pontos_mostrar = dados_usuario["pontos"] % 100
        self.ids.lbl_pontos.text = str(pontos_mostrar)
        self.fator_progresso = (pontos_mostrar/100)
        
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção de filhos
                criancas = db["criancas"]
                
                # Buscando todos os filhos do pai no banco de dados
                filhos_cursor = criancas.find({"pai": self.id_pai})
                
                # Limpa a lista de filhos antes de adicionar novos
                self.lista_filhos.clear()
                
                filhos = list(filhos_cursor)  # Convertendo o cursor em uma lista
                
                # Loop para adicionar os filhos
                for index, filho in enumerate(filhos):
                    dados_filho = self.buscar_dados_crianca(filho)
                    if dados_filho:
                        self.lista_filhos.append(dados_filho)
                
                if not self.lista_filhos:
                    print("Nenhum filho encontrado.")
                    
                # Atualiza o painel principal com o filho selecionado
                filho_encontrado = False
                for i in self.lista_filhos:
                    if i["id"] == self.filho_selecionado:
                        self.ids.img_filho_principal.source = i["foto"]
                        self.ids.lbl_nome_filho_principal.text = i["nome"]
                        if i["ranking"] == "habilitado":
                            self.ids.switch_ranking.active = True
                        
                        filho_encontrado = True
                        break
                
                # Se não tiver filho selecionado, pega o primeiro filho
                if not filho_encontrado and self.lista_filhos:
                    self.ids.img_filho_principal.source = self.lista_filhos[0]["foto"]
                    self.ids.lbl_nome_filho_principal.text = self.lista_filhos[0]["nome"]
                    self.filho_selecionado = self.lista_filhos[0]["id"]  # Atualiza para o primeiro filho
                
            else:
                print("Erro na conexão com o banco de dados.")
        except PyMongoError as e:
            print("Erro ao buscar os dados da criança:", e)
        finally:
            close_connection(client)

    def atualizar_filhos_selecionado(self, id_filho):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Atualiza o filho selecionado no banco de dados
                pais = db["pais"]
                pais.update_one({"_id": self.id_pai}, {"$set": {"filhoSelecionado": id_filho}})
                
                # Atualiza a tela com o novo filho selecionado
                layout_filhos = self.ids.filhos
                painel_principal = self.ids.painel_principal_filhos  # Painel que sempre permanece ativo
                
                # Verifica se há outros widgets além do painel principal
                if any(child != painel_principal for child in layout_filhos.children):
                    # Remove todos os painéis dinâmicos, mantendo o painel principal
                    for child in layout_filhos.children[:]:
                        if child != painel_principal:
                            layout_filhos.remove_widget(child)
                    
                    # Reseta o radius inferior do painel principal        
                    self.radius_painel_principal = [20]    

                # Atualiza o painel principal com o novo filho selecionado pegando diretamente da lista de filhos
                for i in self.lista_filhos:
                    if i["id"] == id_filho:
                        self.ids.img_filho_principal.source = i["foto"]
                        self.ids.lbl_nome_filho_principal.text = i["nome"]
                        # Deixa trocar como False para que o switch não chame a função de atualizar ranking
                        self.trocar = False
                        if i["ranking"] == "habilitado":
                            self.ids.switch_ranking.active = True
                        else:
                            self.ids.switch_ranking.active = False
                        # Volta trocar para true para que o switch volte chame a função de atualizar ranking
                        self.trocar = True
                        break

            else:
                print("Erro na conexão com o banco de dados.")
        except PyMongoError as e:
            print("Erro ao atualizar filho selecionado:", e)
        finally:
            close_connection(client)

    def on_switch_active(self, instance, value):
        # Atualizar o banco de dados quando o switch for alternado
        if self.trocar:
            self.atualizar_estado_ranking(value)

    def atualizar_estado_ranking(self, valor):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Atualiza o ranking no banco de dados
                crianca = db["criancas"]
                novo_status = "habilitado" if valor else "desabilitado"
                crianca.update_one({"_id": self.filho_selecionado}, {"$set": {"ranking": novo_status}})
                
                # Atualiza o ranking na lista local
                for i in self.lista_filhos:
                    if i["id"] == self.filho_selecionado:
                        i["ranking"] = novo_status
                        break

            else:
                print("Erro na conexão com o banco de dados.")
        except PyMongoError as e:
            print("Erro ao atualizar o ranking do filho selecionado:", e)
        finally:
            close_connection(client)

       
    radius_painel_principal = ListProperty([20])  # Valor padrão   
    
    def on_dropdown_click(self):
        # Obter o layout onde os painéis filhos serão adicionados
        layout_filhos = self.ids.filhos
        painel_principal = self.ids.painel_principal_filhos  # Painel que sempre permanece ativo

        # Verifica se há outros widgets além do painel principal
        if any(child != painel_principal for child in layout_filhos.children):
            # Remove todos os painéis dinâmicos, mantendo o painel principal
            for child in layout_filhos.children[:]:
                if child != painel_principal:
                    layout_filhos.remove_widget(child)

            # Reseta o radius inferior do painel principal        
            self.radius_painel_principal = [20]
        else:
            # Filtrar filhos que não são o selecionado
            filhos_dropdown = [filho for filho in self.lista_filhos if filho["id"] != self.filho_selecionado]

            # Adiciona os filhos ao painel dinâmico
            for index, filho in enumerate(filhos_dropdown):
                # Se o filho for o último na lista filtrada, aplica a borda inferior
                if index == len(filhos_dropdown) - 1:
                    radius = [0, 0, 20, 20]  # Último painel com borda inferior
                else:
                    radius = [0, 0, 0, 0]  # Painéis anteriores sem borda inferior

                self.adicionar_painel_filho(filho["id"], filho["foto"], filho["nome"], radius)


    def on_painel_filho_clicado(self, instance):
        print(f"Painel '{instance.nome_filho}' foi clicado!")
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Pega os dados da crianca que vai ser atualizada através do nome
                crianca = db["criancas"].find_one({"nome": instance.nome_filho})
                
                if crianca is not None:
                    self.atualizar_filhos_selecionado(crianca["_id"])
                    self.filho_selecionado = crianca["_id"]

                else:
                    print(f"Nenhum filho encontrado com o nome '{instance.nome_filho}'.")
            else:
                print("Erro na conexão com o banco de dados.")
        except PyMongoError as e:
            print("Erro ao atualizar filho selecionado:", e)
        finally:
            close_connection(client)

    def adicionar_painel_filho(self, id_filho_painel, image_path, nome, radius):
        # Cria uma nova instância de PainelFilho com imagem e nome específicos
        painel = PainelFilho()
        painel.id_filho = id_filho_painel
        painel.image_path = image_path
        painel.nome_filho = nome
        painel.border_radius = radius 
        # Adiciona um evento de clique para o painel inteiro
        painel.bind(on_press=self.on_painel_filho_clicado)
        
        # Adiciona o painel ao layout principal
        self.ids.filhos.add_widget(painel)
        self.radius_painel_principal = [20, 20, 0, 0]
        
    # Função para ir para o cadastro do filho
    def cadastrar_filho(self):
        tela_cadastro_filho = self.manager.get_screen('TelaCadastro')
        tela_cadastro_filho.limpar_campos()
        tela_cadastro_filho.id_pai = self.id_pai  # Define o id do pai na tela do filho
        self.manager.transition.direction = 'left'
        self.manager.current = 'TelaCadastro'

    def go_editar_foto(self):
        tela_editar_foto = self.manager.get_screen("TelaEditarFotoPerfil")
        tela_editar_foto.foto_usuario = self.foto_pai
        tela_editar_foto.tipo_usuario = "pai"
        tela_editar_foto.id_pai = self.id_pai
        self.manager.transition.direction = 'left'
        self.manager.current = "TelaEditarFotoPerfil"
    
    def voltar(self):
        tela_login = self.manager.get_screen("TelaLogin")
        tela_login.limpar_campos()
        self.manager.transition.direction = 'right'
        self.manager.current = 'TelaLogin'
 
class TelaEditarPerfil(GradienteScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dados_carregados = False  # Variável para controlar se a foto foi carregada
        self.id_crianca = None
        self.foto = None
        
    def on_enter(self, *args):
        # Puxa os dados do usuário ativo
        dados_usuario = MDApp.get_running_app().dados_usuario
        if dados_usuario:
            try:
                client, db = create_local_connection()
                if db is not None:
                    criancas = db["criancas"]
                    usuario_banco = criancas.find_one({"usuario": dados_usuario["usuario"]})
                    
                    # Armazena os dados vindos do banco em variáveis
                    self.id_crianca = usuario_banco["_id"]
                    senha = usuario_banco["senha"]
                    nome = usuario_banco["nome"]
                    data_nasc = usuario_banco["data_de_nascimento"]
                    self.foto = usuario_banco["foto"]
                    
                    if not self.dados_carregados:
                        # Exibe a imagem do usuário ativo
                        self.ids.img_editar_perfil.source = self.foto
                        self.ids.img_editar_perfil.reload()  # Recarregar a imagem
                        
                        # Exibe os dados do usuário ativo
                        self.ids.txt_usuario_editar.text = usuario_banco["usuario"]
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
                nome = self.ids.txt_nome_editar.text
                data_nasc = self.ids.txt_data_nasc.text
                
                # Acessar a tela de edição de imagem através do ScreenManager
                tela_editar_foto_perfil = self.manager.get_screen('TelaEditarFotoPerfil')

                # Obter o caminho da imagem copiada
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
                        self.show_popup("Dados Atualizados", "Seus dados foram atualizados com sucesso!")
                    else:
                        # Voltar para o perfil se não tiverem mudanças
                        self.manager.transition.direction = 'right'
                        self.manager.current = 'TelaPerfil'
                else:
                    # Exibir popup de erro se faltar dados
                    self.show_popup_erro("Erro de Edição", "Preencha todos os campos!")
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao atualizar a criança:", e)

        finally:
            close_connection(client)

    # Função para mostrar o popup
    def show_popup(self, title, message):
        # Função para ir para o login
        def go_login_after_popup(*args):
            if self.manager:  # Verifica se o manager foi passado
                tela_login = self.manager.get_screen("TelaLogin")
                tela_login.limpar_campos()
                self.manager.transition.direction = 'right'
                self.manager.current = 'TelaLogin'

        # Cria o popup
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-sucesso.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
            on_dismiss_callback=go_login_after_popup,  # Só adiciona a callback se for sucesso
            manager=self.manager  # Passa o manager para o popup
        )
        popup.open_popup()

    # Função para mostrar o popup
    def show_popup_erro(self, title, message):
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-erro.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
        )
        popup.open_popup()

    def go_editar_foto(self):
        tela_editar_foto = self.manager.get_screen("TelaEditarFotoPerfil")
        tela_editar_foto.foto_usuario = self.foto
        tela_editar_foto.tipo_usuario = "crianca"
        self.manager.transition.direction = 'left'
        self.manager.current = "TelaEditarFotoPerfil"
    

class TelaEditarFotoPerfil(GradienteScreen):    
    
    foto_usuario = None
    tipo_usuario = None
    id_pai = None
    destino_imagem = None  # Variável para armazenar o caminho da imagem copiada

    def on_enter(self, *args):
        self.ids.exibe_imagem.source = self.foto_usuario

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

                # Certificando de que o diretório de destino existe
                if not os.path.exists(destino_dir):
                    os.makedirs(destino_dir)

                # Caminho completo do arquivo no destino
                destino = os.path.join(destino_dir, os.path.basename(origem))

                # Verificando se o arquivo já existe no destino
                if not os.path.exists(destino):
                    # Copiar o arquivo se ele ainda não foi copiado
                    shutil.copy(origem, destino)
                    print(f"Imagem copiada para: {destino}")
                else:
                    print(f"Arquivo já existe em: {destino}")

                # Armazena o caminho da imagem copiada
                self.destino_imagem = destino
                projeto_dir = os.path.dirname(os.path.abspath(__file__))
                caminho_imagem = os.path.relpath(self.destino_imagem, projeto_dir)

                if self.tipo_usuario == "crianca":
                    tela_editar_perfil = self.manager.get_screen('TelaEditarPerfil')
                    # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                    tela_editar_perfil.ids.img_editar_perfil.source = caminho_imagem
                    # Mantém o botão transparente e sem imagem de fundo
                    tela_editar_perfil.ids.image_button.background_normal = ""  # Certificando de que o fundo continua transparente
                    
                    self.manager.transition.direction = 'right'
                    self.manager.current = 'TelaEditarPerfil'
                
                elif self.tipo_usuario == "pai":
                    tela_perfil = self.manager.get_screen('TelaPerfilPais')
                    # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                    tela_perfil.foto_pai = self.destino_imagem 
                    tela_perfil.ids.foto_perfil_pai.source = caminho_imagem

                    try:
                        client, db = create_local_connection()  # Conectar ao MongoDB
                        if db is not None:
                            pais = db["pais"]
                            pais.update_one({"_id": self.id_pai}, {"$set": {"foto": caminho_imagem}})
                                 
                        else:
                            print("Erro na conexão com o banco de dados.")

                    except PyMongoError as e:
                        print("Erro ao atualizar a foto:", e)

                    finally:
                        close_connection(client)
                    
                    self.manager.transition.direction = 'right'
                    self.manager.current = 'TelaPerfilPais'

            except Exception as e:
                print(f"Erro ao copiar a imagem: {e}")    

    # Função para o botão de voltar
    def voltar(self):
        if self.tipo_usuario == "crianca":
            self.manager.transition.direction = 'right'
            self.manager.current = 'TelaEditarPerfil'
        elif self.tipo_usuario == "pai":
            self.manager.transition.direction = 'right'
            self.manager.current = 'TelaPerfilPais'


class TelaAtalhos(GradienteScreen2):
    # Função para verificar o clique no botão de ir para o ranking
    def go_ranking(self):
        dados_usuario = MDApp.get_running_app().dados_usuario
        ranking = dados_usuario["ranking"]
        if ranking.lower() == "habilitado":
            tela_ranking = self.manager.get_screen("TelaRanking")
            tela_ranking.tela_anterior = "atalhos"
            self.manager.transition.direction = "left"
            self.manager.current = "TelaRanking"
            
        else:
            self.show_popup("Erro!", "Você está com o ranking desabilitado!")
         
    # Função para mostrar o popup
    def show_popup(self, title, message):
        popup = CustomPopup(
            title=title,
            message=message,
            icon_path="assets/imagens/icon-erro.png",  # Caminho para o ícone
            bg_color=(0.2, 0.2, 0.2, 1),  # Cor de fundo (RGBA)
        )
        popup.open_popup()
    
class TelaNotificacoes(GradienteScreen2):
    def on_enter(self):
        # Adicionando notificações
        self.adicionar_notificacao("assets/imagens/btn-conquista.png")
        self.adicionar_notificacao("assets/imagens/btn-atividade-amarelo.png")
        self.adicionar_notificacao("assets/imagens/btn-atividade-azul.png")

    # Função para adicionar os paineis de notificação
    def adicionar_notificacao(self, image_path):
        # Adiciona o layout do item ao BoxLayout principal
        self.ids.notificacoes.add_widget(FitImage(source=image_path, size_hint=(None, None), size=(358, 104)))

class TelaRanking(TelaAzul):
    tela_anterior = None

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
                    
                    # Atualizando nome e pontos para o os rankings 4 a 7
                    self.ids[f'lbl_nome_rank{i+1}'].text = crianca["nome"]
                    self.ids[f'lbl_pts_rank{i+1}'].text = str(crianca["pontos"])

                # Se houver menos de 7 crianças, preenche os campos restantes com valores vazios
                for i in range(len(top_criancas), 7):
                    # Exibindo a foto apenas para os três primeiros colocados
                    if i < 3:
                        self.ids[f'img_rank{i+1}'].source = ""   # Imagem vazia

                    self.ids[f'lbl_nome_rank{i+1}'].text = ""  # Nome vazio
                    self.ids[f'lbl_pts_rank{i+1}'].text = ""  # Pontos vazios
                    
            else:
                print("Erro na conexão com o banco de dados.")

        except PyMongoError as e:
            print("Erro ao atualizar o ranking:", e)

        finally:
            close_connection(client)

    # Função para o botão de voltar
    def voltar(self):
        if self.tela_anterior == "atalhos":
            self.manager.transition.direction = 'right'
            self.manager.current = 'TelaAtalhos'
        elif self.tela_anterior == "perfil":
            self.manager.transition.direction = 'right'
            self.manager.current = 'TelaPerfil'


class Learny(MDApp):
    dados_usuario = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Definindo o caminho da área de trabalho no momento da inicialização
        self.desktop_path = join(expanduser("~"), "Desktop")

    def build(self):
        projeto_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(projeto_dir, 'assets\imagens')

        # Define o ícone da janela
        icon_path = os.path.join(img_dir, 'icon-learny.png') 
        self.icon = icon_path

        # Criando uma instãncia do ScreenManager
        sm = ScreenManager()
        # Adicionando as telas no ScreenManager
        sm.add_widget(TelaLogin(name="TelaLogin"))
        sm.add_widget(TelaCadastro(name="TelaCadastro"))
        sm.add_widget(TelaPerfilPais(name="TelaPerfilPais"))
        sm.add_widget(TelaHome(name="TelaHome"))
        sm.add_widget(TelaCadastroPais(name="TelaCadastroPais"))
        sm.add_widget(TelaPerfil(name="TelaPerfil"))
        sm.add_widget(TelaRanking(name="TelaRanking"))
        sm.add_widget(TelaNotificacoes(name="TelaNotificacoes"))
        sm.add_widget(TelaAtalhos(name="TelaAtalhos"))
        sm.add_widget(TelaEditarFotoPerfil(name="TelaEditarFotoPerfil"))
        sm.add_widget(TelaEditarPerfil(name="TelaEditarPerfil"))
        sm.add_widget(TelaSelecionarImagem(name="TelaSelecionarImagem"))
        sm.add_widget(TelaBemVindo(name="TelaBemVindo"))
        
        return sm

    def on_stop(self):
        # Limpa a variável ao fechar o aplicativo
        self.dados_usuario = None
        
    def set_dados_usuario(self, dados_usuario):
        self.dados_usuario = dados_usuario
        
    def on_save(self, instance, value, date_range):            
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
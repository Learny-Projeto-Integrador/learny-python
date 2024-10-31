# Instale as bibliotecas
# pip install pymongo | pip install kivy | pip install pygame (ainda não está sendo usado)

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
    pass

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preload_background()

    def preload_background(self):
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Altere para a cor desejada se precisar
            self.bg_rect = Rectangle(source='assets/imagens/fundo-gradiente.png', size=self.size)

    def on_size(self, *args):
        self.bg_rect.size = self.size  # Atualiza o tamanho do retângulo quando a tela muda

class TelaLogin(BaseScreen):
    # Função onclick para o botão entrar
    def on_enter_button_click(self):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção de usuários (no caso, a coleção "criancas")
                criancas = db["criancas"]
                
                # Variáveis que armazenam os valores obtidos nos campos
                usuario = self.ids.txt_usuario.text
                senha = self.ids.txt_senha.text

                # Buscar o usuário na coleção pelo nome de usuário
                usuario_banco = criancas.find_one({"usuario": usuario})

                # Verificar se o usuário foi encontrado e se a senha está correta
                if usuario_banco and usuario_banco['senha'] == senha:
                    self.go_bem_vindo(usuario_banco["nome"])  # Trocar o nome pelo nome do usuário autenticado
                    Clock.schedule_once(self.go_home, 2)  # Aguarda 2 segundos e vai para a tela Home
                    app = MDApp.get_running_app()
                    app.usuario_ativo = usuario_banco
                else:
                    self.show_popup("Erro de Login", "Usuário ou senha incorretos.")
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
        self.manager.current = 'TelaHome'  # Muda para a tela Home


class TelaCadastro(BaseScreen):
    # Função onclick para o botão cadastrar
    def on_register_button_click(self):
        try:
            client, db = create_local_connection()  # Conectar ao MongoDB
            if db is not None:
                # Buscando a coleção para adicionar
                criancas = db["criancas"]
                
                # Variáveis que armazenam os valores obtidos nos campos
                usuario = self.ids.txt_usuario_cadastro.text
                senha = self.ids.txt_senha_cadastro.text
                nome = self.ids.txt_nome_cadastro.text  # Novo campo de nome
                data_nasc = self.ids.txt_data_nasc_cadastro.text
                
                # Acessar a tela de seleção de imagem através do ScreenManager
                tela_selecionar_imagem = self.manager.get_screen('TelaSelecionarImagem')

                # Obter o caminho da imagem copiada
                # Obtendo caminho relativo a partir do diretório do projeto
                projeto_dir = os.path.dirname(os.path.abspath(__file__))
                caminho_imagem = os.path.relpath(tela_selecionar_imagem.destino_imagem, projeto_dir)
                
                # Lógica de Cadastro
                if usuario != "" and senha != "" and nome != "" and data_nasc != "" and caminho_imagem is not None:
                    crianca = {
                        'usuario': usuario,
                        'senha': senha,
                        'nome': nome,  # Novo campo de nome
                        'data_de_nascimento': data_nasc,
                        'foto': caminho_imagem
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
            self.popup.bind(on_dismiss=self.go_home_after_popup) # Se deu certo o cadastro ele vai para o login ao fechar o popup
        else:
            pass
        self.popup.open()
    
    # Função para ir para a home
    def go_home_after_popup(self, instance):
        self.manager.transition.direction = 'right'  # Define a direção para a transição
        self.manager.current = 'TelaLogin'  # Muda para a tela Home

class TelaSelecionarImagem(BaseScreen, Widget):
    
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

            except Exception as e:
                print(f"Erro ao copiar a imagem: {e}")

class TelaBemVindo(BaseScreen):
    pass

class TelaHome(BaseScreen):
    pass

class TelaPerfil(Screen):
    def on_switch_active(self, switch, active):
        if active:
            print("O switch está ativado")
        else:
            print("O switch está desativado")
 
class TelaEditarPerfil(BaseScreen):
    pass  

class TelaEditarFotoPerfil(BaseScreen):
    try:
        client, db = create_local_connection()  # Conectar ao MongoDB
        if db is not None:
            # Buscando a coleção de usuários (no caso, a coleção "criancas")
            criancas = db["criancas"]
            
            # Variáveis que armazenam os valores obtidos nos campos
            app = MDApp.get_running_app()
            '''
            usuario_banco = app.usuario_ativo
            
            # Buscar o usuário na coleção pelo nome de usuário
            usuario_banco = criancas.find_one({"usuario": usuario})
            
            # Pegar a foto do usuário ativo
            foto = usuario_banco['foto']
            
            try:
                # Exibe a imagem selecionada
                self.ids.exibe_imagem.source = foto
                self.ids.exibe_imagem.reload()  # Recarregar a imagem
            except Exception as e:
                print(f"Erro ao exibir a imagem atual do usuário ativo: {e}")
            '''
    except PyMongoError as e:
        print("Erro buscar o usuário ativo:", e)

    finally:
        close_connection(client)
    
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

                # Acessa a tela de cadastro
                tela_editar_perfil = self.manager.get_screen('TelaEditarPerfil')
                # Atualiza a imagem dentro do MDCard (substitui a imagem no FitImage)
                tela_cadastro.ids.img_editar_perfil.source = self.destino_imagem
                # Remove o texto "+" do botão
                tela_cadastro.ids.image_button.text = ""  
                # Mantém o botão transparente e sem imagem de fundo
                tela_cadastro.ids.image_button.background_normal = ""  # Certifique-se de que o fundo continua transparente

                # Volta para a TelaCadastro com a transição
                self.manager.transition.direction = 'right'
                self.manager.current = 'TelaEditarPerfil'

            except Exception as e:
                print(f"Erro ao copiar a imagem: {e}")    
    
class Learny(MDApp):
    usuario_ativo = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Definindo o caminho da área de trabalho no momento da inicialização
        self.desktop_path = join(expanduser("~"), "Desktop")
    def build(self):
        # Criando uma instãncia do ScreenManager
        sm = ScreenManager()
        # Adicionando as telas no ScreenManager
        sm.add_widget(TelaLogin(name="TelaLogin"))
        sm.add_widget(TelaEditarFotoPerfil(name="TelaEditarFotoPerfil"))
        sm.add_widget(TelaEditarPerfil(name="TelaEditarPerfil"))
        sm.add_widget(TelaHome(name="TelaHome"))
        sm.add_widget(TelaPerfil(name="TelaPerfil"))
        sm.add_widget(TelaCadastro(name="TelaCadastro"))
        sm.add_widget(TelaSelecionarImagem(name="TelaSelecionarImagem"))
        sm.add_widget(TelaBemVindo(name="TelaBemVindo"))
        
        return sm

    def on_stop(self):
        # Limpa a variável ao fechar o aplicativo
        self.usuario_ativo = None
        
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        
        # Acessa a tela de cadastro usando o ScreenManager
        tela_cadastro = self.root.get_screen('TelaCadastro')
        
        # Armazena a data selecionada em uma variável
        selected_date = value.strftime('%d/%m/%Y')  # Formata a data como dd/mm/yyyy

        # Atualiza o texto do campo de data de nascimento na tela de cadastro
        tela_cadastro.ids.txt_data_nasc_cadastro.text = selected_date
        
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
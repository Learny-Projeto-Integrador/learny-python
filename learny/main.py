# Instale as bibliotecas
# pip install pymongo | pip install kivy | pip install pygame (ainda não está sendo usado)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.widget import Widget
import shutil
import os

# Define o tamanho da janela
Window.size = (480, 800)

# Gerenciador das telas
class WindowManager(ScreenManager):
    pass

class TelaLogin(Screen):
    # Função onclick para o botão entrar
    def on_enter_button_click(self):
        # Variáveis que armazenam os valores obtidos nos campos
        usuario = self.ids.txt_usuario.text
        senha = self.ids.txt_senha.text
        
        # Lógica de autenticação
        if usuario == "admin" and senha == "1234": # Trocar pela autenticação com os usuários do Banco
            self.go_bem_vindo("Joana") # Trocar o nome pelo nome do usuário que vier do banco
            Clock.schedule_once(self.go_home, 2)  # Aguarda 2 segundos e vai para a tela Home
        else:
            self.show_popup("Erro de Login", "Usuário ou senha incorretos.")

    # Função para mostrar o popup
    def show_popup(self, title, message):
        self.popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        self.popup.open()

    # Função para ir para a tela de boas vindas e mudar o nome de acordo com o usuário autenticado
    def go_bem_vindo(self, usuario):
        self.manager.get_screen('TelaBemVindo').ids.lbl_transicao.text = f"{usuario}" # Troca o texto da label
        self.manager.transition.direction = 'left'  # Define a direção para a transição entre as telas
        self.manager.current = 'TelaBemVindo'  # Muda para a tela de transição do login
        
    # Função para ir para a tela Home
    def go_home(self, dt):
        self.manager.transition.direction = 'left'  # Define a direção para a transição
        self.manager.current = 'TelaHome'  # Muda para a tela Home

class TelaCadastro(Screen):
    # Função onclick para o botão cadastrar
    def on_register_button_click(self):
        # Variáveis que armazenam os valores obtidos nos campos
        usuario = self.ids.txt_usuario_cadastro.text
        senha = self.ids.txt_senha_cadastro.text
        data_nasc = self.ids.txt_data_nasc_cadastro.text
        
        # Acessar a tela de seleção de imagem através do ScreenManager
        tela_selecionar_imagem = self.manager.get_screen('TelaSelecionarImagem')

        # Obter o caminho da imagem copiada
        caminho_imagem = tela_selecionar_imagem.destino_imagem
        
        # Lógica de Cadastro
        if usuario != "" and senha != "" and data_nasc != "" and caminho_imagem is not None: # Verificar se todos os campos foram preenchidos
            # Inserir o código de cadastro para o MongoDB Atlas
            print(f"Usuário: {usuario}, Senha: {senha}, Data de Nascimento: {data_nasc}, Imagem: {caminho_imagem}")
            self.show_popup("Dados Cadastados", "Seus dados foram cadastrados com sucesso!", "ok")      
        else:
            self.show_popup("Erro de Cadastro", "Preencha todos os campos!", "nao")
            print(f"Usuário: {usuario}, Senha: {senha}, Data de Nascimento: {data_nasc}, Imagem: {caminho_imagem}")

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

class TelaBemVindo(Screen):
    pass

class TelaHome(Screen):
    pass

class TelaSelecionarImagem(Screen, Widget):
    
    destino_imagem = None  # Variável para armazenar o caminho da imagem copiada
    
    # Função para mostrar a imagem selecionada, sem copiar
    def mostrar_imagem(self, filename):
        if filename:
            try:
                # Exibe a imagem selecionada
                self.ids.my_image.source = filename[0]
                self.ids.my_image.reload()  # Recarregar a imagem
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
                    self.manager.transition.direction = 'right'  # Define a direção para a transição
                    self.manager.current = 'TelaCadastro'  # Voltar para a TelaCadastro
                else:
                    print(f"Arquivo já existe em: {destino}")
                    
                # Armazena o caminho da imagem copiada
                self.destino_imagem = destino
                
            except Exception as e:
                print(f"Erro ao copiar a imagem: {e}")
    
class Learny(App):
    def build(self):
        # Criando uma instãncia do ScreenManager
        sm = ScreenManager()
        # Adicionando as telas no ScreenManager
        sm.add_widget(TelaLogin(name="TelaLogin"))
        sm.add_widget(TelaCadastro(name="TelaCadastro"))
        sm.add_widget(TelaSelecionarImagem(name="TelaSelecionarImagem"))
        sm.add_widget(TelaHome(name="TelaHome"))
        sm.add_widget(TelaBemVindo(name="TelaBemVindo"))
        
        return sm

if __name__ == "__main__":
    Learny().run()
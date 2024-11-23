class GerenciadorTelas:
    def __init__(self):
        self.telas = {}
        self.tela_atual = None

    def registrar_tela(self, nome, tela):
        self.telas[nome] = tela

    def trocar_tela(self, nome, dados=None):
        if nome in self.telas:
            self.tela_atual = self.telas[nome]
            if dados:
                self.tela_atual.receber_dados(dados)
        else:
            raise ValueError(f"Tela '{nome}' não encontrada!")

    def atualizar(self, eventos):
        if self.tela_atual:
            self.tela_atual.atualizar(eventos)

    def desenhar(self, tela):
        if self.tela_atual:
            self.tela_atual.desenhar(tela)
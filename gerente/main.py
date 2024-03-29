import pyautogui
import requests
from pyautogui import alert
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from telas import *
from botoes import *
from myfirebase import MyFirebase
from functools import partial
import json
from BannerVendedores import BannerVendedores
from BannerVendas import BannerVendas
from BannerEstoque import BannerEstoque
from BannerFuncionario import BannerFuncionario
from BannerProdutos import BannerProdutos
from BannerCupons import BannerCupons

GUI = Builder.load_file("main.kv")

class MainApp(App):
    nome_Estoque = None
    Devolucao_Nome = None
    Entrada_Nome = None
    Nome_Motivo = None
    Cargo_Funcionario = None
    Link_Funcionario = None
    Cargo_Funcionario_Editar = None
    Link_Produto = None

    def build(self):
        self.title = "GERENCIA"
        self.icon = "../imagens/icones/gerente.png"
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = "login"

    def Requisicao_Delete(self, url):
        try:
            requisicao = requests.delete(f'{url}.json')
            if requisicao.ok:
                return requisicao
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def Requisicao_Post(self, url, dic):
        try:
            requisicao = requests.post(f'{url}.json', data=json.dumps(dic))
            if requisicao.ok:
                return requisicao
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def Requisicao_Patch(self, url, dic):
        try:
            requisicao = requests.patch(f'{url}.json', data=json.dumps(dic))
            if requisicao.ok:
                return requisicao
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def Requisicao_Get(self, url):
        try:
            requisicao = requests.get(f'{url}.json')
            if requisicao.ok:
                requisicao_Dic = requisicao.json()
                return requisicao_Dic
            else:
                pyautogui.alert(requisicao)
        except Exception as erro:
            pyautogui.alert(erro)

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def carregarInfos(self, id_Usuario):
        # Limpar Login
        tela = self.root.ids["login"]
        tela.ids["usuario_input"].text = ''
        tela.ids["senha_input"].text = ''
        # Pegar Dados do Usuario
        requisicao_dic = self.Requisicao_Get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Administrador/Usuarios/{id_Usuario}")
        # Carregar Nome
        nome = requisicao_dic['Nome']
        self.nome_Estoque = nome
        nome_perfil = self.root.ids["homepage"]
        nome_perfil.ids["id_nome_vendedor"].text = f"Gerente {requisicao_dic['Nome']}"

    def realizar_login(self, nome, senha):
        self.id_vendedor = MyFirebase.fazer_login(self, nome, senha)
        meu_aplicativo = App.get_running_app()
        if self.id_vendedor != -1 and self.id_vendedor != -2:
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = ''
            self.carregarInfos(self.id_vendedor)
            self.mudar_tela('homepage')
        elif self.id_vendedor == -2:
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = 'Senha Incorreta'
            pagina_login.ids["erro_login"].color = (1, 0, 0, 1)
        else:
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = 'Usuario Incorreto'
            pagina_login.ids["erro_login"].color = (1, 0, 0, 1)

    def Opcoes(self, funcao):
        if funcao == "gvendedores":
            tela = self.root.ids["gerenciarvendedores"]
            tela.ids["filtro"].text = "ESSE MÊS"
            BannerVendedores()
            self.mudar_tela("gerenciarvendedores")
        elif funcao == "comissao":
            BannerVendedores.GravarComissao(self)
        elif funcao == "gvendedor_filtro":
            BannerVendedores.Filtrar(self)
        elif funcao == "gvendas":
            BannerVendas()
            tela = self.root.ids["gerenciarvendas"]
            tela.ids["filtro"].text = "ESSE MÊS"
            self.mudar_tela("gerenciarvendas")
        elif funcao == "gvendas_filtro":
            BannerVendas.Filtrar(self)
        elif funcao == "gestoque":
            BannerEstoque()
            tela = self.root.ids["gerenciarestoque"]
            tela.ids["filtro"].text = "ESSE MÊS"
            self.mudar_tela("gerenciarestoque")
        elif funcao == "gestoque_filtro":
            BannerEstoque.Filtrar(self)
        elif funcao == "gmotivo_filtro":
            BannerEstoque.Filtrar_Motivo(self)
        elif funcao == "gfuncionarios":
            BannerFuncionario()
            self.mudar_tela("listarfuncionarios")
        elif funcao == "add_func":
            self.Cargo_Funcionario = None
            self.Selecao_Funcionario("")
            tela = self.root.ids["adicionarfuncionario"]
            tela.ids["nome_input"].text = ''
            tela.ids["login_input"].text = ''
            tela.ids["senha_input"].text = ''
            tela.ids["cpf_input"].text = ''
            self.mudar_tela("adicionarfuncionario")
        elif funcao == "add_func_add":
            BannerFuncionario.add_conta(self)
        elif funcao == "edit_func":
            BannerFuncionario.editar(self, self.Link_Funcionario, self.Cargo_Funcionario_Editar)
        elif funcao == "del_func":
            BannerFuncionario.deletar(self, self.Link_Funcionario, self.Cargo_Funcionario_Editar)
        elif funcao == "gprodutos":
            BannerProdutos()
            self.mudar_tela("listarprodutos")
        elif funcao == "add_prod":
            tela = self.root.ids["adicionarproduto"]
            tela.ids["nome_input"].text = ''
            tela.ids["qtde_input"].text = ''
            tela.ids["valor_input"].text = ''
            self.mudar_tela("adicionarproduto")
        elif funcao == "add_prod_add":
            BannerProdutos.add_produto(self)
        elif funcao == "edit_prod":
            BannerProdutos.editar(self, self.Link_Produto)
        elif funcao == "cupom":
            tela = self.root.ids["email"]
            tela.ids["titulo_input"].text = ''
            tela.ids["corpo_input"].text = ''
            tela.ids["cupom_input"].text = ''
            tela.ids["desconto_input"].text = ''
            tela.ids["data_input"].text = ''
            self.mudar_tela("email")
        elif funcao == "enviar_email":
            BannerCupons()
        elif funcao == "emailpadrao":
            BannerCupons.cupom_padrao(self)
        elif funcao == "salvar_email_padrao":
            BannerCupons.salvar_cupom_padrao(self)

    def Motivo(self, nome, extra, *args):
        if nome != "Atualizar":
            self.Nome_Motivo = nome
            BannerEstoque.Listar_Motivos(self)

    def Selecao_Funcionario(self, botao):
        tela = self.root.ids["adicionarfuncionario"]
        if botao != "bt-vendedor":
            tela.ids["bt-vendedor"].color = 0,0,0,1
        else:
            tela.ids["bt-vendedor"].color = 1,0,0,1
            self.Cargo_Funcionario = "Vendedor"
        if botao != "bt-adm":
            tela.ids["bt-adm"].color = 0,0,0,1
        else:
            tela.ids["bt-adm"].color = 1,0,0,1
            self.Cargo_Funcionario = "ADM"
        if botao != "bt-estoque":
            tela.ids["bt-estoque"].color = 0,0,0,1
        else:
            tela.ids["bt-estoque"].color = 1,0,0,1
            self.Cargo_Funcionario = "Estoque"
        if botao != "bt-caixa":
            tela.ids["bt-caixa"].color = 0,0,0,1
        else:
            tela.ids["bt-caixa"].color = 1,0,0,1
            self.Cargo_Funcionario = "Caixa"

MainApp().run()
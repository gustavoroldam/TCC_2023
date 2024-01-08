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

GUI = Builder.load_file("main.kv")

class MainApp(App):
    nome_Estoque = None
    Devolucao_Nome = None
    Entrada_Nome = None
    Nome_Motivo = None
    Cargo_Funcionario = None

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

    # def Devolucao_Selecionar(self, nome, *args):
    #     meu_aplicativo = App.get_running_app()
    #     self.Devolucao_Nome = nome
    #     # pintar de branco todos os outros caras
    #     pagina_home = meu_aplicativo.root.ids["devolucao"]
    #     lista_produtos = pagina_home.ids["lista_produtos"]
    #     for item in list(lista_produtos.children):
    #         item.color = (0, 0, 0, 1)
    #         try:
    #             texto = item.text
    #             if nome in texto:
    #                 item.color = (1, 1, 1, 1)
    #         except:
    #             pass

    # def ModificarQuantidade(self, fazer, pagina):
    #
    #     meu_aplicativo = App.get_running_app()
    #
    #     if fazer == 1:
    #         novo_valor = meu_aplicativo.root.ids[pagina]
    #         valor = int(novo_valor.ids["quantidade"].text)
    #         valor = valor + 1
    #         novo_valor.ids["quantidade"].text = f"{valor}"
    #     elif fazer == -1:
    #         novo_valor = meu_aplicativo.root.ids[pagina]
    #         valor = int(novo_valor.ids["quantidade"].text)
    #         if valor > 1:
    #             valor = valor - 1
    #         novo_valor.ids["quantidade"].text = f"{valor}"

    # def Switch_Lista_E_S(self):
    #     tela = self.root.ids["entrada"]
    #     if tela.ids["switch"].active:
    #         BannerProdutosEntrada.Filtrar(self)
    #     else:
    #         BannerProdutosEntrada()

MainApp().run()
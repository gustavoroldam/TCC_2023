import pyautogui
import requests
from pyautogui import alert
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from telas import *
from botoes import *
from myfirebase import MyFirebase
from functools import partial
import json
from BannerProdutos import BannerProdutos

GUI = Builder.load_file("main.kv")


class MainApp(App):
    id_vendedor = None
    nome_Estoque = None

    def build(self):
        self.title = "ESTOQUE"
        self.icon = "../imagens/icones/estoque.png"
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
        requisicao_dic = self.Requisicao_Get(f"https://tcc2023-9212b-default-rtdb.firebaseio.com/Funcionarios/Estoque/{id_Usuario}")
        # Carregar Nome
        nome = requisicao_dic['Nome']
        self.nome_Estoque = nome
        nome_perfil = self.root.ids["homepage"]
        nome_perfil.ids["id_nome_vendedor"].text = f"Estoque {requisicao_dic['Nome']}"
        # Carregar Lista Produtos
        BannerProdutos()

    def realizar_login(self, nome, senha):
        self.id_vendedor = MyFirebase.fazer_login(self, nome, senha)
        if self.id_vendedor != -1 and self.id_vendedor != -2:
            self.carregarInfos(self.id_vendedor)
            self.mudar_tela('homepage')
        elif self.id_vendedor == -2:
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = 'Senha Incorreta'
            pagina_login.ids["erro_login"].color = (1, 0, 0, 1)
        else:
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["erro_login"].text = 'Usuario Incorreto'
            pagina_login.ids["erro_login"].color = (1, 0, 0, 1)

    def bannerprodutos(self, funcao):
        if funcao == 'atualizar':
            BannerProdutos()



MainApp().run()
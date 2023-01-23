from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import pause
import json
from datetime import datetime, timedelta
from credenciais import usuario, senha
from telegram_bot import TelegramBot, TelegramBotErro
from random import randrange
import os
from utils import *
import sys

hora_jogo_atual = None

# & C:/Python39/python.exe c:/Users/anderson.morais/Documents/dev/sportingbet3/app.py 2 5 4 50 1 20 1 2
class ChromeAuto():
    def __init__(self, meta=0, tipo_valor=1, valor_aposta=None, tipo_meta=None, estilo_jogo=None, usa_perda_acumulada=False, numero_jogos_martingale=0, aposta_no_favorito=1, perda_acumulada=0.0):
        self.valor_aposta = valor_aposta
        self.valor_aposta_inicial = valor_aposta
        self.usa_perda_acumulada = usa_perda_acumulada
        self.meta = float(meta)
        self.meta_inicial = float(meta)
        self.saldo = 0
        self.saldo_inicial = 0
        self.saldo_antes_aposta = 0
        self.tipo_valor = tipo_valor
        self.estilo_jogo = estilo_jogo
        self.estilo_rodada = estilo_jogo
        self.tipo_meta = tipo_meta
        self.aposta_fechada = False
        self.telegram_bot = TelegramBot()
        self.telegram_bot_erro = TelegramBotErro()
        self.perda_acumulada = perda_acumulada
        self.controle_frequencia_mensagens = 0
        self.jogos_realizados = 0
        self.hora_jogo = ''
        self.contador_perdas = 0
        self.perdidas_em_sequencia = 0
        self.maior_perdidas_em_sequencia = 0
        self.x_path_odd = None
        self.x_path_clicavel = None
        self.jogos_atuais = []
        self.controla_jogo_acima_abaixo = 0
        self.n_jogos_alerta_sistema_rodando = 10
        self.nome_time = None
        self.numero_jogos_martingale = numero_jogos_martingale
        self.aposta_no_favorito = aposta_no_favorito
        self.primeira_execucao = True
        self.contador_trava_clica_horario_jogo = 0
        self.numero_vitorias = 0
        self.lista_horarios = [ { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '00:23' }, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '00:32'}, \
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora': '00:53'}, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '00:56'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '00:59'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '01:11'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '01:17'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '01:23'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '01:26'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '01:35'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '01:38' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '01:47' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '01:53' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '01:56' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '01:59' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '02:05' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '02:17' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '02:23' },
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '02:38'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '02:44'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '02:50'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '02:53'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '03:02'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '03:05' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '03:14' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '03:20' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '03:23' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '03:26' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '03:32' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '03:44' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '03:50' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '04:17'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '04:26'}, \
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '04:47' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '04:50'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '04:53'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '05:05'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '05:11'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '05:17'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '05:20'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '05:29'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '05:32' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '05:41' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '05:47' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '05:50' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '05:53' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '05:59' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '06:11' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '06:17' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '06:44'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '06:53'},              
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '07:14' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '07:17'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '07:20'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '07:32'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '07:38'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '07:44'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '07:47'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '07:56'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '07:59' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '08:08' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '08:14' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '08:17' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '08:20' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '08:26' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '08:38' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '08:44' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '09:11'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '09:20'}, 
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '09:41' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '09:44'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '09:47'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '09:59'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '10:05'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '10:11'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '10:14'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '10:23'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '10:26' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '10:35' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '10:41' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '10:44' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '10:47' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '10:53' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '11:05' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '11:11' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '11:38'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '11:47'}, 
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '12:08' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '12:11'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '12:14'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '12:26'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '12:32'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '12:38'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '12:41'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '12:50'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '12:53' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '13:02' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '13:08' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '13:11' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '13:14' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '13:20' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '13:32' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '13:38' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '14:05'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '14:14'}, 
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '14:35' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '14:38'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '14:41'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '14:53'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '14:59'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '15:05'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '15:08'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '15:17'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '15:20' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '15:29' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '15:35' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '15:38' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '15:41' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '15:47' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '15:59' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '16:05' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '16:32'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '16:41'}, 
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '17:02' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '17:05'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '17:08'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '17:20'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '17:26'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '17:32'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '17:35'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '17:44'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '17:47' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '17:56' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '18:02' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '18:05' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '18:08' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '18:14' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '18:26' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '18:32' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '18:59'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '19:08'}, 
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '19:29' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '19:32'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '19:35'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '19:47'}, \
            { 'adversario' : 'Irã', 'time': 'EUA', 'hora': '19:53'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '19:59'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '20:02'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '20:11'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '20:14' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '20:23' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '20:29' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '20:32' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '20:35' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '20:41' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '20:53' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '21:05' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '21:11' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '21:23' }, \
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '21:29' },
            { 'adversario' : 'Catar', 'time': 'Senegal', 'hora': '21:56'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Tunísia', 'hora': '22:05'}, 
            { 'adversario' : 'Alemanha', 'time': 'Espanha', 'hora' : '22:26' }, \
            { 'adversario' : 'Sérvia', 'time': 'Camarões', 'hora': '22:29'},
            { 'adversario' : 'Gana', 'time': 'Coreia do Sul - Coreia do Sul', 'hora': '22:32'}, \
            { 'adversario' : 'Senegal', 'time': 'Equador', 'hora': '22:44'}, \
            { 'adversario' : 'Austrália - Austrália', 'time': 'Dinamarca', 'hora': '22:56'}, 
            { 'adversario' : 'Polônia', 'time': 'Argentina', 'hora': '22:59'}, \
            { 'adversario' : 'Marrocos', 'time': 'Canadá', 'hora': '23:08'}, \
            { 'adversario' : 'Japão', 'time': 'Espanha', 'hora' : '23:11' }, \
            { 'adversario' : 'Gana', 'time': 'Uruguai', 'hora' : '23:20' }, \
            { 'adversario' : 'Suiça', 'time': 'Sérvia', 'hora' : '23:26' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '23:29' }, \
            { 'adversario' : 'Equador', 'time': 'Catar', 'hora' : '23:32' }, \
            { 'adversario' : 'Holanda', 'time': 'Senegal', 'hora' : '23:38' }, \
            { 'adversario' : 'Polônia', 'time': 'México', 'hora' : '23:50' },
            { 'adversario' : 'Marrocos', 'time': 'Croácia', 'hora' : '23:56' },]
        return

    def acessa(self, site):         
        self.driver_path = 'chromedriver'
        self.options = webdriver.ChromeOptions()
        self.chrome = webdriver.Chrome(self.driver_path)     
        self.chrome.get(site)
        self.chrome.maximize_window()

    def sair(self):
        self.chrome.quit()

    def clica_sign_in(self):
        sleep(2)
        try:
            elem = WebDriverWait(self.chrome, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="https://www.sportingbet.com/pt-br/labelhost/login"]' )  )) 
            elem.click()
        except Exception as e:
            print(e)

    def faz_login(self):
        try:
            input_login = WebDriverWait(self.chrome, 10).until(
                EC.element_to_be_clickable((By.ID, 'userId' )  )) 
            input_login.send_keys(usuario)         
            
            input_password = WebDriverWait(self.chrome, 10).until(
                EC.element_to_be_clickable((By.NAME, 'password' )  )) 
            input_password.send_keys(senha)

            remember_me = WebDriverWait(self.chrome, 10).until(
                EC.element_to_be_clickable((By.ID, 'rememberMe' )  ))
            remember_me.click()

            botao_login = WebDriverWait(self.chrome, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="login w-100 btn btn-primary"]' )  )) 
            sleep(2)
            botao_login.click()

            sleep(2)

            self.le_saldo()
            print(f'SALDO ATUAL: {self.saldo}')

            # saldo inicial não pode ser alterado ao longo de toda uma rodada     
            self.saldo_inicial = self.saldo

            self.atualiza_meta_e_valor_aposta()
            self.telegram_bot.envia_mensagem(f'SALDO ATUAL: {self.saldo}\nVALOR POR APOSTA: {self.valor_aposta:.2f}\nMETA: { self.meta:.2f}')
            self.primeira_execucao = False

            print(f'VALOR POR APOSTA: {self.valor_aposta:.2f}')        
            print(f'META: { self.meta:.2f}')            

            virtuais = WebDriverWait(self.chrome, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//*[normalize-space(text()) = 'Virtuais']/ancestor::a" ) )) 
            virtuais.click() 

            sleep(2)

            cookies = WebDriverWait(self.chrome, 20).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler' ) )) 
            cookies.click() 
        except Exception as e:
            print(e)

    def atualiza_meta_e_valor_aposta(self):
        ''' tanto a meta quanto o valor são percentuais '''
        if self.tipo_meta == TipoMeta.PORCENTAGEM:
            self.meta = self.saldo + self.saldo * ( self.meta_inicial / 100 )
        elif self.tipo_meta == TipoMeta.SALDO_MAIS_META:
            self.meta = self.saldo_inicial + self.meta_inicial
        elif self.tipo_meta == TipoMeta.SALDO_MAIS_VALOR:
            self.meta = self.saldo_inicial + self.meta_inicial

        if self.tipo_valor == TipoValorAposta.PORCENTAGEM:
            self.valor_aposta = self.saldo * ( self.valor_aposta_inicial / 100 )           

        if self.valor_aposta < 2.0:
            self.valor_aposta = 2.0

    def clica_horario_jogo(self, horario_jogo):     
        self.aposta_fechada = False
        self.estilo_rodada = self.estilo_jogo
        try: 
            horario = WebDriverWait(self.chrome, 5).until(
                    EC.element_to_be_clickable((By.XPATH, horario_jogo)))      
            horario.click()
            sleep(2)
            horario.click()
            sleep(2)
            self.contador_trava_clica_horario_jogo = 0
        except Exception:
            self.contador_trava_clica_horario_jogo += 1
            if self.contador_trava_clica_horario_jogo > 5:
                #vou tentar clicar pra fechar o modal que apareceu
                try:
                    modal = WebDriverWait(self.chrome, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-multi-slot[2]/lh-rtms-layer/div/div/div/div/lh-rtms-layer-custom-overlay/div/lh-header-bar/vn-header-bar/div/div/div[3]/span/ancestor::div' ) )) 
                    modal.click()
                except Exception:
                    try:
                        modal = WebDriverWait(self.chrome, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-multi-slot[2]/lh-rtms-layer/div/div/div/div/lh-rtms-layer-custom-overlay/div/lh-header-bar/vn-header-bar/div/div/div[3]' ) )) 
                        modal.click() 
                    except Exception:
                        # se ainda assim car na exceptino eu envio a mensagem    
                        self.telegram_bot_erro.envia_mensagem("SISTEMA TRAVADO NO CLICA HORÁRIO JOGO.")
                        self.contador_trava_clica_horario_jogo = 0
                        self.hora_jogo = input("INSIRA O HORÁRIO ATUALIZADO DO PRÓXIMO JOGO:")
            self.aposta_fechada = True
            sleep(10)                                              

    def analisa_odds(self):
        try: 
            resultado_partida = WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[normalize-space(text()) = 'Resultado da partida']") )) 

            odd_casa = WebDriverWait(self.chrome, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[1]/div/div/div/div/ms-main-column/div/ms-virtual-list/ms-virtual-fixture/div/ms-option-group-list/div[1]/ms-option-panel[1]/ms-regular-group/ms-regular-option-group/div/ms-option[1]/ms-event-pick/div/div[2]') )) 

            odd_casa = odd_casa.get_property('innerText')
            odd_empate = WebDriverWait(self.chrome, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[1]/div/div/div/div/ms-main-column/div/ms-virtual-list/ms-virtual-fixture/div/ms-option-group-list/div[1]/ms-option-panel[1]/ms-regular-group/ms-regular-option-group/div/ms-option[2]/ms-event-pick/div/div[2]') )) 

            odd_empate = odd_empate.get_property('innerText')
            odd_fora = WebDriverWait(self.chrome, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[1]/div/div/div/div/ms-main-column/div/ms-virtual-list/ms-virtual-fixture/div/ms-option-group-list/div[1]/ms-option-panel[1]/ms-regular-group/ms-regular-option-group/div/ms-option[3]/ms-event-pick/div/div[2]') )) 

            odd_fora = odd_fora.get_property('innerText')

            odd_casa = float(odd_casa)
            odd_empate = float(odd_empate)
            odd_fora = float(odd_fora)
            odd_jogo = 0

            if odd_casa >= 4 and odd_casa >= odd_fora:
                odd_jogo = odd_casa
                aposta_casa = WebDriverWait(self.chrome, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[1]/div/div/div/div/ms-main-column/div/ms-virtual-list/ms-virtual-fixture/div/ms-option-group-list/div[1]/ms-option-panel[1]/ms-regular-group/ms-regular-option-group/div/ms-option[1]' ) )) 
                aposta_casa.click()
            elif odd_fora >= 4 and odd_fora >= odd_casa:
                aposta_fora = WebDriverWait(self.chrome, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[1]/div/div/div/div/ms-main-column/div/ms-virtual-list/ms-virtual-fixture/div/ms-option-group-list/div[1]/ms-option-panel[1]/ms-regular-group/ms-regular-option-group/div/ms-option[3]' ) )) 
                aposta_fora.click()
                odd_jogo = odd_fora
            elif odd_casa == odd_fora and odd_casa >= 4:
                odd_jogo = odd_casa
                aposta_casa = WebDriverWait(self.chrome, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[1]/div/div/div/div/ms-main-column/div/ms-virtual-list/ms-virtual-fixture/div/ms-option-group-list/div[1]/ms-option-panel[1]/ms-regular-group/ms-regular-option-group/div/ms-option[1]' ) )) 
                aposta_casa.click()

            if odd_jogo != 0:
                if self.tipo_valor == TipoValorAposta.PORCENTAGEM:
                    self.valor_aposta = ( self.saldo_inicial * self.valor_aposta_inicial / 100 + self.perda_acumulada ) / ( odd_jogo - 1.00 )
                elif self.tipo_valor == TipoValorAposta.VALOR_ABSOLUTO:
                    self.valor_aposta = ( self.valor_aposta_inicial + self.perda_acumulada ) / ( odd_jogo - 1.00 )

                if self.valor_aposta < 2.0:
                    self.valor_aposta = 2.0

                if self.valor_aposta > self.saldo:
                    print('VALOR DA APOSTA É MAIOR DO QUE O SALDO.')
                    self.telegram_bot_erro.envia_mensagem('VALOR DA APOSTA É MAIOR DO QUE O SALDO.')

                    while self.valor_aposta > self.saldo:
                        sleep(1800)
                        self.le_saldo()
                    self.aposta_fechada = True

                print(f'PERDA ACUMULADA: {self.perda_acumulada:.2f} R$')
                print(f'VALOR DA APOSTA: {self.valor_aposta:.2f} R$')                    
                print(f'GANHO POTENCIAL: {(self.valor_aposta * odd_jogo):.2f} R$')
                print(f'GANHO POTENCIAL REAL: {(self.valor_aposta * odd_jogo - self.valor_aposta):.2f} R$') 
            else:
                self.aposta_fechada = True
        except Exception as e:
            print("APOSTA JÁ FECHADA...")
            print(e)
            self.aposta_fechada = True

    def insere_valor(self):
        contador_travamento = 0
        while True:         
            contador_travamento += 1
            try:
                input_valor = WebDriverWait(self.chrome, 20).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[2]/div/div/div/div/ms-widget-column/ms-widget-slot/ms-bet-column/ms-betslip-component/div/div[2]/div/ms-betslip-stakebar/div/div/span/ms-stake/div/ms-stake-input/div/input') )) 
                sleep(2)
                input_valor.clear()
                input_valor.send_keys(f'{self.valor_aposta:.2f}')
            except Exception as e:
                print(e)
           
            sleep(2)

            try:
                botao_aposta = WebDriverWait(self.chrome, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[2]/div/div/div/div/ms-widget-column/ms-widget-slot/ms-bet-column/ms-betslip-component/div/div[2]/div/div/ms-betslip-action-button/div/button' ) )) 
                botao_aposta.click()     

                sleep(2) 

                botao_fechar = WebDriverWait(self.chrome, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[2]/div/div/div/div/ms-widget-column/ms-widget-slot/ms-bet-column/ms-betslip-component/div/div/div/div/button' ) )) 
                botao_fechar.click() 

                self.le_saldo()

                print(f'SALDO ATUAL: {self.saldo}')
                print(f'META: {self.meta:.2f}')

                numero_apostas_abertas = self.chrome.execute_script(f'let d = await fetch("https://sports.sportingbet.com/pt-br/sports/api/mybets/betslips?index=1&maxItems=12&typeFilter=2"); return await d.json();')
                numero_apostas_abertas = numero_apostas_abertas['summary']['openBetsCount']

                print('NÚMERO DE APOSTAS ABERTAS: ', numero_apostas_abertas)

                if numero_apostas_abertas > 0:
                    self.jogos_realizados += 1
                    if self.jogos_realizados % self.n_jogos_alerta_sistema_rodando == 0:
                        self.telegram_bot.envia_mensagem('SISTEMA AINDA RODANDO...')                    
                    return

                if contador_travamento == 10:
                    self.telegram_bot_erro.envia_mensagem(f'SISTEMA POSSIVELMENTE TRAVADO NO INSERE VALOR!!!')

            except Exception as e:
                lixeira = WebDriverWait(self.chrome, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[2]/div/div/div/div/ms-widget-column/ms-widget-slot/ms-bet-column/ms-betslip-component/div/div[1]/div[1]/ms-betslip-picks/div[2]/ms-betslip-remove-all-picks/div/div' ) )) 
                lixeira.click()
                confirmacao_exclusao = WebDriverWait(self.chrome, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[2]/div/div/div/div/ms-widget-column/ms-widget-slot/ms-bet-column/ms-betslip-component/div/div[1]/div[1]/ms-betslip-picks/div[2]/ms-betslip-remove-all-picks/div' ) )) 
                confirmacao_exclusao.click()
                print(e)

    def le_saldo(self):        
        leu_saldo = False
        contador_de_trava = 0
        while not leu_saldo:
            sleep(10)
            try:
                saldo_request = self.chrome.execute_script(f'let d = await fetch("https://sports.sportingbet.com/pt-br/api/balance/refresh"); return await d.json();')
                self.saldo = saldo_request['vnBalance']['accountBalance']
                leu_saldo = True
                sleep(10)
            except Exception as e:
                print(e)
                contador_de_trava += 1
                if contador_de_trava >= 10:
                    self.telegram_bot_erro.envia_mensagem('SISTEMA POSSIVELMENTE TRAVADO AO LER SALDO.')
                    self.chrome.refresh()
                print('Não foi possível ler saldo. Tentando de novo...')
    
    def seleciona_indice_jogo(self):
        indice = 0

        hora_atual = datetime.today()

        for horario in self.lista_horarios:
            hora = int(horario.get('hora').split(':')[0])
            minuto = int(horario.get('hora').split(':')[1])
            now = datetime.today()  
            hora_do_jogo = datetime( now.year, now.month, now.day, hora, minuto, 0 )

            if hora_do_jogo > hora_atual:
                return indice
            else:
                indice += 1

    def define_hora_jogo(self, hora_jogo_atual):
        hora = int(hora_jogo_atual.split(':')[0])
        minuto = int(hora_jogo_atual.split(':')[1])
        now = datetime.today()  
        hora_do_jogo = datetime( now.year, now.month, now.day, hora, minuto, 0)
        hora_jogo_atual_datetime = hora_do_jogo + timedelta(minutes=3)
        hora_jogo_atual =  hora_jogo_atual_datetime.strftime("%H:%M")

        if hora_jogo_atual == '20:56':
            hora_jogo_atual = '21:05'
            self.hora_jogo = '21:05'
            return hora_jogo_atual

        self.hora_jogo = hora_jogo_atual
        return hora_jogo_atual

    def espera_resultado_jogo_sem_aposta(self):
        print('HORÁRIO', self.hora_jogo )
        print('Esperando resultado da partida sem aposta...')

        hora = int(self.hora_jogo.split(':')[0])
        minuto = int(self.hora_jogo.split(':')[1])
        now = datetime.today()  
        hora_do_jogo = datetime( now.year, now.month, now.day, hora, minuto, 0)

        pause.until( hora_do_jogo + timedelta(minutes=1, seconds=20)  )
    
    def espera_resultado_jogo(self):
        print('Entrou no espera_resultado_jogo')

        try:
            print('HORÁRIO', self.hora_jogo )
            print('Esperando resultado da partida...')
            hora = int(self.hora_jogo.split(':')[0])
            minuto = int(self.hora_jogo.split(':')[1])
            now = datetime.today()  
            hora_do_jogo = datetime( now.year, now.month, now.day, hora, minuto, 0)

            self.le_saldo()
            self.saldo_antes_aposta = self.saldo

            pause.until( hora_do_jogo + timedelta(minutes=1, seconds=20)  )

            numero_apostas_abertas = self.chrome.execute_script(f'let d = await fetch("https://sports.sportingbet.com/pt-br/sports/api/mybets/betslips?index=1&maxItems=1&typeFilter=2"); return await d.json();')
            numero_apostas_abertas = numero_apostas_abertas['summary']['openBetsCount']

            contador_de_trava = 0

            # enquanto a aposta não for liquidada o script vai ficar buscando aqui
            while numero_apostas_abertas == 1:
                numero_apostas_abertas = self.chrome.execute_script(f'let d = await fetch("https://sports.sportingbet.com/pt-br/sports/api/mybets/betslips?index=1&maxItems=1&typeFilter=2"); return await d.json();')
                numero_apostas_abertas = numero_apostas_abertas['summary']['openBetsCount']
                contador_de_trava += 1
                if contador_de_trava == 10:
                    self.telegram_bot_erro.envia_mensagem(f'SISTEMA POSSIVELMENTE TRAVADO AO ESPERAR RESULTADO DA APOSTA!!!')
                sleep(5)

            # agora verifico se o horário da partida é igual a self.hora_jogo
            horario_ultima_aposta = self.chrome.execute_script(f'let d = await fetch("https://sports.sportingbet.com/pt-br/sports/api/mybets/betslips?index=1&maxItems=1&typeFilter=2"); return await d.json();')
            horario_ultima_aposta_texto = horario_ultima_aposta['betslips'][0]['bets'][0]['fixture']['date']
            horario_ultima_aposta_texto = horario_ultima_aposta_texto.replace('Z', '')
            horario_ultima_aposta_texto = datetime.strptime( horario_ultima_aposta_texto, '%Y-%m-%dT%H:%M:%S') 
            horario_ultima_aposta_texto = ( horario_ultima_aposta_texto - timedelta(hours=3) ).strftime("%H:%M")

            contador_de_trava = 0

            # enquanto for diferente é porque a última aposta não saiu
            while horario_ultima_aposta_texto != self.hora_jogo:
                horario_ultima_aposta = self.chrome.execute_script(f'let d = await fetch("https://sports.sportingbet.com/pt-br/sports/api/mybets/betslips?index=1&maxItems=1&typeFilter=2"); return await d.json();')
                horario_ultima_aposta_texto = horario_ultima_aposta['betslips'][0]['bets'][0]['fixture']['date']
                horario_ultima_aposta_texto = horario_ultima_aposta_texto.replace('Z', '')
                horario_ultima_aposta_texto = datetime.strptime( horario_ultima_aposta_texto, '%Y-%m-%dT%H:%M:%S') 
                horario_ultima_aposta_texto = ( horario_ultima_aposta_texto - timedelta(hours=3) ).strftime("%H:%M")
                contador_de_trava += 1
                if contador_de_trava == 10:
                    self.telegram_bot_erro.envia_mensagem(f'SISTEMA POSSIVELMENTE TRAVADO AO ESPERAR RESULTADO DA PARTIDA!!!')
                sleep(5)
            
            print('JÁ SAIU RESULTADO')
            # agora vamos conferir se foi favorável ou não              

            contador_de_trava = 0

            self.le_saldo()

            if horario_ultima_aposta['betslips'][0]['state'] == 'Won':
                # se tiver ganhado, vai buscar o saldo até que o mesmo esteja atualizado
                while self.saldo <= self.saldo_antes_aposta:
                    print('SALDO ATUALIZADO?', self.saldo > self.saldo_antes_aposta)
                    self.le_saldo()
                    sleep(5)

                    contador_de_trava += 1
                    if contador_de_trava == 10:
                        self.telegram_bot_erro.envia_mensagem(f'SISTEMA POSSIVELMENTE TRAVADO AO ATUALIZAR SALDO!!!')
                print('GANHOU.')
                self.perdidas_em_sequencia = 0
                self.numero_vitorias += 1
            else:
                self.perdidas_em_sequencia += 1
                if self.maior_perdidas_em_sequencia < self.perdidas_em_sequencia:
                    self.maior_perdidas_em_sequencia = self.perdidas_em_sequencia
                print('PERDEU.')

            print(f'SALDO ATUAL: {self.saldo}')

            # significa que perdemos, então vamos adicionar a perda ao valor acumulado
            if self.saldo <= self.saldo_antes_aposta:
                if self.usa_perda_acumulada:
                    self.perda_acumulada += self.valor_aposta
                else:
                    self.perda_acumulada = 0.0
                self.contador_perdas += 1
            # significa que recuperamos o valor perdido, então zeramos a perda acumulada
            elif self.saldo > self.saldo_antes_aposta:
                self.perda_acumulada = 0.0
                self.contador_perdas = 0
                
            if self.saldo_inicial < self.saldo:
                self.saldo_inicial = self.saldo
                self.telegram_bot_erro.envia_mensagem(f'GANHOU! SALDO: R$ {self.saldo}')

            if self.usa_perda_acumulada:
                if self.perdidas_em_sequencia == self.numero_jogos_martingale:
                    self.perda_acumulada = 0.0
                    self.perdidas_em_sequencia = 0
            else:
                self.perda_acumulada = 0.0

            if self.tipo_meta == TipoMeta.NUMERO_VITORIAS:
                if self.numero_vitorias == self.meta:
                    print('PARABÉNS! VOCÊ ATINGIU SUA META!')
                    self.telegram_bot_erro.envia_mensagem(f'PARABÉNS! VOCÊ ATINGIU SUA META! SEU SALDO É: R$ {self.saldo}\nMAIOR SEQUÊNCIA DE PERDAS: {self.maior_perdidas_em_sequencia}')
                    print(f'MAIOR SEQUÊNCIA DE PERDAS: {self.maior_perdidas_em_sequencia}')
                    if ao_atingir_meta == AoAtingirMeta.FECHAR_APLICATIVO:
                        self.chrome.quit()
                        exit(0)
                    elif ao_atingir_meta == AoAtingirMeta.DESLIGAR_COMPUTADOR:
                        return os.system("shutdown /s /t 1")
                    elif ao_atingir_meta == AoAtingirMeta.CONTINUAR_APOSTANDO:
                        self.maior_perdidas_em_sequencia = 0
                else:
                    print('META NÃO ATINGIDA. KEEP GOING.')
            else: 
                if self.saldo >= self.meta - 0.5:
                    print('PARABÉNS! VOCÊ ATINGIU SUA META!')
                    self.telegram_bot_erro.envia_mensagem(f'PARABÉNS! VOCÊ ATINGIU SUA META! SEU SALDO É: R$ {self.saldo}\nMAIOR SEQUÊNCIA DE PERDAS: {self.maior_perdidas_em_sequencia}')
                    print(f'MAIOR SEQUÊNCIA DE PERDAS: {self.maior_perdidas_em_sequencia}')
                    if ao_atingir_meta == AoAtingirMeta.FECHAR_APLICATIVO:
                        self.chrome.quit()
                        exit(0)
                    elif ao_atingir_meta == AoAtingirMeta.DESLIGAR_COMPUTADOR:
                        return os.system("shutdown /s /t 1")
                    elif ao_atingir_meta == AoAtingirMeta.CONTINUAR_APOSTANDO:
                        #self.atualiza_meta_e_valor_aposta()
                        self.maior_perdidas_em_sequencia = 0
                    else:
                        print('META NÃO ATINGIDA. KEEP GOING.')
                    self.controle_frequencia_mensagens += 1

        except Exception as e:
            print(e)
            print('Algo saiu errado no espera_resultado')        
        
if __name__ == '__main__':


    print('COMO QUER ESTABELECER O VALOR DA APOSTA?')
    print('(1) PORCENTAGEM DO SALDO (2) VALOR ABSOLUTO')

    tipo_valor = int(sys.argv[1]) if len(sys.argv) > 1 else int(input())
    
    print('INSIRA O VALOR DESEJADO DAS APOSTAS')
    valor_aposta = float(sys.argv[2]) if len(sys.argv) > 2 else float(input())
    
    print('COMO QUER ESTABELECER A META?')
    print('(1) PORCENTAGEM DO SALDO (2) VALOR ABSOLUTO (3) SALDO ATUAL MAIS META (4) SALDO ATUAL MAIS VALOR (5) NÚMERO DE VITÓRIAS')

    tipo_meta = int(sys.argv[3]) if len(sys.argv) > 3 else int(input())
    print('INSIRA O VALOR DA META')
    meta = float(sys.argv[4]) if len(sys.argv) > 4 else float(input())

    print('QUER USAR A PERDA ACUMULADA? (1) SIM (2) NÃO')
    usa_perda_acumulada = int(sys.argv[5]) if len(sys.argv) > 5 else int(input())
    if usa_perda_acumulada == 1:
        usa_perda_acumulada = True
    else:
        usa_perda_acumulada = False

    numero_jogos_martingale = 0
    if usa_perda_acumulada:
        print('ATÉ QUANTAS PERDAS QUER USAR O MARTINGALE?')
        numero_jogos_martingale = int(sys.argv[6]) if len(sys.argv) > 6 else int(input())

    print('O QUE DESEJA FAZER AO ATINGIR A META?')
    print('(1) FECHAR O APLICATIVO')
    print('(2) DESLIGAR O COMPUTADOR')
    print('(3) RECALCULAR META E CONTINUAR APOSTANDO')
    ao_atingir_meta = int(sys.argv[7]) if len(sys.argv) > 7 else int(input())      

    print('APOSTAR NO FAVORITO OU NO ADVERSÁRIO? (1) FAVORITO (2) ADVERSÁRIO')
    aposta_no_favorito = int(sys.argv[8]) if len(sys.argv) > 8 else int(input())
    if aposta_no_favorito == 1:
        aposta_no_favorito = True
    else:
        aposta_no_favorito = False

    perda_acumulada = float(sys.argv[9]) if len(sys.argv) > 9 else int(input())

    chrome = ChromeAuto(meta=meta, tipo_valor=tipo_valor, valor_aposta=valor_aposta, tipo_meta=tipo_meta, usa_perda_acumulada=usa_perda_acumulada, numero_jogos_martingale=numero_jogos_martingale, aposta_no_favorito=aposta_no_favorito, perda_acumulada=perda_acumulada )
    chrome.acessa('https://www.sportingbet.com/pt-br/labelhost/login')        
    chrome.faz_login()  

    horario_jogo = '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[1]/div/div/div/div/ms-main-column/div/ms-virtual-list/ms-virtual-fixture/div/ms-tab-bar/ms-scroll-adapter/div/div/ul/li[2]/a'

    primeiro_horario = chrome.chrome.find_element(By.XPATH, horario_jogo + '/descendant::*')
    hora_jogo_atual = primeiro_horario.get_property('innerText')
    chrome.hora_jogo = hora_jogo_atual

    while True:
        chrome.clica_horario_jogo(f"//*[normalize-space(text()) = '{ hora_jogo_atual }']")
        if not chrome.aposta_fechada:
            chrome.analisa_odds()
            if not chrome.aposta_fechada:
                chrome.insere_valor()
                chrome.espera_resultado_jogo()
            else:
                chrome.espera_resultado_jogo_sem_aposta()
        else:
            chrome.espera_resultado_jogo_sem_aposta()


        hora_jogo_atual = chrome.define_hora_jogo(chrome.hora_jogo)
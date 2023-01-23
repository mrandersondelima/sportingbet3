import os
from dotenv import load_dotenv

load_dotenv()

usuario = os.getenv('USUARIO')
senha = os.getenv('SENHA')
token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
token_id_erro = os.getenv('BOT_TOKEN_ERRO')
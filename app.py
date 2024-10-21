from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import base64
import os  # Adicione esta linha
from dotenv import load_dotenv
from perguntas import registrar_rotas

load_dotenv()  # Carrega as variáveis de ambiente do .env

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

cursor = conn.cursor()
conn.autocommit = True

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  

@app.route('/')
def home():
    return "teste"

registrar_rotas(app, cursor)

# if __name__ == '__main__':
#     app.run(debug=True)
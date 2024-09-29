from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os  # Adicione esta linha
from dotenv import load_dotenv

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
CORS(app)

@app.route('/')
def home():
    return "teste"

@app.route('/perguntas')
def getperguntas():
    cursor.execute("SELECT * FROM perguntas")
    perguntas = list()
    for pergunta in cursor.fetchall():
        perguntas.append({
            'codigo': pergunta[0],
            'descricao': pergunta[1],
            'imagem': pergunta[2].hex()
        })
    print(perguntas)
    
    return perguntas

def adicionarPergunta(data): 
    cursor.execute("INSERT INTO public.perguntas (pg_descricao, pg_imagem) VALUES(%s, decode(%s,'hex'))", data)

@app.route('/perguntas', methods=['POST'])
def cadastrarPergunta():
    adicionarPergunta((
        request.json.get('descricao'),
        request.json.get('imagem')
    ))
    return jsonify({'message': 'Pergunta cadastrada com sucesso!'}), 201


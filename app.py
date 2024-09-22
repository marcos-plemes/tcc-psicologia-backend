from flask import Flask
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

@app.route('/')
def home():
    cursor.execute("SELECT * FROM perguntas")
    perguntas = list()
    for pergunta in cursor.fetchall():
        perguntas.append({
            'codigo': pergunta[0],
            'descricao': pergunta[1]
        })
    print(perguntas)
    
    return perguntas

if __name__ == '__main__':
    app.run(debug=True)

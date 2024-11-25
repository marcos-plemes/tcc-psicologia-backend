from flask import request, jsonify
import json

import base64

def registrar_rotas_respostas(app, cursor):
    @app.route('/respostas/<int:grupo>', methods=['POST'])
    def cadastrarRespostas(grupo):
        try:
            cursor.execute("INSERT INTO participante (pa_grupo) VALUES (%s) RETURNING pa_codigo", (grupo,))
            participante = cursor.fetchone()[0]
            print(participante)
            cursor.execute(""" 
INSERT INTO resposta (re_configuracao,
                      re_participante)
	VALUES (%s,
            %s)
RETURNING re_codigo                           
""",
(
    json.dumps(request.json['configuracaoUsada']),
    participante
))
            resposta = cursor.fetchone()[0]

            for item_resposta in request.json['respostas']:
                print(item_resposta)
                cursor.execute(""" 
INSERT INTO resposta_item (rei_resposta,
                           rei_descricao,
                           rei_inicio,
                           rei_fim)
	VALUES (%s,
            %s,
            %s,
            %s)                           
""",
(
    resposta,
    item_resposta['resposta'],
    item_resposta['inicio'],
    item_resposta['fim']
))

            return jsonify({'message': 'Respostas cadastradas com sucesso!'}), 201    
        except:
            return jsonify({"error": str(e)}), 500
    
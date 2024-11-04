from flask import request, jsonify
import base64

def registrar_rotas_respostas(app, cursor):
    @app.route('/respostas/<int:grupo>', methods=['POST'])
    def cadastrarRespostas(grupo):
        
        try:
            cursor.execute("INSERT INTO participante (pa_grupo) VALUES (8) RETURNING pa_codigo", (grupo,))
            participante = cursor.fetchone()[0]
        
            for resposta in request.json:
                cursor.execute(""" 
INSERT INTO resposta (re_resposta,
                      re_inicio,
                      re_fim,
                      re_participante)
	VALUES (%s,
            %s,
            %s,
            %s)
""",
(
    resposta['resposta'],
    resposta['inicio'],
    resposta['fim'],
    participante
))

            return jsonify({'message': 'Respostas cadastradas com sucesso!'}), 201    
        except:
            return jsonify({"error": str(e)}), 500
    
from flask import request, jsonify
import base64

def registrar_rotas(app, cursor):
    @app.route('/perguntas/<int:codigo>', methods=['DELETE'])
    def deletarPergunta(codigo):
        cursor.execute("DELETE FROM perguntas WHERE pg_codigo = %s", (codigo,))
        return jsonify({'message': 'Pergunta deletada com sucesso!'}), 200

    @app.route('/perguntas/<int:codigo>', methods=['GET'])
    def get_pergunta(codigo):
        cursor.execute("SELECT * FROM perguntas WHERE pg_codigo = %s", (codigo,))
        pergunta = cursor.fetchone()  

        if pergunta:
            return jsonify({
                'codigo': pergunta[0],
                'descricao': pergunta[1],
                'imagem': f"data:image/jpeg;base64,{base64.b64encode(pergunta[2]).decode('utf-8')}"
            })
        else:
            return jsonify({'message': 'Pergunta não encontrada'}), 404

    @app.route('/perguntas')
    def getperguntas():
        cursor.execute("SELECT pg_codigo, pg_descricao FROM perguntas")
        perguntas = list()
        for pergunta in cursor.fetchall():
            perguntas.append({
                'codigo': pergunta[0],
                'descricao': pergunta[1]
            })
    
        return perguntas

    @app.route('/perguntas', methods=['POST'])
    def cadastrarPergunta():
        if 'imagem' not in request.files:
            return jsonify({"error": "Nenhuma imagem enviada"}), 400
        if request.files['imagem'].filename == '':
            return jsonify({"error": "Nenhuma imagem selecionada"}), 400
    
        imagem = request.files['imagem']
    
        try:
            imagem_binaria = imagem.read()
            cursor.execute("INSERT INTO public.perguntas (pg_descricao, pg_imagem) VALUES(%s, %s) RETURNING pg_codigo",
                        (request.form['descricao'],
                            imagem_binaria))
        
            codigo = cursor.fetchone()[0]
            return jsonify({
                'message': 'Pergunta cadastrada com sucesso!',
                'codigo': codigo
                }), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/perguntas', methods=['PUT'])
    def alterarPergunta():    
        codigo = request.form['codigo']
        print(request.form)
        if codigo == '':
            return jsonify({"error": "Código não informado"}), 400
    
        try:
        
            if 'imagem' in request.files and request.files['imagem'].filename != '' and request.form['descricao'] != '':
                imagem = request.files['imagem']    
                imagem_binaria = imagem.read()
                cursor.execute("UPDATE perguntas SET pg_descricao= %s, pg_imagem= %s WHERE pg_codigo= %s;", 
                               (request.form['descricao'],
                                imagem_binaria,
                                codigo))    
        
            if 'imagem' in request.files and request.files['imagem'].filename != '' and request.form['descricao'] == '':
                imagem = request.files['imagem']    
                imagem_binaria = imagem.read()
                cursor.execute("UPDATE perguntas SET pg_imagem= %s WHERE pg_codigo= %s;", 
                               (imagem_binaria,
                                codigo))
        
            if 'imagem' not in request.files and request.form['descricao'] != '':
                cursor.execute("UPDATE perguntas SET pg_descricao= %s WHERE pg_codigo= %s;", 
                               (request.form['descricao'],
                                codigo))  
              
            return jsonify({'message': 'Pergunta alterada com sucesso!'}), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
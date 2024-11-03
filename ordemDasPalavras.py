from flask import request, jsonify
import base64

def registrar_rotas_ordem_da_palavra(app, cursor):
    @app.route('/ordem-das-palavras')
    def getLista():
        cursor.execute("SELECT op_codigo,op_descricao,op_quantidade,op_mostar_imagem_correspondente_a_palavra FROM ordem_da_palavra ORDER BY op_descricao")
        ordemDasPalavras = list()
        for ordemDaPalavra in cursor.fetchall():
            ordemDasPalavras.append({
                'codigo': ordemDaPalavra[0],
                'descricao': ordemDaPalavra[1],
                'quantidadeDePalavras': ordemDaPalavra[2],
                'isMostrarImagemCorrespondenteAPalavra': ordemDaPalavra[3]
            })
    
        return ordemDasPalavras
    
    @app.route('/ordem-das-palavras/<int:codigo>', methods=['GET'])
    def getPorCodigo(codigo):
        cursor.execute("SELECT op_codigo,op_descricao,op_quantidade,op_mostar_imagem_correspondente_a_palavra FROM ordem_da_palavra WHERE op_codigo = %s", (codigo,))
        ordemDaPalavra = cursor.fetchone()  

        if ordemDaPalavra:
            return jsonify({
                'codigo': ordemDaPalavra[0],
                'descricao': ordemDaPalavra[1],
                'quantidadeDePalavras': ordemDaPalavra[2],
                'isMostrarImagemCorrespondenteAPalavra': ordemDaPalavra[3]
            })
        else:
            return jsonify({'message': 'Ordem da Palavra não encontrada'}), 404    
        
    @app.route('/ordem-das-palavras', methods=['POST'])
    def cadastrar():
        try:
            cursor.execute("""INSERT INTO ordem_da_palavra (op_descricao,
                                                            op_quantidade,
                                                            op_mostar_imagem_correspondente_a_palavra) VALUES (%s, %s, %s) 
                           RETURNING op_codigo""",
                        (request.form['descricao'],
                         request.form['quantidadeDePalavras'],
                         request.form['isMostrarImagemCorrespondenteAPalavra']))
        
            codigo = cursor.fetchone()[0]
            return jsonify({
                'message': 'Ordem da Palavra cadastrada com sucesso!',
                'codigo': codigo
                }), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/ordem-das-palavras', methods=['PUT'])
    def alterar():
        codigo = request.form['codigo']
        if codigo == '':
            return jsonify({"error": "Código não informado"}), 400
        try:
            cursor.execute("""UPDATE public.ordem_da_palavra 
                                 SET op_descricao=%s,
                                     op_quantidade=%s,
                                     op_mostar_imagem_correspondente_a_palavra=%s 
                               WHERE op_codigo=%s;""",
                        (request.form['descricao'],
                         request.form['quantidadeDePalavras'],
                         request.form['isMostrarImagemCorrespondenteAPalavra'],
                         codigo))
            
            return jsonify({'message': 'Ordem da Palavra Alterado com sucesso!'}), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500        
        
    @app.route('/ordem-das-palavras/<int:codigo>', methods=['DELETE'])
    def deletar(codigo):
        cursor.execute("DELETE FROM ordem_da_palavra WHERE op_codigo = %s", (codigo,))
        return jsonify({'message': 'Ordem da Palavra deletada com sucesso!'}), 200        
    
    @app.route('/ordem-das-palavras/<int:codigo>/itens', methods=['GET'])
    def buscarItens(codigo):
        cursor.execute("""
SELECT opi.opi_codigo,
       opi.opi_ordem_da_palavra,                
       opi.opi_ordem,
       
       opi.opi_palavra_texto,
       opi.opi_quantidade_da_palavra,
       opi.opi_tempo_da_palavra,
       opi.opi_intervalo_da_palavra,
       
       opi.opi_palavra_imagem,
       opi.opi_quantidade_da_imagem,
       opi.opi_tempo_da_imagem,
       opi.opi_intervalo_da_imagem
  FROM ordem_da_palavra_item opi
     WHERE opi.opi_ordem_da_palavra = %s
  ORDER BY opi.opi_ordem                            
""", (codigo,))
        
        itens = list()
        for item in cursor.fetchall():
            itens.append({
                'codigo': item[0],
                'ordemDaPalavra': item[1],
                'ordem': item[2],

                'codigoDaPalavraTexto': item[3],
                'quantidadeDaPalavraTexto': item[4],
                'tempoDaPalavraTexto': item[5],
                'intervaloDaPalavraTexto': item[6],

                'codigoDaPalavraImagem': item[7],
                'quantidadeDaPalavraImagem': item[8],
                'tempoDaPalavraImagem': item[9],
                'intervaloDaPalavraImagem': item[10],
            })

        return itens
    
    @app.route('/ordem-das-palavras/<int:codigo>/itens', methods=['PUT'])
    def alterarItens(codigo):    
        try:
            for item in request.json:
                cursor.execute(""" 
UPDATE ordem_da_palavra_item
	SET opi_palavra_texto=%s,
	    opi_quantidade_da_palavra=%s,
	    opi_tempo_da_palavra=%s,
	    opi_intervalo_da_palavra=%s,
	    
	    opi_palavra_imagem=%s,
	    opi_quantidade_da_imagem=%s,
	    opi_tempo_da_imagem=%s,
	    opi_intervalo_da_imagem=%s
	WHERE opi_codigo=%s
""",
(
    item['codigoDaPalavraTexto'],
    item['quantidadeDaPalavraTexto'],
    item['tempoDaPalavraTexto'],
    item['intervaloDaPalavraTexto'],

    item['codigoDaPalavraImagem'],
    item['quantidadeDaPalavraImagem'],
    item['tempoDaPalavraImagem'],
    item['intervaloDaPalavraImagem'],
    item['codigo']
))

            return jsonify({'message': 'Itens alterado com sucesso!'}), 201    
        
        except:
            return 
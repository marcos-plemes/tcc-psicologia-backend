from flask import request, jsonify
import base64

def registrar_rotas_grupos(app, cursor):
    @app.route('/grupos/<int:codigo>', methods=['DELETE'])
    def deletarGrupo(codigo):
        cursor.execute("DELETE FROM grupo WHERE gp_codigo = %s", (codigo,))
        return jsonify({'message': 'Grupo deletada com sucesso!'}), 200

    @app.route('/grupos')
    def get_grupos():
        cursor.execute("SELECT * FROM grupo ORDER BY gp_nome")
        grupos = list()
        for grupo in cursor.fetchall():
            grupos.append({
                'codigo': grupo[0],
                'nome': grupo[1],
                'isMostrarImagem': grupo[2],
                'isMostrarImagemPrimeiro': grupo[3]
            })
    
        return grupos
    
    @app.route('/grupos/<int:codigo>', methods=['GET'])
    def get_grupo(codigo):
        cursor.execute("SELECT * FROM grupo WHERE gp_codigo = %s", (codigo,))
        grupo = cursor.fetchone()  

        if grupo:
            return jsonify({
                'codigo': grupo[0],
                'nome': grupo[1],
                'isMostrarImagem': grupo[2],
                'isMostrarImagemPrimeiro': grupo[3],
                'ordemDaPalavra': grupo[4]
            })
        else:
            return jsonify({'message': 'Grupo não encontrada'}), 404
        
    @app.route('/grupos', methods=['POST'])
    def cadastrarGrupo():
        try:
            cursor.execute("""INSERT INTO public.grupo (gp_nome,
                                                        gp_mostrar_foto, 
                                                        gp_mostrar_foto_primeiro,
                                                        gp_ordem_da_palavra
                           ) VALUES(%s, %s, %s, %s) RETURNING gp_codigo""",
                        (request.form['nome'],
                         request.form['isMostrarImagem'],
                         request.form['isMostrarImagemPrimeiro'],
                         request.form['ordemDaPalavra']
                         ))
        
            codigo = cursor.fetchone()[0]
            return jsonify({
                'message': 'Grupo cadastrada com sucesso!',
                'codigo': codigo
                }), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/grupos', methods=['PUT'])
    def alterarGrupo():
        codigo = request.form['codigo']
        print(request.form)
        if codigo == '':
            return jsonify({"error": "Código não informado"}), 400
        try:
            cursor.execute("""UPDATE public.grupo 
                                 SET gp_mostrar_foto=%s, 
                                     gp_nome=%s, 
                                     gp_mostrar_foto_primeiro=%s,
                                     gp_ordem_da_palavra=%s
                               WHERE gp_codigo=%s;""",
                        (request.form['isMostrarImagem'],
                         request.form['nome'],
                         request.form['isMostrarImagemPrimeiro'],
                         request.form['ordemDaPalavra'],
                         request.form['codigo']))
            return jsonify({'message': 'Grupo Alterado com sucesso!'}), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/gerar-ordem/<int:quantidade>')
    def getOrdemDasPalavras(quantidade):
        print(quantidade)
        cursor.execute("""
SELECT p.pg_codigo, 
       p.pg_descricao, 
       (SELECT pg_codigo
          FROM perguntas 
         WHERE pg_codigo != p.pg_codigo
      ORDER BY random() 
         LIMIT 1) 
  FROM perguntas p 
ORDER BY random() 
    LIMIT %s                        
""", (quantidade,))
        palavras = list()
        for palavra in cursor.fetchall():
            palavras.append({
                'codigo': palavra[0],
                'descricao': palavra[1],
                'codigoDaImagemAleatoria': palavra[2],
                'quantidadeDaPalavra': 1,
                'intervaloDeTempoDaPalavra': 1000,
                'tempoDaPalavra': 1000,
                'quantidadeDaImagem': 1,
                'intervaloDeTempoDaImagem': 1000,
                'tempoDaImagem': 1000
            })
    
        return palavras
    
    @app.route('/ordem/<int:grupo>', methods=['POST'])
    def cadastrarOrdem(grupo):    
        try:
            
            cursor.execute("DELETE FROM ordem WHERE grupo = %s", (grupo,))

            for ordem in request.get_json():
                cursor.execute("""INSERT INTO ordem (quantidade_da_palavra,
                                                     tempo_da_palavra,
                                                     intervalo_da_palavra,
                                                     quantidade_da_imagem,
                                                     tempo_da_imagem,
                                                     intervalo_da_imagem,
                                                     palavra,
                                                     grupo) 
                                  VALUES (%s,
                                          %s,
                                          %s,
                                          %s,
                                          %s,
                                          %s,
                                          %s,
                                          %s)""", (ordem['quantidadeDaPalavra'],
                                                   ordem['tempoDaPalavra'],
                                                   ordem['intervaloDeTempoDaPalavra'],
                                                   ordem['quantidadeDaImagem'],
                                                   ordem['tempoDaPalavra'],
                                                   ordem['intervaloDeTempoDaImagem'],
                                                   ordem['codigo'],
                                                   grupo))

                # cursor.execute("""INSERT INTO public.grupo (gp_nome,
                #                                         gp_mostrar_foto, 
                #                                         gp_mostrar_foto_primeiro,
                #                                         gp_mostrar_foto_correspondente_a_palavra,
                #                                         gp_quantidade_de_palavras) VALUES(%s, %s, %s, %s, %s) RETURNING gp_codigo""",
                #         (request.form['nome'],
                #          request.form['isMostrarImagem'],
                #          request.form['isMostrarImagemPrimeiro'],
                #          request.form['isMostrarImagemCorrespondenteAPalavra'],
                #          request.form['quantidadeDePalavras']
                #          ))
        
                
            return jsonify({'message': 'Ordem cadastrada com sucesso!'}), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
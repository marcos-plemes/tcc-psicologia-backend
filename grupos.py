from flask import request, jsonify
import base64

def registrar_rotas_grupos(app, cursor):
    @app.route('/grupos')
    def get_grupos():
        cursor.execute("SELECT * FROM grupo")
        grupos = list()
        for grupo in cursor.fetchall():
            grupos.append({
                'codigo': grupo[0],
                'nome': grupo[1],
                'isMostrarImagem': grupo[2]
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
                'isMostrarImagem': grupo[2]
            })
        else:
            return jsonify({'message': 'Grupo não encontrada'}), 404
        
    @app.route('/grupos', methods=['POST'])
    def cadastrarGrupo():
        try:
            cursor.execute("INSERT INTO public.grupo (gp_nome,gp_mostrar_foto) VALUES(%s, %s) RETURNING gp_codigo",
                        (request.form['descricao'],
                            request.form['isMostrarImagem']))
        
            codigo = cursor.fetchone()[0]
            return jsonify({
                'message': 'Grupo cadastrada com sucesso!',
                'codigo': codigo
                }), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/grupos', methods=['PUT'])
    def alterarGrupo():
        try:
            cursor.execute("UPDATE public.grupo SET gp_mostrar_foto=%s, gp_nome=%s WHERE gp_codigo=%s;",
                        (request.form['descricao'],
                         request.form['isMostrarImagem'],
                         request.form['codigo']))
            return jsonify({'message': 'Grupo Alterado com sucesso!'}), 201    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
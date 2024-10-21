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
                'isMostrarFoto': grupo[2]
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
                'imaisMostrarFotogem': grupo[2]
            })
        else:
            return jsonify({'message': 'Grupo não encontrada'}), 404
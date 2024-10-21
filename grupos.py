from flask import request, jsonify
import base64

def registrar_rotas_grupos(app, cursor):
    @app.route('/grupos')
    def getGrupos():
        cursor.execute("SELECT * FROM grupo")
        grupos = list()
        for grupo in cursor.fetchall():
            grupos.append({
                'codigo': grupo[0],
                'nome': grupo[1],
                'isMostrarFoto': grupo[2]
            })
    
        return grupos
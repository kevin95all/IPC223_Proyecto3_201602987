from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)


@app.route('/')
def hellow_world():
    return jsonify({"MSG": "Iniciando servidor en el puerto por defecto 5000"})


@app.route('/UsuarioConectado', methods=['GET'])
def usuario_conectado():
    nombre = request.args.get('nombre')

    return jsonify({"Nombre": nombre})


@app.route('/ObtenerDatos', methods=['POST'])
def obtener_datos():
    perfil = request.get_json()

    if perfil['id'] == 1:
        return jsonify({"MSG": "Usuario bloqueado"})
    return jsonify({"MSG": "Tu si puedes pasar"})


if __name__ == "__main__":
    app.run()

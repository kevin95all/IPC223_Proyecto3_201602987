from flask import Flask, request, Response
from flask.json import jsonify
from Gestor import Gestor


app = Flask(__name__)

gestor = Gestor()


@app.route('/')
def home():
    return 'MSG: Iniciando servidor en el puerto por defecto 5000'


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


@app.route('/CargarConfiguraciones', methods=['POST'])
def cargar_configuraciones():
    if request.method == 'POST':
        return Response(gestor.recibir_configuraciones(request.data), status=201, mimetype='text/xml')
    else:
        return 'No se pudo cargar el archivo de configuraciones'


@app.route('/CargarMensajes', methods=['POST'])
def cargar_mensajes():
    if request.method == 'POST':
        return Response(gestor.recibir_mensajes(request.data), status=201, mimetype='text/xml')
    else:
        return 'No se pudo cargar el archivo de mensajes'


if __name__ == "__main__":
    app.run()

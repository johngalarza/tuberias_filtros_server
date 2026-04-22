import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/filtros/validar", methods = ["POST"])
def validar():
    try:
        context = request.get_json()
        cedula = context.get("cedula")
        nombre = context.get("nombre")
        apellido = context.get("apellido")
        telefono = context.get("telefono")
        email = context.get("email")

        if len(cedula) != 10:
            return jsonify({"estado": "error", "mensaje": "La cedula debe tener 10 digitos."}), 406
        if len(telefono) != 10:
            return jsonify({"estado": "error", "mensaje": "El telefono debe tener 10 digitos."}), 406
        if not re.match("^[a-zA-Z0-9_.±]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$", email):
            return jsonify({"estado": "error", "mensaje": "Ingrese un email valido"}), 406
        
        return jsonify({"estado": "ok", "mensaje": "Datos validados"}), 200
    except Exception as error:
        return jsonify({"estado": "error", "mensaje": error}), 500

if __name__ == "__main__":
    app.run(port=503, debug=True)
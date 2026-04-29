import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from flask import Flask, request, jsonify
from db.db import get_connection

app = Flask(__name__)

@app.route("/filtros/registrar", methods = ["POST"])
def registrar():
    contexto = request.get_json()
    cedula = contexto.get("cedula")
    nombre = contexto.get("nombre")
    apellido = contexto.get("apellido")
    telefono = contexto.get("telefono")
    email = contexto.get("email")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM pacientes WHERE cedula = %s", (cedula,))
        paciente = cursor.fetchone()
        if paciente:
            cursor.close()
            conn.close()
            return jsonify({"mensaje": f"Ya existe paciente con la cedula {cedula}"}), 400
        cursor.execute("INSERT INTO pacientes (cedula, nombre, apellido, telefono, email) VALUES (%s,%s,%s,%s,%s) RETURNING *", (cedula, nombre, apellido, telefono, email))
        paciente = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"estado": "ok", "mensaje": "Registrado Exitosamente", "paciente_id": paciente["id"]}), 201
    except Exception as error:
        return jsonify({"estado": "error", "mensaje": str(error)}), 500

@app.route("/pacientes", methods = ["GET"])
def listar_pacientes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes")
        pacientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"estado": "ok", "datos": pacientes}), 200
    except Exception as error:
        return jsonify({"estado": "error", "mensaje": str(error)})

if __name__ == "__main__":
    app.run(port=504, debug=True)
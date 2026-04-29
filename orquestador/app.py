from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

tuberia = [
    {
        "nombre": "Validar",
        "url": "http://localhost:503/filtros/validar"
    },
    {
        "nombre": "Registrar",
        "url": "http://localhost:504/filtros/registrar"
    },
]

@app.route("/pipeline/ejecutar", methods=["POST"])
def ejecutar_pipeline():
    contexto  = request.get_json()
    historial = []

    for filtro in tuberia:
        try:
            respuesta = requests.post(filtro["url"], json=contexto, timeout=10)
        except requests.exceptions.ConnectionError:
            return jsonify({
                "estado": "error",
                "paso": filtro["nombre"],
                "historial": historial
            }), 503

        try:
            resultado = respuesta.json()
        except ValueError:
            return jsonify({
                "estado": "error",
                "paso": filtro["nombre"],
                "mensaje": "Respuesta inválida del servicio",
                "detalle": respuesta.text,
                "historial": historial
            }), 502

        historial.append({
            "filtro": filtro["nombre"],
            "resultado": resultado
        })

        if resultado.get("estado") != "ok":
            return jsonify({
                "estado": "error",
                "paso": filtro["nombre"],
                "mensaje": resultado.get("mensaje"),
                "historial": historial
            }), 400

        contexto.update(resultado.get("datos", {}))

    return jsonify({
        "estado": "ok",
        "historial": historial
    }), 200

if __name__ == "__main__":
    app.run(port=502, debug=True)

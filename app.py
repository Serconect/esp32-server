from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print("Datos recibidos:", data)
    return jsonify({"status": "ok"}), 200

import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

def init_db():
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperatura REAL,
            humedad REAL,
            vibracion INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    timestamp = datetime.utcnow().isoformat()

    conn = sqlite3.connect('datos.db')
    c = conn.cursor()
    c.execute('INSERT INTO registros (timestamp, temperatura, humedad, vibracion) VALUES (?, ?, ?, ?)',
              (timestamp, data['temperatura'], data['humedad'], data['vibracion']))
    conn.commit()
    conn.close()

    print("Datos guardados:", data)
    return jsonify({"status": "ok"}), 200

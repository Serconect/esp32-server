from flask import render_template
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Inicializar base de datos
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

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM registros ORDER BY timestamp DESC LIMIT 50')
    rows = c.fetchall()
    conn.close()

    html = "<h2>Últimos registros</h2><table border='1'><tr><th>Fecha</th><th>Temp (°C)</th><th>Humedad (%)</th><th>Vibración</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
    html += "</table>"
    return html

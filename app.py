import os
import socket
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "notas.db")
APP_VERSION = os.environ.get("APP_VERSION", "v1.0")

def init_db():
    if os.path.dirname(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notas (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT NOT NULL)"
        )
        
@app.route("/")
def index():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, texto FROM notas").fetchall()
    return jsonify({
        "servicio": "Bitacora Sistemas Operativos",
        "version": APP_VERSION,
        "contenedor_id": socket.gethostname(),
        "total_notas": len(rows),
        "notas": [{"id": r[0], "texto": r[1]} for r in rows],   
    })

@app.route("/notas", methods =["POST"])
def agregar_nota():
    data = request.get_json(silent=True) or {}
    texto = data.get("texto", "").strip()
    if not texto:
        return jsonify({"error": "El campo 'texto' es obligatorio"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO notas (texto) VALUES (?)",
        (texto,))
    return jsonify({"mensaje": "Nota guardada", "texto": texto}), 201

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

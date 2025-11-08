# app/faq_api.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from . import database_oracle as db

app = Flask(__name__)

# --- inicializa a tabela ao carregar o app (compatível com Flask 3.x) ---
try:
    db.init_db()
except Exception as e:
    print("init_db falhou:", e)

# --- CORS: apenas ambiente local ---
raw = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173,http://127.0.0.1:5173")
_clean = raw.replace("\r", "").replace("\n", "")
origins = [o.strip() for o in _clean.split(",") if o.strip()]

CORS(app, resources={
    r"/api/*": {
        "origins": origins if origins else "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
    }
})

@app.after_request
def add_cors_headers(resp):
    origin = request.headers.get("Origin")
    if origin and (origin in origins or not origins):
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Vary"] = "Origin"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return resp

# Healthcheck
@app.get("/")
def home():
    return jsonify({"status": "ok", "service": "faq-api", "allowed_origins": origins}), 200

# ---- CRUD FAQ ----
@app.get("/api/faqs")
def faqs_all():
    q = request.args.get("q")
    return jsonify(db.listar_faqs(q)), 200

@app.get("/api/faqs/<int:fid>")
def faqs_one(fid: int):
    itens = [f for f in db.listar_faqs() if f.get("id") == fid]
    if not itens:
        return jsonify({"title": "FAQ não encontrada", "status": 404}), 404
    return jsonify(itens[0]), 200

@app.post("/api/faqs")
def faqs_create():
    data = request.get_json(silent=True) or {}
    pergunta = (data.get("pergunta") or "").strip()
    resposta = (data.get("resposta") or "").strip()
    if not pergunta or not resposta:
        return jsonify({"title": "Campos obrigatórios: pergunta, resposta", "status": 400}), 400

    new_id = db.criar_faq(pergunta, resposta)
    return jsonify({"id": new_id, "pergunta": pergunta, "resposta": resposta}), 201

@app.put("/api/faqs")
def faqs_update():
    data = request.get_json(silent=True) or {}
    try:
        fid = int(data.get("id"))
    except (TypeError, ValueError):
        return jsonify({"title": "Campo obrigatório: id (inteiro)", "status": 400}), 400

    pergunta = data.get("pergunta")
    resposta = data.get("resposta")
    ok = db.atualizar_faq(fid, pergunta, resposta)
    return (jsonify({"id": fid, "pergunta": pergunta, "resposta": resposta}), 200) if ok \
        else (jsonify({"title": "FAQ não encontrada", "status": 404}), 404)

@app.delete("/api/faqs/<int:fid>")
def faqs_delete(fid: int):
    ok = db.remover_faq(fid)
    return (jsonify({"id": fid}), 200) if ok else (jsonify({"title": "FAQ não encontrada", "status": 404}), 404)

# Rota de debug (lista rotas)
@app.get("/__routes")
def routes():
    return jsonify(sorted([str(r) for r in app.url_map.iter_rules()])), 200

# Execução local
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

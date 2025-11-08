# app/faq_api.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from . import database_oracle as db  # seu arquivo de banco

app = Flask(__name__)

# Origens permitidas: múltiplas separadas por vírgula na env FRONTEND_ORIGIN
origins = [o.strip() for o in os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",") if o.strip()]

# CORS para rotas /api/*
CORS(app, resources={r"/api/*": {"origins": origins, "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# Reforço de CORS (preflight/headers)
@app.after_request
def add_cors_headers(resp):
    origin = request.headers.get("Origin")
    if origin and origin in origins:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Vary"] = "Origin"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return resp

# Healthcheck (resolve o 404 do "/")
@app.get("/")
def home():
    return {"status": "ok", "service": "faq-api", "allowed_origins": origins}, 200

# ---- CRUD FAQ ----
@app.get("/api/faqs")
def faqs_all():
    q = request.args.get("q")
    return jsonify(db.listar_faqs(q)), 200

@app.post("/api/faqs")
def faqs_create():
    dado = request.get_json(force=True)
    new_id = db.criar_faq(dado["pergunta"], dado["resposta"])
    return jsonify({"id": new_id, **dado}), 201

@app.put("/api/faqs")
def faqs_update():
    dado = request.get_json(force=True)
    ok = db.atualizar_faq(int(dado["id"]), dado.get("pergunta"), dado.get("resposta"))
    if ok:
        return jsonify(dado), 200
    return jsonify({"title": "FAQ não encontrada", "status": 404}), 404

@app.delete("/api/faqs/<int:fid>")
def faqs_delete(fid):
    ok = db.remover_faq(fid)
    if ok:
        return jsonify({"id": fid}), 200
    return jsonify({"title": "FAQ não encontrada", "status": 404}), 404

# Debug opcional: lista rotas registradas
@app.get("/__routes")
def routes():
    return jsonify(sorted([str(r) for r in app.url_map.iter_rules()])), 200

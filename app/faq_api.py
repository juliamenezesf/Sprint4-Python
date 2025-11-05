# app/faq_api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from . import database_oracle as db   # usa o seu arquivo de banco

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

# --- inicializa o DB uma vez, no carregamento do app (compatível com Flask 3) ---
try:
    db.init_db()
except Exception as e:
    # não para a aplicação por causa de DDL sem permissão; só loga
    app.logger.warning(f"init_db falhou: {e}")

def _ok(payload, status=200):
    return jsonify(payload), status

def _nf(msg="Não encontrado"):
    return jsonify({"title": msg, "status": 404}), 404

@app.get("/api/faqs")
def faqs_all():
    q = request.args.get("q")
    return _ok(db.listar_faqs(q))

@app.post("/api/faqs")
def faqs_create():
    dado = request.get_json(force=True)
    new_id = db.criar_faq(dado["pergunta"], dado["resposta"])
    return _ok({"id": new_id, **dado}, 201)

@app.put("/api/faqs")
def faqs_update():
    dado = request.get_json(force=True)
    ok = db.atualizar_faq(int(dado["id"]), dado.get("pergunta"), dado.get("resposta"))
    return _ok(dado) if ok else _nf("FAQ não encontrada")

@app.delete("/api/faqs/<int:fid>")
def faqs_delete(fid):
    return _ok({"id": fid}) if db.remover_faq(fid) else _nf("FAQ não encontrada")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

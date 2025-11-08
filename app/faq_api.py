# app/faq_api.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from . import database_oracle as db

app = Flask(__name__)

# múltiplas origens separadas por vírgula (ex: "http://localhost:5173,https://seu-front.com")
origins = [o.strip() for o in os.getenv("FRONTEND_ORIGIN", "http://localhost:5173,http://127.0.0.1:5173").split(",") if o.strip()]
CORS(app, origins=origins)

# init DB compatível Flask 3
try:
    db.init_db()
except Exception as e:
    app.logger.warning(f"init_db falhou: {e}")

@app.get("/")
def home():
    return {"status": "ok", "service": "faq-api", "allowed_origins": origins}, 200

# ... (resto igual: /api/faqs GET/POST/PUT/DELETE)

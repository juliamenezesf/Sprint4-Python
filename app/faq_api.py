import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from . import database_oracle as db

app = Flask(__name__)

origins = [o.strip() for o in os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",") if o.strip()]

CORS(app, resources={r"/api/*": {"origins": origins, "methods": ["GET","POST","PUT","DELETE","OPTIONS"]}})

@app.after_request
def add_cors_headers(resp):
    origin = request.headers.get("Origin")
    if origin and origin in origins:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Vary"] = "Origin"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return resp

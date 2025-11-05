# app/export.py
import json, os
from . import db_oracle as db

def exportar_json() -> str:
    os.makedirs("exports", exist_ok=True)
    data = {"faqs": db.listar_faqs()}
    path = os.path.join("exports", "faqs_dump.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

# app/export.py
import json
from . import database_oracle as db

def run(path="faqs_export.json"):
    data = db.listar_faqs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exportado: {path} ({len(data)} registros)")

if __name__ == "__main__":
    run()

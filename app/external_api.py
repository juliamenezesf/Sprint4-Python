# app/external_api.py
import requests

def conselho_do_dia() -> str:
    """Busca um conselho em API pública (sem chave)."""
    r = requests.get("https://api.adviceslip.com/advice", timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["slip"]["advice"]

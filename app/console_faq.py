# app/console_faq.py
import json
from . import database_oracle as db
from .external_api import conselho_do_dia

def menu():
    print("\n==== MENU FAQ ====")
    print("1. Inserir nova FAQ")
    print("2. Listar FAQs")
    print("3. Atualizar FAQ")
    print("4. Remover FAQ")
    print("5. Exportar FAQs (JSON)")
    print("6. Importar 'Conselho do dia' (API pública) como FAQ")
    print("0. Sair")
    return input("Escolha: ")

def inserir():
    pergunta = input("Pergunta: ")
    resposta = input("Resposta: ")
    new_id = db.criar_faq(pergunta, resposta)
    print(f"✅ Inserido com ID {new_id}")

def listar():
    filtro = input("Buscar por termo (ou Enter p/ tudo): ").strip()
    faqs = db.listar_faqs(filtro or None)
    if not faqs:
        print("⚠️ Nenhum registro encontrado.")
    else:
        print("\n--- FAQs ---")
        for f in faqs:
            print(f"[{f['id']}] {f['pergunta']} → {f['resposta']}")

def atualizar():
    fid = int(input("ID da FAQ a atualizar: "))
    pergunta = input("Nova pergunta (ou Enter p/ manter): ").strip() or None
    resposta = input("Nova resposta (ou Enter p/ manter): ").strip() or None
    ok = db.atualizar_faq(fid, pergunta, resposta)
    print("✅ Atualizada." if ok else "❌ Não encontrada.")

def remover():
    fid = int(input("ID da FAQ a remover: "))
    ok = db.remover_faq(fid)
    print("✅ Removida." if ok else "❌ Não encontrada.")

def exportar():
    faqs = db.listar_faqs()
    nome_arquivo = "faqs_export.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(faqs, f, ensure_ascii=False, indent=2)
    print(f"✅ Exportado para {nome_arquivo}")

def importar_conselho():
    txt = conselho_do_dia()
    new_id = db.criar_faq("Conselho do dia", txt)
    print(f"✅ Importado e salvo como FAQ #{new_id}: {txt}")

def main():
    db.init_db()
    while True:
        op = menu()
        if op == "1": inserir()
        elif op == "2": listar()
        elif op == "3": atualizar()
        elif op == "4": remover()
        elif op == "5": exportar()
        elif op == "6": importar_conselho()
        elif op == "0":
            print("👋 Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

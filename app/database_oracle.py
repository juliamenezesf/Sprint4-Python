# app/database_oracle.py
import os
from typing import Dict, Any, List, Optional
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String,
    select, update, delete, text
)
from sqlalchemy.engine import Engine

# variável do ambiente (já configurada no terminal)
# oracle+oracledb://USUARIO:SENHA@oracle.fiap.com.br:1521/ORCL
DATABASE_URL = os.environ["DATABASE_URL"]

engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
metadata = MetaData()

faqs = Table(
    "FAQS", metadata,
    Column("ID", Integer, primary_key=True, autoincrement=True),
    Column("PERGUNTA", String(500), nullable=False),
    Column("RESPOSTA", String(2000), nullable=False),
)

def init_db():
    """Cria a tabela se não existir (requer permissão DDL no schema)."""
    metadata.create_all(engine)

def _row_to_dict(row) -> Dict[str, Any]:
    m = dict(row._mapping)
    return {k.lower(): v for k, v in m.items()}

def criar_faq(pergunta: str, resposta: str) -> int:
    with engine.begin() as conn:
        res = conn.execute(faqs.insert().values(PERGUNTA=pergunta, RESPOSTA=resposta))
        try:
            return int(res.inserted_primary_key[0])
        except Exception:
            return int(conn.execute(text("SELECT MAX(ID) FROM FAQS")).scalar_one())

def listar_faqs(filtro: Optional[str]=None) -> List[Dict[str, Any]]:
    with engine.begin() as conn:
        if filtro:
            like = f"%{filtro}%"
            stmt = select(faqs).where(
                (faqs.c.PERGUNTA.like(like)) | (faqs.c.RESPOSTA.like(like))
            ).order_by(faqs.c.ID)
        else:
            stmt = select(faqs).order_by(faqs.c.ID)
        return [_row_to_dict(r) for r in conn.execute(stmt).fetchall()]

def atualizar_faq(faq_id: int, pergunta: Optional[str]=None, resposta: Optional[str]=None) -> bool:
    values = {}
    if pergunta is not None:
        values["PERGUNTA"] = pergunta
    if resposta is not None:
        values["RESPOSTA"] = resposta
    if not values:
        return False
    with engine.begin() as conn:
        res = conn.execute(update(faqs).where(faqs.c.ID==faq_id).values(**values))
        return (res.rowcount or 0) > 0

def remover_faq(faq_id: int) -> bool:
    with engine.begin() as conn:
        res = conn.execute(delete(faqs).where(faqs.c.ID==faq_id))
        return (res.rowcount or 0) > 0

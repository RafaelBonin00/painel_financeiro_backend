from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

acoes = []
with open("acoes_simples.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        acoes.append({"ticker": row["ticker"], "nome": row["nome"]})

@app.get("/autocomplete")
def autocomplete(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100)
):
    q_lower = q.lower()
    resultados = []
    for acao in acoes:
        # Busca com 'in' para achar termo em qualquer posição
        if q_lower in acao["ticker"].lower() or q_lower in acao["nome"].lower():
            resultados.append(acao)
            if len(resultados) >= limit:
                break
    return resultados

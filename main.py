from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import os
import csv

app = FastAPI()

# Permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio da sua aplicação frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar lista de ações na memória ao iniciar a aplicação
acoes = []
with open("acoes_simples.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        acoes.append({"ticker": row["ticker"], "nome": row["nome"]})

@app.get("/preco/{ticker}")
def preco_acao(ticker: str):
    acao = yf.Ticker(ticker)
    preco = acao.info.get("regularMarketPrice")
    nome = acao.info.get("shortName")
    return {
        "ticker": ticker.upper(),
        "nome": nome,
        "preco": preco,
    }

@app.get("/autocomplete")
def autocomplete(q: str = Query(..., min_length=1)):
    q = q.lower()
    resultados = []
    for acao in acoes:
        if acao["ticker"].lower().startswith(q) or acao["nome"].lower().startswith(q):
            resultados.append(acao)
        if len(resultados) >= 10:  # Limitar máximo de resultados para performance
            break
    return resultados

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

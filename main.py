from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import os
import csv

app = FastAPI()

# Permitir acesso do frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, use domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega lista de ações ao iniciar o app
acoes = []
try:
    with open("acoes_simples.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            acoes.append({"ticker": row["ticker"], "nome": row["nome"]})
except FileNotFoundError:
    print("Arquivo 'acoes_simples.csv' não encontrado.")

@app.get("/preco/{ticker}")
def preco_acao(ticker: str):
    try:
        acao = yf.Ticker(ticker)
        info = acao.info
        preco = info.get("regularMarketPrice")
        nome = info.get("shortName")
        return {
            "ticker": ticker.upper(),
            "nome": nome,
            "preco": preco,
        }
    except Exception as e:
        return {"erro": f"Não foi possível obter dados para {ticker}. Erro: {str(e)}"}

@app.get("/autocomplete")
def autocomplete(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100)
):
    q_lower = q.lower()
    resultados = []
    for acao in acoes:
        if q_lower in acao["ticker"].lower() or q_lower in acao["nome"].lower():
            resultados.append(acao)
            if len(resultados) >= limit:
                break
    return resultados

# Rodar com: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

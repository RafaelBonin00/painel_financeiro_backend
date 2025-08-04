from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import os

app = FastAPI()

# Permitir frontend acessar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/preco/{ticker}")
def preco_acao(ticker: str):
    acao = yf.Ticker(ticker)
    preco = acao.info.get("regularMarketPrice")
    nome = acao.info.get("shortName")
    return {
        "ticker": ticker,
        "nome": nome,
        "preco": preco,
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Permitir requisições do frontend (coloque seu domínio do Vercel em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: ["https://seu-app.vercel.app"]
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

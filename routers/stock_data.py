from fastapi import APIRouter
import schemas
import yfinance as yf
from typing import List


router = APIRouter(
    prefix="/stock_market",
    tags=["Stock Market"]
)


@router.post("/latest", response_model=List[schemas.Stock_Market_Ticker_Out])
async def get_latest_stock_data(tickers: schemas.Stock_Market_Ticker):
    current_prices = []
    for ticker in tickers.tickers:
        ticker_yahoo = yf.Ticker(ticker)
        data = ticker_yahoo.history()
        last_quote = data['Close'].iloc[-1]
        current_prices.append({"ticker": ticker, "last_quote": last_quote})
    return current_prices

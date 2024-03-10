from fastapi import APIRouter
import schemas
from typing import List
from .Stock_Market.current_data import get_current_stock_price
import concurrent.futures


router = APIRouter(
    prefix="/stock_market",
    tags=["Stock Market"]
)


@router.post("/latest", response_model=List[schemas.Stock_Market_Ticker_Out])
async def get_latest_stock_data(tickers: schemas.Stock_Market_Ticker):
    current_prices = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(
            get_current_stock_price, ticker, current_prices) for ticker in tickers.tickers]
    return current_prices

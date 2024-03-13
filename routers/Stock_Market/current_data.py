import requests
from config import settings

headers = {
    "User-Agent": settings.USER_AGENT
}


def get_current_stock_price(ticker: str, current_prices: list):
    response = requests.get(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}", proxies=settings.PROXIES, headers=headers).json()
    # print(response)
    last_quote = response['chart']['result'][0]['meta']['regularMarketPrice']
    current_prices.append({"ticker": ticker, "last_quote": last_quote})

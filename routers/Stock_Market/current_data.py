import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def get_current_stock_price(ticker: str, current_prices: list):
    response = requests.get(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}", proxies={
            "http": "http://nvkgvyfp-rotate:kccxhfu1bt2o@p.webshare.io:80/",
            "https": "http://nvkgvyfp-rotate:kccxhfu1bt2o@p.webshare.io:80/"
        }, headers=headers).json()
    # print(response)
    last_quote = response['chart']['result'][0]['meta']['regularMarketPrice']
    current_prices.append({"ticker": ticker, "last_quote": last_quote})

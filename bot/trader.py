import os
from binance.client import Client

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
client = Client(API_KEY, API_SECRET)

def analyze_signal():
    return "BTCUSDT", "LONG", "10 USDT"

def place_order():
    qty = 0.0001  # пробный ордер
    try:
        order = client.order_market_buy(symbol="BTCUSDT", quantity=qty)
        return order
    except Exception as e:
        return f"Ошибка: {e}"

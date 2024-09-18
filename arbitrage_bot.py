import ccxt
import time
import logging

# Logging ayarları
logging.basicConfig(filename='arbitrage_bot.log', level=logging.INFO)

# Borsa nesnelerini başlat
binance = ccxt.binance()
coinbase = ccxt.coinbase()
kraken = ccxt.kraken()  # Örnek olarak Kraken'i ekleyelim

def get_price(borsa, sembol):
    try:
        ticker = borsa.fetch_ticker(sembol)
        return ticker['last']
    except Exception as e:
        logging.error(f"Error fetching price from {borsa.id} for {sembol}: {e}")
        return None

def check_arbitrage_opportunity():
    binance_price = get_price(binance, 'BTC/USDT')
    coinbase_price = get_price(coinbase, 'BTC/USD')
    kraken_price = get_price(kraken, 'BTC/USD')  # Kraken'den USD fiyatını al

    if binance_price is None or coinbase_price is None or kraken_price is None:
        print("Error fetching prices.")
        return

    print(f"Binance Price: {binance_price} USDT")
    print(f"Coinbase Price: {coinbase_price} USD")
    print(f"Kraken Price: {kraken_price} USD")

    # Fiyat farklarını hesapla
    binance_vs_coinbase = coinbase_price - binance_price
    kraken_vs_coinbase = coinbase_price - kraken_price
    print(f"Binance vs Coinbase Price Difference: {binance_vs_coinbase} USD")
    print(f"Kraken vs Coinbase Price Difference: {kraken_vs_coinbase} USD")

    # Arbitrage fırsatlarını kontrol et
    if binance_vs_coinbase > 0:
        print(f"Arbitrage Opportunity: Buy on Binance and Sell on Coinbase")
        logging.info(f"Arbitrage Opportunity: Buy on Binance ({binance_price}) and Sell on Coinbase ({coinbase_price})")
    elif binance_vs_coinbase < 0:
        print(f"Arbitrage Opportunity: Buy on Coinbase and Sell on Binance")
        logging.info(f"Arbitrage Opportunity: Buy on Coinbase ({coinbase_price}) and Sell on Binance ({binance_price})")
    else:
        print("No Arbitrage Opportunity")

    # Kraken fırsatlarını kontrol et
    if kraken_vs_coinbase > 0:
        print(f"Arbitrage Opportunity: Buy on Kraken and Sell on Coinbase")
        logging.info(f"Arbitrage Opportunity: Buy on Kraken ({kraken_price}) and Sell on Coinbase ({coinbase_price})")
    elif kraken_vs_coinbase < 0:
        print(f"Arbitrage Opportunity: Buy on Coinbase and Sell on Kraken")
        logging.info(f"Arbitrage Opportunity: Buy on Coinbase ({coinbase_price}) and Sell on Kraken ({kraken_price})")
    else:
        print("No Arbitrage Opportunity with Kraken")

# Botu belirli aralıklarla çalıştır
while True:
    check_arbitrage_opportunity()
    time.sleep(60)  # 1 dakikada bir kontrol et

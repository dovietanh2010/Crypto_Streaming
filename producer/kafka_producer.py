from kafka import KafkaProducer
import json
import requests
import time
from datetime import datetime


# Khởi tạo Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

COINS = ["bitcoin", "ethereum", "dogecoin", "solana"]

def fetch_crypto_data():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(COINS)}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()

while True:
    crypto_data = fetch_crypto_data()
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
   
    for coin, price in crypto_data.items():
        message = {
            "symbol": coin.upper(),
            "price": price.get('usd', 'N/A'),
            "timestamp": formatted_time
        }
        producer.send("crypto_topic", value=message)
        print(f"Sent: {message}")
    
    time.sleep(60)  # Gửi dữ liệu mỗi 60 giây

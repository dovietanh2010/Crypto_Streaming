# ⚡ Crypto Streaming Pipeline

## 🐳 Giới thiệu

Dự án này sử dụng **Apache Kafka** và **Apache Spark Streaming** để thu thập, xử lý và lưu trữ dữ liệu giá tiền điện tử theo thời gian thực. Dữ liệu được lưu vào cơ sở dữ liệu SQLite để phân tích.

## 🌟 Quy trình ETL

- **Dữ liệu thu thập**: Lấy dữ liệu giá tiền điện tử từ API.

- **Xử lý**: Streaming dữ liệu theo thời gian thực bằng Spark.

- **Lưu trữ**: Lưu dữ liệu vào SQLite để phân tích.

## 🌍 Công nghệ sử dụng

- **Apache Kafka**: Hệ thống message queue để truyền dữ liệu.

- **Apache Spark Streaming**: Xử lý dữ liệu thời gian thực.

- **SQLite**: Lưu trữ dữ liệu đã xử lý.

-**Docker**: Triển khai pipeline.

## 🛠️ Cài đặt & Chạy thử

### 1. Clone repository
``` bash
git clone https://github.com/user/crypto-streaming.git
cd crypto-streaming
```
### 2. Chạy Kafka và Spark Streaming bằng Docker
``` bash
docker-compose up --build
```
### 3. Kiểm tra luồng dữ liệu

- Producer gửi dữ liệu từ **kafka_producer.py**.

- Consumer xử lý dữ liệu với **spark_streaming.py**.

- Dữ liệu được lưu vào **CryptoDB.db**.

---
Chúc bạn cài đặt thành công! 🚀


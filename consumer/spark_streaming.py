import sqlite3
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Kafka & SQLite Config
KAFKA_TOPIC = "crypto_topic"
KAFKA_BROKER = "localhost:9092"
SQLITE_DB = "CryptoDB.db" 

# SQLite Connection String
conn_str = f"sqlite:///{SQLITE_DB}"

# Define Schema
schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("timestamp", StringType(), True),
])

def write_to_sql(df, epoch_id):
    print(f"Writing batch {epoch_id}...")

    # Chuyển đổi DataFrame Spark thành Pandas để xử lý pivot
    pdf = df.toPandas()

    # Pivot dữ liệu: mỗi symbol trở thành một cột
    pdf_pivot = pdf.pivot(index="timestamp", columns="symbol", values="price").reset_index()

    # Kết nối SQLite
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    # Tạo bảng nếu chưa có trong SQLite
    columns = ", ".join([f'"{col}" REAL' for col in pdf_pivot.columns if col != "timestamp"])
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            timestamp TEXT PRIMARY KEY, {columns}
        )
    """
    cursor.execute(create_table_query)

    # Ghi dữ liệu vào SQLite
    pdf_pivot.to_sql("crypto_prices", conn, if_exists="append", index=False)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Batch {epoch_id} đã ghi vào SQLite")


# Khởi tạo Spark Session
spark = SparkSession.builder \
    .appName("CryptoStreaming") \
    .master("local") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .config("spark.sql.streaming.checkpointLocation", "checkpoint/") \
    .getOrCreate()

# Đọc dữ liệu từ Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Parsing dữ liệu Kafka JSON thành DataFrame
df_parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Chạy Streaming Query và ghi dữ liệu vào SQLite
query = df_parsed.writeStream \
    .foreachBatch(write_to_sql) \
    .outputMode("append") \
    .trigger(processingTime="10 seconds")\
    .start()

query.awaitTermination()

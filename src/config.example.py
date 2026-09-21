import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# --- ES405 Connection ---
ES405_HOST = os.getenv("DEVICE_HOST", "your_device_host")
ES405_PORT = int(os.getenv("DEVICE_PORT", "your_device_port"))
ES405_TIMEOUT = int(os.getenv("ES405_TIMEOUT", "5"))
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", "3600"))

# --- Device Identity ---
DEVICE_ID = os.getenv("DEVICE_ID", "your_device_id")

# --- MQTT HiveMQ ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "brokermqtt.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "mqtt_port"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "mqtt_username")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "mqtt_password")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "mqtt_topic")
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "True").lower() in ("true", "1", "yes")

# --- MySQL Database ---
DB_HOST = os.getenv("DB_HOST", "host.docker.internal")
DB_PORT = int(os.getenv("DB_PORT", "db_port"))
DB_USER = os.getenv("DB_USER", "db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "db_password")
DB_NAME = os.getenv("DB_NAME", "db_name")
DB_TABLE = os.getenv("DB_TABLE", "db_table")

# --- File Storage ---
# Dalam Docker, data akan disimpan di folder /app/data
SAVE_FOLDER = "/app/data"
HISTORY_FILE = os.path.join(SAVE_FOLDER, "pm25_history_24h.json")

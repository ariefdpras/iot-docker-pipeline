import os
import csv
import random
import mysql.connector

from .config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_TABLE, SAVE_FOLDER

def save_to_mysql(payload):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        sql = f"""
            INSERT INTO {DB_TABLE}
                (ID, Time, PM1, PM25, PM4, PM10, TSP, Status, ISPU, Validasi, Ket)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            payload["device_id"],
            payload["timestamp"],
            payload["pm1"],
            payload["pm25"],
            payload["pm4"],
            payload["pm10"],
            payload["tsp"],
            payload["status"],
            payload["ispu"],
            payload["data_validation"],
            payload["ispu_category"]
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        print(f"  ✅ MySQL: Data disimpan ke tabel {DB_TABLE}")
        return True

    except Exception as e:
        print(f"  ✗ MySQL Error: {e}")
        return False


def save_to_csv(payload):
    random_str = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    filename = f"es405_output-{random_str}.csv"
    csv_path = os.path.join(SAVE_FOLDER, filename)

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "Device ID", "Timestamp", "PM1 (ug/m3)", "PM2.5 (ug/m3)",
            "PM4 (ug/m3)", "PM10 (ug/m3)", "TSP (ug/m3)", "Status",
            "PM2.5 Avg 24h (ug/m3)", "ISPU", "Kategori ISPU", "Validasi Data (%)"
        ])
        writer.writerow([
            payload["device_id"], payload["timestamp"], payload["pm1"],
            payload["pm25"], payload["pm4"], payload["pm10"],
            payload["tsp"], payload["status"], payload["pm25_avg_24h"],
            payload["ispu"], payload["ispu_category"], payload["data_validation"]
        ])

    print(f"  ✅ CSV: {csv_path}")
    return csv_path

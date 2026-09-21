import time
import sys
from datetime import datetime, timedelta

from config import DEVICE_ID, ES405_HOST, ES405_PORT, POLLING_INTERVAL, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, DB_USER, DB_HOST, DB_NAME, SAVE_FOLDER
from device import connect_es405
from ispu import load_pm25_history, prune_history, save_pm25_history, get_24h_stats, calculate_ispu, get_ispu_category
from storage import save_to_mysql, save_to_csv
from mqtt_client import publish_mqtt

def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " ES405 CONTINUOUS MONITOR (DOCKER VERSION) ".center(58) + "║")
    print("╠" + "═" * 58 + "╣")
    print(f"║  Device ID  : {DEVICE_ID:<42}║")
    print(f"║  Target     : {ES405_HOST}:{ES405_PORT:<35}║")
    print(f"║  Interval   : {POLLING_INTERVAL} detik ({POLLING_INTERVAL // 60} menit)" + " " * (58 - 30 - len(str(POLLING_INTERVAL)) - len(str(POLLING_INTERVAL // 60))) + "║")
    print(f"║  MQTT       : {MQTT_BROKER}:{MQTT_PORT}" + " " * (58 - 16 - len(MQTT_BROKER) - len(str(MQTT_PORT))) + "║")
    print(f"║  MQTT Topic : {MQTT_TOPIC:<42}║")
    print(f"║  MySQL      : {DB_USER}@{DB_HOST}/{DB_NAME}" + " " * (58 - 16 - len(DB_USER) - len(DB_HOST) - len(DB_NAME)) + "║")
    print(f"║  Folder Data: {SAVE_FOLDER:<42}║")
    print("╚" + "═" * 58 + "╝")
    print()

    history = load_pm25_history()
    history = prune_history(history)
    save_pm25_history(history)
    print(f"📊 PM2.5 History: {len(history)} data dalam 24 jam terakhir")
    print()

    polling_count = 0

    while True:
        polling_count += 1
        now = datetime.now()

        print("=" * 60)
        print(f"  [{now.strftime('%Y-%m-%d %H:%M:%S')}] Polling #{polling_count}")
        print("=" * 60)

        record = connect_es405()

        if record is None:
            next_retry = now + timedelta(seconds=POLLING_INTERVAL)
            print(f"\n  ⏳ Gagal ambil data. Retry: {next_retry.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            time.sleep(POLLING_INTERVAL)
            continue

        print()
        print(f"  ┌{'─' * 44}┐")
        print(f"  │{'DATA PENGUKURAN':^44}│")
        print(f"  ├{'─' * 44}┤")
        print(f"  │  Device ID : {record['device_id']:<29}│")
        print(f"  │  Timestamp : {record['timestamp']:<29}│")
        print(f"  │  PM1       : {record['pm1']:<10.2f} µg/m³{' ' * 13}│")
        print(f"  │  PM2.5     : {record['pm25']:<10.2f} µg/m³{' ' * 13}│")
        print(f"  │  PM4       : {record['pm4']:<10.2f} µg/m³{' ' * 13}│")
        print(f"  │  PM10      : {record['pm10']:<10.2f} µg/m³{' ' * 13}│")
        print(f"  │  TSP       : {record['tsp']:<10.2f} µg/m³{' ' * 13}│")
        print(f"  │  Status    : {record['status']:<29}│")
        print(f"  └{'─' * 44}┘")

        history.append({
            "timestamp": record["timestamp"],
            "local_timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "pm25": record["pm25"]
        })
        history = prune_history(history)
        save_pm25_history(history)

        pm25_avg, data_count, data_percentage = get_24h_stats(history)
        ispu_value = calculate_ispu(pm25_avg)
        ispu_category = get_ispu_category(ispu_value)

        print()
        print(f"  ┌{'─' * 44}┐")
        print(f"  │{'ISPU (PM2.5 - Rata-rata 24 Jam)':^44}│")
        print(f"  ├{'─' * 44}┤")
        print(f"  │  Data Valid      : {data_count} dari 24{' ' * (44 - 25 - len(str(data_count)))}│")
        print(f"  │  Validasi Data   : {data_percentage}%{' ' * (44 - 24 - len(str(data_percentage)))}│")
        print(f"  │  PM2.5 Avg 24h   : {pm25_avg:<10.2f} µg/m³{' ' * 8}│")
        print(f"  │  Nilai ISPU      : {ispu_value:<23}│")
        print(f"  │  Kategori        : {ispu_category:<23}│")
        print(f"  └{'─' * 44}┘")
        print("  *Keterangan: Data pengukuran selama 24 jam terus menerus,")
        print("   hasil perhitungan ISPU PM 2.5 disampaikan tiap jam selama 24 jam.")

        payload = {
            "device_id": record["device_id"],
            "timestamp": record["timestamp"],
            "pm1": record["pm1"],
            "pm25": record["pm25"],
            "pm4": record["pm4"],
            "pm10": record["pm10"],
            "tsp": record["tsp"],
            "status": record["status"],
            "pm25_avg_24h": pm25_avg,
            "ispu": ispu_value,
            "ispu_category": ispu_category,
            "data_validation": data_percentage
        }

        print()
        print(f"  ┌{'─' * 44}┐")
        print(f"  │{'SIMPAN & PUBLISH':^44}│")
        print(f"  ├{'─' * 44}┤")

        save_to_csv(payload)
        save_to_mysql(payload)
        publish_mqtt(payload)

        print(f"  └{'─' * 44}┘")

        next_poll = now + timedelta(seconds=POLLING_INTERVAL)
        print()
        print(f"  ⏳ Next polling: {next_poll.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("  🛑 Script dihentikan oleh user (Ctrl+C)")
        print("=" * 60)
        sys.exit(0)

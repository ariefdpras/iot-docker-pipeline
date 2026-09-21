import socket
import time
from .config import ES405_HOST, ES405_PORT, ES405_TIMEOUT, DEVICE_ID

def connect_es405():
    """
    Connect ke ES405 via TCP Socket, request last data, dan parse.
    Returns:
        dict: Record data, atau None jika gagal.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(ES405_TIMEOUT)

    try:
        sock.connect((ES405_HOST, ES405_PORT))
        print("  ✓ Connected to ES405")
    except Exception as e:
        print(f"  ✗ Gagal connect ke ES405: {e}")
        return None

    try:
        # Masuk user mode
        sock.sendall(b"\r\r\r")
        time.sleep(1)
        sock.recv(4096) 

        # Request last data
        sock.sendall(b"4\r")
        time.sleep(1)
        reply = sock.recv(4096).decode(errors="ignore")
    except Exception as e:
        print(f"  ✗ Error komunikasi: {e}")
        return None
    finally:
        sock.close()

    # --- Parsing ---
    lines = reply.splitlines()
    data_line = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("20"):
            data_line = stripped
            break

    if data_line is None:
        print("  ✗ Tidak menemukan data ES405 dalam response.")
        return None

    fields = [x.strip().replace("*", "") for x in data_line.split(",")]
    if len(fields) != 7:
        print(f"  ✗ Format data tidak sesuai (expected 7 fields, got {len(fields)})")
        print(f"    Raw: {fields}")
        return None

    try:
        record = {
            "device_id": DEVICE_ID,
            "timestamp": fields[0],
            "pm1": float(fields[1]),
            "pm25": float(fields[2]),
            "pm4": float(fields[3]),
            "pm10": float(fields[4]),
            "tsp": float(fields[5]),
            "status": float(fields[6])
        }
        return record
    except (ValueError, IndexError) as e:
        print(f"  ✗ Error parsing field: {e}")
        return None

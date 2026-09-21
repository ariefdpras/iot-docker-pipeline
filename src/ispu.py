import json
import os
from datetime import datetime, timedelta
from .config import HISTORY_FILE

# ==========================================================
# TABEL BREAKPOINT ISPU PM2.5 (PerMen LHK)
# ==========================================================
ISPU_BREAKPOINTS = [
    #  Ib,  Ia,    Xb,     Xa
    (   0,  50,    0.0,    15.5),
    (  50, 100,   15.5,    55.4),
    ( 100, 200,   55.4,   150.4),
    ( 200, 300,  150.4,   250.4),
    ( 300, 400,  250.4,   500.4),
]

def calculate_ispu(xx):
    """
    Hitung ISPU dari PM2.5 rata-rata 24 jam.
    Rumus: ISPU = (Ia - Ib) / (Xa - Xb) × (Xx - Xb) + Ib
    """
    if xx is None or xx < 0:
        return 0

    for Ib, Ia, Xb, Xa in ISPU_BREAKPOINTS:
        if Xb <= xx <= Xa:
            ispu = ((Ia - Ib) / (Xa - Xb)) * (xx - Xb) + Ib
            return round(ispu)

    if xx > ISPU_BREAKPOINTS[-1][3]:
        Ib, Ia, Xb, Xa = ISPU_BREAKPOINTS[-1]
        ispu = ((Ia - Ib) / (Xa - Xb)) * (xx - Xb) + Ib
        return round(ispu)

    return 0

def get_ispu_category(ispu_value):
    if ispu_value <= 50:
        return "Baik"
    elif ispu_value <= 100:
        return "Sedang"
    elif ispu_value <= 200:
        return "Tidak Sehat"
    elif ispu_value <= 300:
        return "Sangat Tidak Sehat"
    else:
        return "Berbahaya"

# ==========================================================
# HISTORY MANAGEMENT
# ==========================================================
def load_pm25_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"  ⚠ Gagal load history: {e}")
            return []
    return []

def save_pm25_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"  ⚠ Gagal simpan history: {e}")

def prune_history(history):
    cutoff = datetime.now() - timedelta(hours=24)
    pruned = []
    for entry in history:
        try:
            ts_str = entry.get("local_timestamp", entry.get("timestamp"))
            ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            if ts >= cutoff:
                pruned.append(entry)
        except (ValueError, KeyError, TypeError):
            continue
    return pruned

def get_24h_stats(history):
    if not history:
        return 0.0, 0, 0.0

    values = [entry["pm25"] for entry in history if "pm25" in entry]
    count = len(values)
    avg = sum(values) / count if count > 0 else 0.0
    percentage = round((count / 24) * 100, 2)

    return round(avg, 2), count, percentage

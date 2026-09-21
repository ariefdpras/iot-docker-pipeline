import json
import time
import ssl
import paho.mqtt.client as mqtt

from .config import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_TOPIC, MQTT_USE_TLS, DEVICE_ID

def publish_mqtt(payload):
    try:
        client_id = f"{DEVICE_ID}_{int(time.time())}"
        try:
            client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION1,
                client_id=client_id
            )
        except (AttributeError, TypeError):
            client = mqtt.Client(client_id=client_id)

        if MQTT_USERNAME and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

        if MQTT_USE_TLS:
            client.tls_set(tls_version=ssl.PROTOCOL_TLS)

        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

        message = json.dumps(payload, ensure_ascii=False)
        result = client.publish(MQTT_TOPIC, message, qos=1)
        result.wait_for_publish(timeout=10)

        client.disconnect()
        print(f"  ✅ MQTT: Published ke {MQTT_BROKER}:{MQTT_PORT}/{MQTT_TOPIC}")
        return True

    except Exception as e:
        print(f"  ✗ MQTT Error: {e}")
        return False

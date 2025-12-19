
#!/usr/bin/env python3
import json
import time
import uuid
import pika
from pika.exceptions import AMQPConnectionError, StreamLostError

VIP_HOST = "192.168.215.100"
VIP_PORT = 5672
VHOST = "/"

USER = "test_user"     
PASS = "abc123"

QUEUE = "q.repl_test"
SEND_INTERVAL_SEC = 1.0

def connect():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=VIP_HOST,
            port=VIP_PORT,
            virtual_host=VHOST,
            credentials=pika.PlainCredentials(USER, PASS),
            heartbeat=30,
            blocked_connection_timeout=30,
            connection_attempts=1,
            retry_delay=0,
            client_properties={"connection_name": "pub-1s-repl-test"},
        )
    )

def main():
    conn = None
    ch = None
    seq = 0

    while True:
        try:
            if conn is None or conn.is_closed or ch is None or ch.is_closed:
                if conn:
                    try: conn.close()
                    except: pass
                print("[PUB] connecting...")
                conn = connect()
                ch = conn.channel()

                print(f"[PUB] connected -> publishing to queue={QUEUE} via VIP {VIP_HOST}:{VIP_PORT}")

            seq += 1
            msg_id = str(uuid.uuid4())
            send_ts_ms = int(time.time() * 1000)

            payload = {"id": msg_id, "seq": seq, "send_ts_ms": send_ts_ms}
            ch.basic_publish(
                exchange="",
                routing_key=QUEUE,
                body=json.dumps(payload).encode("utf-8"),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2,  # persistent
                    message_id=msg_id,
                    timestamp=int(time.time()),
                ),
            )

            print(f"[PUB] sent seq={seq} id={msg_id} ts_ms={send_ts_ms} -> {QUEUE}")
            time.sleep(SEND_INTERVAL_SEC)

        except (AMQPConnectionError, StreamLostError, ConnectionResetError, BrokenPipeError) as e:
            print(f"[PUB] connection error: {type(e).__name__}: {e} -> reconnecting")
            conn = None
            ch = None
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[PUB] exit")
            try:
                if conn: conn.close()
            except: pass
            return

if __name__ == "__main__":
    main()

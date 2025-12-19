#!/usr/bin/env python3
import json
import time
import pika
from pika.exceptions import AMQPConnectionError, StreamLostError

VIP_HOST = "192.168.215.100"
VIP_PORT = 5672
VHOST = "/"

USER = "test_user"      # sửa đúng user của bạn
PASS = "abc123"  # sửa đúng password

QUEUE = "q.repl_test"
PREFETCH = 50

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
            client_properties={"connection_name": "sub-repl-test"},
        )
    )

def main():
    conn = None
    ch = None

    while True:
        try:
            if conn is None or conn.is_closed or ch is None or ch.is_closed:
                if conn:
                    try: conn.close()
                    except: pass
                print("[SUB] connecting...")
                conn = connect()
                ch = conn.channel()
                ch.basic_qos(prefetch_count=PREFETCH)
                print(f"[SUB] connected -> consuming from queue={QUEUE}")

            def on_msg(channel, method, properties, body):
                recv_ts_ms = int(time.time() * 1000)
                try:
                    data = json.loads(body.decode("utf-8"))
                    send_ts_ms = int(data.get("send_ts_ms", recv_ts_ms))
                    seq = data.get("seq", "?")
                    msg_id = data.get("id", "?")
                    latency_ms = recv_ts_ms - send_ts_ms
                    print(f"[SUB] got seq={seq} id={msg_id} latency={latency_ms}ms (send={send_ts_ms} recv={recv_ts_ms})")
                except Exception as e:
                    print(f"[SUB] got non-json message: {e}")
                channel.basic_ack(delivery_tag=method.delivery_tag)

            ch.basic_consume(queue=QUEUE, on_message_callback=on_msg, auto_ack=False)
            ch.start_consuming()

        except (AMQPConnectionError, StreamLostError, ConnectionResetError, BrokenPipeError) as e:
            print(f"[SUB] connection error: {type(e).__name__}: {e} -> reconnecting")
            try:
                if conn: conn.close()
            except: pass
            conn = None
            ch = None
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[SUB] exit")
            try:
                if conn: conn.close()
            except: pass
            return

if __name__ == "__main__":
    main()

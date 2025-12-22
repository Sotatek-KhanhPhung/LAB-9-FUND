# File pub.py

```sh
VIP_HOST = "192.168.215.100"
VIP_PORT = 5672
VHOST = "/"

USER = "test_user"     
PASS = "abc123"

QUEUE = "q.repl_test"
SEND_INTERVAL_SEC = 1.0
```

- **VIP_HOST:** địa chỉ VIP của Keepalived
- **VIP_PORT:** Port để truy cập vào Queue
- **VHOST, USER, PASS:** thông tin user RabbitMQ
- **QUEUE:** queue sẽ send message đến
- **SEND_INTERVAL_SEC:** khoảng thời gian giữa các lần gửi

```sh
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
            client_properties={"connection_name":"pub-1s-repl-test"},
        )
    )
```

- **heartbeat:** phát hiện kết nối TCP bị đứt. Nếu trong 30 giây vẫn có publish, consume, ack, không cần gửi heartbeat. Nếu trong 30 giây không có gì sẽ gửi heartbeat, client và broker mỗi bên sẽ gửi một heartbeat frame
- **blocked_connection_timeout:** thời gian tối đa client chịu connection bị broker block. Nếu sau thời gian này, connection bị đóng và sẽ reconnect
- **connection_attempts, retry_delay:** kiểm soát reconnect

# Result
<img width="1512" height="947" alt="Image" src="https://github.com/user-attachments/assets/95b13f91-bc25-4e69-bdae-6b9b42fc169d" />

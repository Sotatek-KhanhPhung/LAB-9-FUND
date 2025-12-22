# LAB 9 FUND
## RabbitMQ Install
```sh
sudo apt update
sudo apt install -y curl gnupg apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/rabbitmq-erlang.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/rabbitmq-server.gpg
cat <<'EOF' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
deb [signed-by=/usr/share/keyrings/rabbitmq-erlang.gpg] https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/deb/ubuntu jammy main
deb [signed-by=/usr/share/keyrings/rabbitmq-server.gpg] https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/deb/ubuntu jammy main
EOF
sudo apt update
sudo apt install -y erlang-base erlang-asn1 erlang-crypto erlang-eldap erlang-inets erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl rabbitmq-server
```
## Enable RabbitMQ UI Management
```sh
sudo rabbitmq-plugins enable rabbitmq_management
sudo systemctl enable --now rabbitmq-server
```

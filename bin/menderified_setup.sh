#!/bin/bash

sudo apt-get update
sudo apt install -y raspberrypi-kernel-headers libmnl-dev libelf-dev build-essential git curl
sudo apt install -y wireguard supervisor pigpio python-pigpio python-smbus i2c-tools
sudo apt-get -y upgrade
sudo mkdir -p /opt/udaan/drishti/data
sudo chmod -R 777 /opt/udaan/drishti
sudo supervisorctl update
sudo supervisorctl reread
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
wget https://udhardware.blob.core.windows.net/init/config.txt -O /boot/config.txt
sudo su -
cd /etc/wireguard
wg genkey | tee privatekey | wg pubkey > publickey
PRIVATE_KEY=$(cat privatekey)
PUBLIC_KEY=$(cat publickey)
# TODO: Remove username pw
IP=$(curl -X POST -u udaan:UdaanRobotics@2020 https://hardware.infra.udaan.io/getIP --data-urlencode "publickey=${PUBLIC_KEY}")
cat << EOF > wg0.conf
[Interface]
PrivateKey = $PRIVATE_KEY
Address = $IP/24

[Peer]
PublicKey = EP1zf+BUVmOJbVEf0MPZl5OE57D2/Go6Letrusaeuxk=
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 20.193.149.188:61951
PersistentKeepalive = 25
EOF

wg-quick up wg0
systemctl enable wg-quick@wg0.service

sudo sed -i_bkp "s/raspberrypi/drishtipi/" /etc/hosts && sudo sed -i_bkp "s/raspberrypi/drishtipi/" /etc/hostname
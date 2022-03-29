#!/bin/bash


## Build Image
## enable ssh
## Boot Image
## Set wifi, locale from UI

sudo apt-get update
sudo apt install -y raspberrypi-kernel-headers libmnl-dev libelf-dev build-essential git curl
sudo apt install -y wireguard supervisor pigpio python-pigpio python3-pigpio python-smbus i2c-tools
sudo apt-get -y upgrade
sudo sed -i_bkp "s/raspberrypi/drishtipi/" /etc/hosts && sudo sed -i_bkp "s/raspberrypi/drishtipi/" /etc/hostname

## Enable camera
#Add the following to config.txt

start_x=1
gpu_mem=256
disable_camera_led=1

## Self Machine
ssh-copy-id -i ~/.ssh/id_rsa.pub  pi@raspberrypi.local
scp conf/wpa_supplicant.conf pi@raspberrypi.local:/tmp/wpa_supplicant.conf
ssh pi@raspberrypi.local "sudo cp /tmp/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf"
ssh pi@raspberrypi.local "sudo reboot now"



## Setup wireguard
sudo su -
cd /etc/wireguard
wg genkey | tee privatekey | wg pubkey > publickey
PRIVATE_KEY=$(cat privatekey)
IP=$1
cat << EOF > wg0.conf
[Interface]
PrivateKey = $PRIVATE_KEY
Address = $IP/24

[Peer]
PublicKey = EP1zf+BUVmOJbVEf0MPZl5OE57D2/Go6Letrusaeuxk=
AllowedIPs = 10.45.5.0/24
Endpoint = 20.193.149.188:61951
PersistentKeepalive = 25
EOF

wg-quick up wg0
systemctl enable wg-quick@wg0.service

## setup drishti
sudo mkdir -p /opt/udaan/drishti/data
sudo chmod -R 777 /opt/udaan/drishti

# Self machine
./bin/deploy.sh drishtipi.local

## Setup supervisor
ssh pi@drishtipi.local "sudo ln /opt/udaan/drishti/conf/drishti_supervisor.conf /etc/supervisor/conf.d/"
ssh pi@drishtipi.local "sudo supervisorctl update"
ssh pi@drishtipi.local "sudo supervisorctl reread"

## Enable camera
##Add the following to config.txt
#start_x=1
#gpu_mem=256
#disable_camera_led=1

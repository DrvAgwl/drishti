#!/bin/bash

wget -q -O- https://get.mender.io/ | sudo bash -s -- --demo && \
sudo bash -c 'DEVICE_TYPE="raspberrypi4" && \
TENANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW5kZXIudGVuYW50IjoiNjAxYWM4OGU5N2E1ODI4OTc4NmM1ZjM5IiwiaXNzIjoiTWVuZGVyIiwic3ViIjoiNjAxYWM4OGU5N2E1ODI4OTc4NmM1ZjM5In0.YuX9-YzsG3WHrnHQmvSY8Tt8MHWteJf9nNkwfxP6A3JzpFtjaQHXhxx1O592aIrSNwY6ekmrOFKgVdpglhuLg-V955LtkDQ7xnYjZTll4uFpPgK3MRqvDeSPUkpxeT7q8Z-1nZA7hwo9VR7SMBLJZRP7ldNCfj4aW1xSsmxg-o5k0XWl9e1I9TlRVTT_hjJDkkmliPi9n9irSjS_GO7TrQXNLv4eId2A4tkWhKlii0VxgpSVxqHaaRhqMHeIPN5AoZ6WB7QPm1kKFrAD1Fhj0dTrHFN4Pws8CPvkT9FOayQ7UcSh3n0tKO7duW6ApNkbePMB11lq3opT8nPGH-pPLNcvshJMPtW3ze9OERUGKtTzVQBKsQLwtgLSYynPLdTY9s5xTb-wIKzf_UAppuAwbWioQLa_qZtnBp8Wfo4L7DSXSU3M5_8aXt5qTcvDdzfiKBHE7pCrJLcsOhXS61zSW8lQD8i9lbjPHi2xeA3vqQwBvipMViR-6Q3aa5NVQaoS" && \
echo "Running mender setup for hosted.mender.io" && \
mender setup \
  --device-type $DEVICE_TYPE \
  --quiet --hosted-mender \
  --tenant-token $TENANT_TOKEN \
  --retry-poll 30 \
  --update-poll 5 \
  --inventory-poll 5 && \
systemctl restart mender-client && \
(cat > /etc/mender/mender-connect.conf << EOF
{
  "ServerCertificate": "/usr/share/doc/mender-client/examples/demo.crt",
  "User": "pi",
  "ShellCommand": "/bin/bash"
}
EOF
) && wget https://udhardware.blob.core.windows.net/init/mender-device-identity -O /usr/share/mender/identity/mender-device-identity && \
chmod +x /usr/share/mender/identity/mender-device-identity && \
systemctl restart mender-connect && \
echo "Done!"'
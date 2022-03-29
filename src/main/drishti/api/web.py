import json
import logging
import time
from datetime import datetime
import os
from pathlib import Path

import pigpio
import requests

from src.main.commons.hal.camera import Camera
from src.main.commons.utils.network_utils import get_device_id
from dotenv import load_dotenv

from src.main.commons.utils.utils import base_init

env_path = Path('/opt/udaan/drishti/src/.env')
load_dotenv(verbose=True, dotenv_path=env_path)
logger = logging.getLogger("drishti_web")


class Web:
    def __init__(self, base_url, lcd=None):
        self.base_url = base_url
        self.lcd = lcd

    ## 200 Cool
    ## 400 Buzzer

    def is_do_valid(self, order_id):
        url = self.base_url + '/isOrderValid/' + order_id
        return requests.get(url)

    def is_crate_code_valid(self, crate_barcode):
        url = self.base_url + '/isCrateValid/' + crate_barcode
        return requests.get(url)

    def is_correct_sku(self, sku_id):
        url = self.base_url + '/isSkuIdValid/' + sku_id
        return requests.get(url)

    def get_skuname(self, sku_id):
        url = self.base_url + '/skuName/' + sku_id
        return requests.get(url)

    def send_outbound_packet(self, image_path, crate_barcode, order_id, total_weight):
        start_time = time.time()
        url = self.base_url + '/scan_event/'
        logger.debug("Sending Packet " + url)
        fresh_crate_event = {
            "warehouseId": os.getenv('WAREHOUSE_ID'),
            "crateBarcode": crate_barcode,
            "stage": os.getenv('STAGE'),
            "deviceId": get_device_id(),
            "createdAt": datetime.utcnow().isoformat(),
            'totalWeight': total_weight,
            "orderId": order_id,
        }

        if image_path is not None:
            files = {
                'scanEvent': (None, json.dumps(fresh_crate_event), 'application/json'),
                'imageData': (os.path.basename(image_path), open(image_path, 'rb'), 'application/octet-stream')
            }
        else:
            files = {
                'scanEvent': (None, json.dumps(fresh_crate_event), 'application/json'),
            }

        logger.info(files)
        try:
            response = requests.post(url, files=files)
            logger.info("Request time: " + str(time.time() - start_time))
            return response
        except TimeoutError:
            logger.error("Timeout Exception")
            logger.info("Request time: " + str(time.time() - start_time))
            self.lcd.put_line(3, "Timeout! Try Again")
            return

    def send_inbound_packet(self, image_path, crate_barcode, irn_id, sku_id,
                            filled_crate_weight):
        start_time = time.time()
        url = self.base_url + '/scan_event/'
        logger.debug("Sending Packet " + url)
        fresh_crate_event = {
            "warehouseId": os.getenv('WAREHOUSE_ID'),
            "crateBarcode": crate_barcode,
            "stage": os.getenv('STAGE'),
            "deviceId": get_device_id(),
            "createdAt": datetime.utcnow().isoformat(),
            'irnId': irn_id,
            'tareWeight': 0,
            'skuId': sku_id,
            'netWeight': filled_crate_weight
        }

        if image_path is not None:
            files = {
                'scanEvent': (None, json.dumps(fresh_crate_event), 'application/json'),
                'imageData': (os.path.basename(image_path), open(image_path, 'rb'), 'application/octet-stream')
            }
        else:
            files = {
                'scanEvent': (None, json.dumps(fresh_crate_event), 'application/json'),
            }

        logger.info(files)
        try:
            response = requests.post(url, files=files)
            logger.info("Request time: " + str(time.time() - start_time))
            return response
        except TimeoutError:
            logger.error("Timeout Exception")
            logger.info("Request time: " + str(time.time() - start_time))
            self.lcd.put_line(3, "Timeout! Try Again")
            return


if __name__ == "__main__":
    base_init()
    web_client = Web("http://10.45.5.5/drishti/fresh-crate-scanner")
    # image_path = "/Users/soumyadeepmukherjee/Downloads/02-16-2021-03-25-05.jpg"
    crate_barcode = 'FR-TST-B20-00264'
    order_id = 'DOO-BUYERRES50'
    total_weight = '1.245'
    sku_id = "S1367557"
    image_path = '/opt/udaan/drishti/data/03-19-2021-19-41-37.jpg'
    pi = pigpio.pi('')
    camera = Camera(pi, True)

    for i in range(1, 5):
        start_time = time.time()
        image_path = camera.capture()
        response = web_client.send_outbound_packet(image_path, crate_barcode, order_id, total_weight)
        # response = web_client.get_skuname('S8L6C4856B2890E9B844')
        logger.info("Total time: " + str(time.time() - start_time))

# response = web_client.is_crate_code_valid(crate_barcode)
# logger.debug(response.text.encode('utf8'))
# response = web_client.is_do_valid(order_id)
# logger.debug(response.text.encode('utf8'))
# response = web_client.is_correct_sku(sku_id)
# logger.debug(response.text.encode('utf8'))


# curl --location --request POST 'http://10.45.5.5/drishti/fresh-crate-scanner/scan_event' --header 'Content-Type: multipart/form-data' --form 'request={"warehouseId": "ORG3432NFDFSDBN321","crateBarcode": "FR-TST-FSDF-32243","createdAt": "17-02-2021 12:34:454","machineNumber": "32","totalWeight": "90.34","orderId": "DOO-ODFCUKK", "stage": "INBOUND"};type=application/json' --form 'imageData=@/Users/manikantakondeti/Downloads/download.jpeg'
# curl -w "@curl-format.txt" -o /dev/null --location --request POST 'http://10.45.5.5/drishti/fresh-crate-scanner/scan_event' --header 'Content-Type: multipart/form-data' --form 'scanEvent={"warehouseId": "ORG3432NFDFSDBN321","crateBarcode": "FR-TST-FSDF-32243","createdAt": "17-02-2021 12:34:454","deviceId": "32","totalWeight": "90.34","orderId": "DOO-ODFCUKK", "stage": "OUTBOUND"};type=application/json' --form 'imageData=@/Users/soumyadeepmukherjee/Downloads/a.jpg'

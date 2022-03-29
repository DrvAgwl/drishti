import logging
import os
import time

from src.main.commons.utils.utils import is_camera_enabled
from src.main.drishti.components.scanner import BarcodeType

logger = logging.getLogger("drishti_inbound")

sku_id = -1
sku_name = -1
irn_id = -1
is_empty_crate_scanned = False
empty_crate_weight = 0.0
empty_barcode = -1


def reset_state():
    global is_empty_crate_scanned
    global sku_id
    global irn_id
    global empty_crate_weight
    global empty_barcode
    sku_id = -1
    irn_id = -1
    is_empty_crate_scanned = False
    empty_crate_weight = 0.0


def reset_inbound(lcd):
    reset_state()
    logger.info("Got Reset")
    lcd.put_line(1, "Reseting Workflow.")
    lcd.put_line(2, "Start Over")
    return


def inbound_loop(lcd, barcode_scanner, weight_catcher, buzzer, web_client, camera=None):
    global is_empty_crate_scanned
    global sku_id
    global irn_id
    global empty_crate_weight
    global empty_barcode
    global sku_name

    logger.info("Starting Inbound")
    barcode = barcode_scanner.wait_till_barcode_read()
    barcode_type = barcode_scanner.get_barcode_type(barcode)
    lcd.clear()
    logger.info("Barcode: " + str(barcode))
    if barcode_type == BarcodeType.IRN_ID.value or barcode_type == BarcodeType.RTO.value or \
            barcode_type == BarcodeType.OPENING_STOCK.value:
        buzzer.switch_off()
        sku_id = -1
        irn_id = -1
        logger.info("Scanned: " + str(barcode_type))
        irn_id = barcode
        lcd.put_line(0, "I:" + irn_id)
        sku_id = -1
        lcd.put_line(1, "Scan Sku ID")
        logger.info(irn_id)

    elif barcode_type == BarcodeType.SKU_ID.value:
        buzzer.switch_off()
        logger.info("Scanned: " + str(barcode_type))
        if irn_id == -1:
            lcd.put_line(1, "Scan IRN ID")
            return
        else:
            sku_id = barcode
            empty_barcode = barcode
            response = web_client.get_skuname(sku_id)
            if response.status_code != 200:
                buzzer.error_beep()
                sku_name = "Error"
            else:
                sku_name = response.text.encode('utf-8').decode()
            logger.info("skuname: " + sku_name)
            lcd.put_line(0, "I:" + irn_id)
            lcd.put_line(1, "S:" + sku_name)

    elif barcode_type == BarcodeType.CRATE_ID.value:
        buzzer.switch_off()
        logger.info("Scanned: " + str(barcode_type))
        if irn_id == -1:
            lcd.put_line(1, "IRN ID Missing")
            logger.info("Missing IRN ID")
            return
        elif sku_id == -1:
            lcd.put_line(1, "SKU ID Missing")
            logger.info("Missing SKU ID")
            return
        else:
            lcd.put_line(0, 'I:' + irn_id)
            lcd.put_line(1, "S: " + sku_name)

        lcd.put_line(2, "Crt:" + str(barcode))
        time.sleep(1)

        lcd.put_line(3, "Capturing. Dont touch.")
        buzzer.single_beep()
        filled_crate_weight = weight_catcher.get_weight()
        logger.info('Filled: ' + str(filled_crate_weight))
        image_path = None
        if is_camera_enabled():
            image_path = camera.capture()
        lcd.put_line(3, "Change and Wait!")
        buzzer.double_beep()

        if filled_crate_weight <= 0.001:
            buzzer.switch_on()
            logger.error("Weight Error: Couldn't capture weight")
            lcd.put_line(0, "Invalid Weight")
            lcd.put_line(1, "Scan again")
            return

        if is_camera_enabled():
            camera.close_leds()
        buzzer.switch_on()
        response = web_client.send_inbound_packet(image_path, barcode, irn_id, sku_id,filled_crate_weight)

        if response.status_code != 200:
            logger.info("ERROR: "+str(response.status_code))
            buzzer.switch_on()
            lcd.put_line(3, "ERROR: Scan Again")
            if is_camera_enabled():
                camera.clean_image(image_path)

            return

        response_wms = str(response.text.encode('UTF-8').decode('utf-8'))
        logger.info("Response: " + str(response.text.encode('UTF-8').decode('utf-8')))
        logger.info("Response Status Code: " + str(response.status_code))
        buzzer.switch_off()

        if response_wms != 'HAPPY':
            logger.info("ERROR: "+response_wms)
            buzzer.switch_on()
            display_message = response_wms
            lcd.put_line(3, "Error: " + display_message)
        else:
            buzzer.double_beep()
            lcd.put_line(3, "Done. Scan Next!")
        if is_camera_enabled():
            camera.clean_image(image_path)

    elif barcode_type == BarcodeType.RESET.value:
        return reset_inbound(lcd)
    else:
        return barcode_scanner.invalid_scan()

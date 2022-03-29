import logging
import time

from src.main.commons.utils.utils import is_camera_enabled
from src.main.drishti.components.scanner import BarcodeType

logger = logging.getLogger("drishti_outbound")

order_id = -1


def outbound_loop(lcd, barcode_scanner, weight_catcher, buzzer, web_client, camera=None):
    global order_id
    logger.info("Starting Outbound")
    barcode = barcode_scanner.wait_till_barcode_read()
    lcd.clear()
    barcode_type = barcode_scanner.get_barcode_type(barcode)
    logger.info("Barcode: " + str(barcode))
    logger.debug("Order Id: " + str(order_id))
    if barcode_type == BarcodeType.ORDER_ID.value:
        logger.info("Scanned: " + str(barcode_type))
        order_id = barcode
        lcd.put_line(0, "O:" + order_id)
        lcd.put_line(1, "Scan Crate")
        logger.info(order_id)
    elif barcode_type == BarcodeType.CRATE_ID.value:
        start_time = time.time()
        logger.info("Scanned: " + str(barcode_type))
        if order_id == -1:
            lcd.put_line(1, "Please Scan Order Id")
            logger.info("No Order Id Scan")
            return
        else:
            lcd.put_line(0, "O: " + order_id)
        lcd.put_line(1, "Crt:" + str(barcode))
        lcd.put_line(2, "Capturing. Please Wait")
        if is_camera_enabled():
            camera.open_camera()
        time.sleep(1)
        captured_weight = weight_catcher.get_weight()
        if captured_weight <= 0.001:
            buzzer.error_beep()
            logger.error("Weight Error: Crate weight is zero.")
            lcd.put_line(0, "Invalid Crate Weight")
            lcd.put_line(1, "Clear Scale")
            lcd.put_line(2, "Manual Tare")
            lcd.put_line(3, "Rescan")
            return
        logger.info("Captured weight: " + str(captured_weight))
        if is_camera_enabled():
            image_path = camera.capture()
        else:
            image_path = None
        buzzer.double_beep()
        buzzer.switch_on()
        if is_camera_enabled():
            camera.close_leds()
        lcd.put_line(2, "Change Crate and Wait")
        response = web_client.send_outbound_packet(image_path, barcode, order_id, captured_weight)
        logger.info("Response: " + str(response.text.encode('UTF-8')))
        buzzer.switch_off()
        if response.status_code != 200:
            buzzer.error_beep()
            display_message = response.text.encode('utf-8').decode()
            lcd.put_line(3, "Error: " + display_message)
        else:
            buzzer.double_beep()
            lcd.put_line(2, "Done. Scan Next!")
        logger.info("Crate Time for %s: " + str(time.time()-start_time), barcode)
        if is_camera_enabled():
            camera.clean_image(image_path)
    else:
        logger.info("Invalid Barcode")
        lcd.put_line(1, "Invalid Barcode." + str(barcode))
        lcd.put_line(2, "Please fix")

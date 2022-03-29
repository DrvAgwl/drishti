import sys
import logging
from enum import Enum
from errno import ENOENT

hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l',
       16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x',
       28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0',
       43: ' ',
       44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}
hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L',
        16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X',
        28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')',
        43: ' ',
        44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

logger = logging.getLogger("drishti_scanner")


class BarcodeType(Enum):
    ORDER_ID = 1
    IRN_ID = 2
    CRATE_ID = 3
    SKU_ID = 4
    RESET = 5
    OPENING_STOCK = 6
    RTO = 7


barcode_map = {
    'DOO': BarcodeType.ORDER_ID,
    'IRN': BarcodeType.IRN_ID,
    'FR': BarcodeType.CRATE_ID,
    'S': BarcodeType.SKU_ID,
    'UDAANRESET': BarcodeType.RESET,
    'OPENINGSTOCK': BarcodeType.OPENING_STOCK,
    'RTO': BarcodeType.RTO
}


class BarcodeScanner:
    def __init__(self, lcd):
        logger.info("Barcode Scanner Init")
        try:
            self.fp = open('/dev/hidraw0', 'rb')
        except OSError as e:
            logger.error("hidraw0 failed. Looking for hidraw1")
            if e.errno == ENOENT:
                try:
                    self.fp = open('/dev/hidraw1', 'rb')
                except Exception as e:
                    raise e
            else:
                raise e
        except Exception as e:
            logger.error("Barcode Scanner Not Found", e)
            lcd.put_line(1, "Scanner Not Found!")
            lcd.put_line(2, "Fix and Restart")
        self.ss = ""
        self.shift = False
        self.done = False
        self.lcd = lcd

    def wait_till_barcode_read(self):
        logger.debug("waiting for barcode read")
        while not self.done:
            buffer = self.fp.read(8)
            for c in buffer:
                if c > 0:
                    ##  40 is carriage return which signifies
                    ##  we are done looking for characters
                    if c == 40:
                        self.done = True
                        break
                    ##  If we are shifted then we have to
                    ##  use the hid2 characters.
                    if self.shift:
                        ## If it is a '2' then it is the shift key
                        if c == 2:
                            shift = True
                        ## if not a 2 then lookup the mapping
                        else:
                            self.ss += hid2[c]
                            self.shift = False
                    ##  If we are not shifted then use
                    ##  the hid characters
                    else:
                        ## If it is a '2' then it is the shift key
                        if c == 2:
                            self.shift = True
                        ## if not a 2 then lookup the mapping
                        else:
                            self.ss += hid[c]
            self.shift = False
            logger.debug(self.ss)
        self.done = False
        barcode = self.ss
        self.ss = ""
        logger.debug("Read barcode: " + str(barcode))
        return barcode

    def get_barcode_type(self, barcode):
        logger.debug("Type check: " + barcode)
        barcode = barcode.replace(" ", "").upper()
        for barcode_prefix in barcode_map.keys():
            barcode_prefix = barcode_prefix.upper()
            if barcode.startswith(barcode_prefix):
                barcode_type = barcode_map[barcode_prefix].value
                logger.debug("barcode type: " + str(barcode_type))
                return barcode_type
        return ""

    def invalid_scan(self):
        logger.info("Invalid Scan")
        self.lcd.put_line(1, "Invalid Scan")
        self.lcd.put_line(2, "Start Over from IRN")
        return

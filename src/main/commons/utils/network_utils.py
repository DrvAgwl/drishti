import logging
import socket
import fcntl
import struct

logger = logging.getLogger("drishti_network_utils")


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifname = ifname[:15].encode('utf-8')
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def get_device_id():
    ip = get_ip_address('wg0')
    logger.debug(ip)
    return ip.strip().replace('.', '-')

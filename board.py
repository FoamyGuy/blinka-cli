import json
import logging
import os.path
import re
import urlutil

# This is a mapping from the text in boot_log.txt to the board ID used in the firmware filenames

boards = {
    "Adafruit Feather M0 RFM69 with samd21g18": "feather_m0_rfm69",
    "Adafruit PyPortal Titano with samd51j20": "pyportal_titano",

    #"SparkFun Qwiic Micro with samd21e18": "sparkfun_qwiic_micro_no_flash",
    #"SparkFun Qwiic Micro with samd21e18": "sparkfun_qwiic_micro_with_flash",

    "Adafruit Feather M4 CAN with same51j19a": "feather_m4_can",
    "TG-Boards' Datalore IP M4 with samd51j19": "datalore_ip_m4",
    "Arduino MKR1300 with samd21g18": "arduino_mkr1300",
    "SparkFun SAMD21 Dev Breakout with samd21g18": "sparkfun_samd21_dev",
    "Sprite_v2b with samd51G19": "kicksat-sprite",
    "J&J Studios datum-Distance with None": "datum_distance",
    "Adafruit Feather M0 Express with Crickit libraries with samd21g18": "feather_m0_express_crickit",
    "SAM E54 Xplained Pro with same54p20": "same54_xplained",
    "PewPew M4 with samd51g19": "pewpew_m4",
    "SparkFun LUMIDrive with samd21g18": "sparkfun_lumidrive",
    "PyCubedv04 with samd51j19": "pycubed",
    "J&J Studios datum-IMU with None": "datum_imu",
    "@sarfata shIRtty with samd21e18": "shirtty",
    "SparkFun Thing Plus - SAMD51 with samd51j20": "sparkfun_samd51_thing_plus",
    "PewPew 10.2 with samd21e18": "pewpew10",
    "Robo HAT MM1 M4 with samd51g19": "robohatmm1_m4",
    "Adafruit Grand Central M4 Express with samd51p20": "grandcentral_m4_express",
    "Adafruit PyGamer with samd51j20": "pygamer_advance",
    "CP32-M4 with samd51j20": "cp32-m4",
    "Adafruit CircuitPlayground Express with displayio with samd21g18": "circuitplayground_express_displayio",
    "Electronic Cats NFC Copy Cat with samd21e18": "nfc_copy_cat",
    "Arduino Zero with samd21g18": "arduino_zero",
    "Adafruit Monster M4SK with samd51j19": "monster_m4sk",
    "DynOSSAT-EDU-OBC with samd51j20": "dynossat_edu_obc",
    "Adafruit Matrix Portal M4 with samd51j19": "matrixportal_m4",
    "Adafruit CircuitPlayground Express with Crickit libraries with samd21g18": "circuitplayground_express_crickit",
    "XinaBox CS11 with samd21g18": "xinabox_cs11",
    "ndGarage[n°]Bit6:FeatherSnow with samd21e18": "ndgarage_ndbit6",
    "Winterbloom Big Honking Button with samd21g18": "winterbloom_big_honking_button",
    "Adafruit BLM Badge with samd21e18": "blm_badge",
    "8086 Commander with samd21g18": "8086_commander",
    "Adafruit Feather M4 Express with samd51j19": "feather_m4_express",
    "Arduino MKR Zero with samd21g18": "arduino_mkrzero",
    "Adafruit Feather M0 Basic with samd21g18": "feather_m0_basic",
    "SparkFun RedBoard Turbo with samd21g18": "sparkfun_redboard_turbo",
    "ndGarage[n°] Bit6: FeatherSnow-v2 with samd21e18": "ndgarage_ndbit6_v2",
    "Adafruit Gemma M0 with samd21e18": "gemma_m0",
    "Adafruit Feather M0 Express with samd21g18": "feather_m0_express",
    "The Open Book Feather with samd51j19": "openbook_m4",
    "Adafruit PyPortal with samd51j20": "pyportal",
    "keithp.com snekboard with samd21g18": "snekboard",
    "Adafruit Trellis M4 Express with samd51g19": "trellis_m4_express",
    "LoC BeR M4 base board with samd51g19": "loc_ber_m4_base_board",
    "Meow Meow with samd21g18": "meowmeow",
    "Adafruit Metro M0 Express with samd21g18": "metro_m0_express",
    "Serpente with samd21e18": "serpente",
    "Adafruit QT Py M0 with samd21e18": "qtpy_m0",
    "SparkFun SAMD21 Mini Breakout with samd21g18": "sparkfun_samd21_mini",
    "BDMICRO VINA-D51 with samd51n20": "bdmicro_vina_d51",
    "Capable Robot Programmable USB Hub with samd51g19": "capablerobot_usbhub",
    "Adafruit PyGamer with samd51j19": "pygamer",
    "DynOSSAT-EDU-EPS with samd21g18": "dynossat_edu_eps",
    "XinaBox CC03 with samd21g18": "xinabox_cc03",
    "Adafruit ItsyBitsy M4 Express with samd51g19": "itsybitsy_m4_express",
    "Seeeduino XIAO with samd21g18": "seeeduino_xiao",
    "Adafruit Trinket M0 with samd21e18": "trinket_m0",
    "Adafruit Feather M0 RFM9x with samd21g18": "feather_m0_rfm9x",
    "J&J Studios datum-Light with None": "datum_light",
    "Adafruit Feather RadioFruit Zigbee with samr21g18": "feather_radiofruit_zigbee",
    "BDMICRO VINA-D21 with samd21g18": "bdmicro_vina_d21",
    "Adafruit Feather M0 Adalogger with samd21g18": "feather_m0_adalogger",
    "Fluff M0 with samd21e18": "fluff_m0",
    "Adafruit Metro M4 Express with samd51j19": "metro_m4_express",
    "Adafruit Metro M4 Airlift Lite with samd51j19": "metro_m4_airlift_lite",
    "J&J Studios datum-Weather with None": "datum_weather",
    "Adafruit pIRKey M0 with samd21e18": "pirkey_m0",
    "Adafruit ItsyBitsy M0 Express with samd21g18": "itsybitsy_m0_express",
    "HalloWing M0 Express with samd21g18": "hallowing_m0_express",
    "AloriumTech Evo M51 with samd51p19": "aloriumtech_evo_m51",
    "UARTLogger II with samd51j19": "uartlogger2",
    "Trinket M0 Haxpress with samd21e18": "trinket_m0_haxpress",
    "Adafruit QT Py M0 Haxpress with samd21e18": "qtpy_m0_haxpress",
    "Arduino Nano 33 IoT with samd21g18": "arduino_nano_33_iot",
    "CircuitBrains Basic with samd21e18": "circuitbrains_basic_m0",
    "Winterbloom Sol with samd51j20": "winterbloom_sol",
    "Escornabot Makech with samd21g18": "escornabot_makech",
    "Adafruit Hallowing M4 Express with samd51j19": "hallowing_m4_express",
    "Electronic Cats CatWAN USBStick with samd21e18": "catwan_usbstick",
    "SAM32v26 with samd51j20": "sam32",
    "Electronic Cats Bast Pro Mini M0 with samd21e18": "bast_pro_mini_m0",
    "PicoPlanet with samd21e18": "picoplanet",
    "Adafruit CircuitPlayground Express with samd21g18": "circuitplayground_express",
    "Adafruit PyRuler with samd21e18": "pyruler",
    "Seeeduino Wio Terminal with samd51p19": "seeeduino_wio_terminal",
    "PyCubedv04-MRAM with samd51j19": "pycubed_mram",
    "Adafruit Pybadge Airlift with samd51j20": "pybadge_airlift",
    "Hacked Feather M0 Express with 8Mbyte SPI flash with samd21g18": "feather_m0_supersized",
    "Adafruit Pybadge with samd51j19": "pybadge",
    "Mini SAM M4 with samd51g19": "mini_sam_m4",
    "uChip with samd21e18": "uchip",
    "Cedar Grove StringCar M0 Express with samd21e18": "stringcar_m0_express",
    "CircuitBrains Deluxe with samd51j19": "circuitbrains_deluxe_m4",
    "uGame10 with samd21e18": "ugame10",
}

download_url_template = "https://downloads.circuitpython.org/bin/{board}/{locale}/adafruit-circuitpython-{board}-{locale}-{version}.{extension}"

def get_boot_string(root):
    # Read first line of boot_out.txt
    filename = os.path.join(root, 'boot_out.txt')
    logging.debug("Reading line from %s" % filename)
    with open(filename, 'r') as f:
        return f.readline()

def identify(root):
    boot_string = get_boot_string(root)
    # Format is:
    # Adafruit CircuitPython 5.3.1 on 2020-07-13; Adafruit Feather M0 RFM69 with samd21g18
    parts = [item.strip() for item in boot_string.split(';')]
    boot_board = parts[1]
    logging.debug("boot_board = \"%s\"" % boot_board)

    version = re.search(r"\s+(\d\S+)", parts[0]).group(1)

    return (version, boards[boot_board])

def get_version_metadata(board_id):
    # This file has the metadata for all the boards. Go get it and find our board in it.
    url = 'https://raw.githubusercontent.com/adafruit/circuitpython-org/master/_data/files.json'
    logging.debug("Fetching metadata from %s" % url)
    all_metadata = urlutil.get_json_from_url(url)
    return next((x for x in all_metadata if x['id'] == board_id), None)

def get_download_url(version, board, extension, locale):
    return download_url_template.format(version = version, locale = locale, extension = extension, board = board)
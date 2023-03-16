import os

from dotenv import load_dotenv

load_dotenv()

BLUETOOTH_DEVICE = os.getenv("BLUETOOTH_DEVICE", "")
TERMINAL = os.getenv("TERMINAL", "")
WIFI_SSID = os.getenv("WIFI_SSID", "")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD", "")

CUR_DIR = os.path.realpath(os.path.dirname(__file__))

import os

from dotenv import load_dotenv

load_dotenv()

BLUETOOTH_DEVICE = os.getenv("BLUETOOTH_DEVICE")

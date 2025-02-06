import os
import dotenv

dotenv.load_dotenv()

SBER_UID = os.getenv('SBER_UID')
SBER_AUTH = os.getenv('SBER_AUTH')

TG_TOKEN = os.getenv('TG_TOKEN')
import os
import dotenv
from dataclasses import dataclass

dotenv.load_dotenv()

@dataclass
class Models:
    chat: str
    vision: str

@dataclass
class Sber:
    uid: str
    auth: str

@dataclass
class Qwen:
    token: str
    model: str
    visual: str

@dataclass
class Telegram:
    token: str
    chat_id: int


class Config:
    models: Models = Models(
        chat=os.getenv('MODEL_CHAT'),
        vision=os.getenv('MODEL_VISION')
    )
    sber: Sber = Sber(
        uid=os.getenv('SBER_UID'),
        auth=os.getenv('SBER_AUTH')
    )
    qwen: Qwen = Qwen(
        token=os.getenv("QWEN_TOKEN"),
        model=os.getenv("QWEN_MODEL"),
        visual=os.getenv("QWEN_VISUAL")
    )
    telegram: Telegram = Telegram(
        token=os.getenv('TG_TOKEN'),
        chat_id=int(os.getenv('TG_CHAT_ID'))
    )

config = Config()
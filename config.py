import os
import dotenv
from dataclasses import dataclass

dotenv.load_dotenv()

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
import json
from dataclasses import dataclass

@dataclass
class Prompts:
    chat: str
    vision: str
    translator: str

with open('prompts.json', encoding="utf-8") as file:
    prompts_dict = json.load(file)

prompts = Prompts(
    chat = prompts_dict.get("chat"),
    vision = prompts_dict.get("vision"),
    translator = prompts_dict.get("translator")
)

if __name__ == "__main__":
    print(prompts)
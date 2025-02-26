# gycha_tg
### Бот-комментатор для TG каналов
Бот использует связку трёх нейросетевых моделей: GigaChat Lite, goekdenizguelmez/JOSIEFIED-Qwen2.5:1.5b, moondream:0.5b.

## Установка
**Требования:** Python 3.11.0, 6Гб ОЗУ.

Устанавливаем ollama, goekdenizguelmez/JOSIEFIED-Qwen2.5:1.5b и moondream
```sh
curl -fsSL https://ollama.com/install.sh | sh
ollama run goekdenizguelmez/JOSIEFIED-Qwen2.5:1.5b
/bye
ollama run moondream
/bye
```
Устанавливаем tesseract для распознавания текста
```sh
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-eng
sudo apt install tesseract-ocr-rus
```
Устанавливаем бота и его зависимости
```sh
git clone https://github.com/buvanenko/gycha_tg.git
cd gycha_tg
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
Создаём файл .env со следующим содержимым:
```
SBER_UID = UID из консоли GigaChat
SBER_AUTH = Токен авторизации из той же консоли
TG_TOKEN = Токен бота Telegram
TG_CHAT_ID = Айди чата с комментариями Telegram
MODEL_CHAT = Модель для чата (в Гыче используется goekdenizguelmez/JOSIEFIED-Qwen2.5:1.5b)
MODEL_VISION = Модель для распознавания изображений (в Гыче используется moondream)
```
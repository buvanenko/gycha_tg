# gycha_tg
### Бот-комментатор для TG каналов
Бот использует связку трёх нейросетевых моделей: GigaChat, qwen2:1b, moondream:0.5b.

## Установка
**Требования:** Python 3.11.0, 6Гб ОЗУ.

Устанавливаем ollama и qwen2:1b
```sh
curl -fsSL https://ollama.com/install.sh | sh
ollama run qwen2:1.5b
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
Устанавливаем moondream:0.5b
```sh
wget https://huggingface.co/vikhyatk/moondream2/resolve/9dddae84d54db4ac56fe37817aeaeb502ed083e2/moondream-0_5b-int8.mf.gz?download=true
```
Создаём файл .env со следующим содержимым:
```
SBER_UID = UID из консоли GigaChat
SBER_AUTH = Токен авторизации из той же консоли
TG_TOKEN = Токен бота Telegram
```
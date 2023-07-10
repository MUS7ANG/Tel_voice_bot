from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from gtts import gTTS
from dotenv import load_dotenv
import os
load_dotenv()

bot = Bot(os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add("English 🇺🇸").add("Русский 🇷🇺").add("Français 🇫🇷").add("Español 🇪🇸")

current_language = "en"
def convert(msg=None):
    text = msg.text
    filename = f'{msg.chat.id}_{msg.message_id}.mp3'
    audio = gTTS(text=text, lang=current_language, slow=False)
    audio.save(filename)
    with open(filename, 'rb') as f:
        bot.send_audio(chat_id=msg.chat.id, audio=f)
    os.remove(filename)
@dp.message_handler(commands=["start"])
async def say_hi(msg: types.Message):
    await msg.answer("Ok, choose your language", reply_markup=main)

@dp.message_handler(text="English 🇺🇸")
async def eng(msg: types.Message):
    global current_language
    current_language = "en"
    await msg.reply(f'Установлен язык: {current_language}')
    await convert()

@dp.message_handler(text="Русский 🇷🇺")
async def rus(msg: types.Message):
    global current_language
    current_language = "ru"
    await msg.reply(f'Установлен язык: {current_language}')
    await convert()

@dp.message_handler(text="Français 🇫🇷")
async def fran(msg: types.Message):
    global current_language
    current_language = "fr"
    await msg.reply(f'Установлен язык: {current_language}')
    await convert()

@dp.message_handler(text="Español 🇪🇸")
async def esp(msg: types.Message):
    global current_language
    current_language = "es"
    await msg.reply(f'Установлен язык: {current_language}')
    await convert()

@dp.message_handler(content_types=types.ContentType.TEXT)
async def theend(msg: types.Message):
    await msg.reply("converted successfully!")
    await msg.reply(f'Установлен язык: {current_language}')
    text = msg.text
    filename = f'{msg.chat.id}_{msg.message_id}.mp3'

    audio = gTTS(text=text, lang=current_language, slow=False)
    audio.save(filename)

    with open(filename, 'rb') as f:
        await bot.send_audio(chat_id=msg.chat.id, audio=f)

    os.remove(filename)


if __name__ == '__main__':
    executor.start_polling(dp)
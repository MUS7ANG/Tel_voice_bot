from aiogram import Bot, Dispatcher, executor, types
from TOKEN import Token
from gtts import gTTS
import os

API_TOKEN = Token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def send_voice(msg: types.Message) -> None:
    current_language = 'en'

    if msg.reply_to_message:
        current_language = msg.reply_to_message.text
        await msg.reply('Установлен язык: {current_language}')
    else:
        await msg.reply('Язык по умолчанию: английский')

    text = msg.text
    filename = f'{msg.chat.id}_{msg.message_id}.mp3'

    audio = gTTS(text=text, lang=current_language)
    audio.save(filename)

    with open(filename, 'rb') as f:
        await bot.send_audio(chat_id=msg.chat.id, audio=f)

    os.remove(filename)


if __name__ == '__main__':
    executor.start_polling(dp)







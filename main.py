import logging
import shutil

import config
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import os
import time
import MatchStrings as match
import GetVkMusic as do

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def instruction(message: Message):
    await message.answer("Hi, I'm VibesBot powered by Alin. Send vk playlist url or youtube video url to download it")


@dp.message_handler()
async def send_music(message: Message):
    time_start = time.time()
    initial_path = os.getcwd()
    name_dir = 'music_vk' + str(time_start) + '\\'
    path = initial_path + '\\' + name_dir
    artist_path = path + 'artist\\'
    title_path = path + 'title\\'
    print(initial_path, path, artist_path, title_path)
    try:
        if not os.path.isfile(initial_path + "\\" + "restart_point.txt"):
            await message.answer("Starting downloading")
        await do.get_music(user_id=match.get_user_id(message.text),
                           album_id=match.get_album_id(message.text),
                           acces_url=message.text,
                           time=time_start)
        for i in os.listdir(path):
            try:
                print(i)
                if os.path.isfile(path + i):
                    music = open(path + i, 'rb')
                    title = open(title_path + i.replace(".mp3", ".txt"))
                    artist = open(artist_path + i.replace(".mp3", ".txt"))
                    await message.answer_audio(music, title=title.readline(),
                                               performer=artist.readline())
                    title.close()
                    artist.close()
            except PermissionError as e:
                do.traceback.print_exc()
                print(e)
    except do.vk_api.exceptions.AccessDenied as e:
        print(e)
        await message.answer("You don't have access to current playlist")
    if not os.path.isfile(initial_path + "\\" + "restart_point.txt"):
        await bot.delete_message(chat_id=message.chat.id, message_id=int(message.message_id) + 1)
    else:
        os.remove(f"{initial_path}\\restart_point.txt")
    await message.delete()
    os.chdir(initial_path)
    shutil.rmtree(artist_path)
    shutil.rmtree(title_path)
    shutil.rmtree(path)
    time_finish = time.time()
    print(time_finish - time_start)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

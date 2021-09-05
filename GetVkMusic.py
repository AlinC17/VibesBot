import os
import shutil
import traceback
from subprocess import Popen
import json

import requests
import vk_api
from vk_api import audio

login = '+37378021755'
password = 'prog17it'
my_id = '647908525'

vk_session = vk_api.VkApi(login=login, password=password)
vk_session.auth()
vk_audio = audio.VkAudio(vk_session)


async def get_music(user_id, acces_url, album_id, time):
    REQUEST_STATUS_CODE = 200
    initial_path = os.getcwd()
    name_dir = 'music_vk' + str(time) + '\\'
    path = initial_path + '\\' + name_dir
    artist_path = path + 'artist\\'
    title_path = path + 'title\\'
    try:
        print(path)

        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(artist_path):
            os.makedirs(artist_path)

        if not os.path.exists(title_path):
            os.makedirs(title_path)

        count = 1

        for i in vk_audio.get(owner_id=user_id, access_hash=acces_url, album_id=album_id):
            try:
                r = requests.get(i["url"])
                if r.status_code == REQUEST_STATUS_CODE:
                    print(i)
                    os.chdir(path)
                    with open(str(count) + '.mp3', 'wb') as output_file:
                        output_file.write(r.content)
                        r.close()
                    os.chdir(artist_path)
                    with open(str(count) + '.txt', 'w+') as artist:
                        artist.write(i['artist'])
                        artist.close()
                    os.chdir(title_path)
                    with open(str(count) + '.txt', 'w+') as title:
                        title.write(i['title'])
                        title.close()
                    count += 1
            except OSError as e:
                traceback.print_exc()
                print(e)
                print("Something went wrong with: " + i["artist"] + '_' + i["title"])
    except json.decoder.JSONDecodeError:
        print("Restarting...")
        os.chdir(initial_path)
        shutil.rmtree(artist_path)
        shutil.rmtree(title_path)
        shutil.rmtree(path)
        open("restart_point.txt", 'w')
        p = Popen('python main.py', shell=True)
        p.wait()

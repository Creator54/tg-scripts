#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 "with python3Packages; [ telethon tqdm ]"

import os, json
from tqdm import tqdm
from pprint import pprint
from telethon import TelegramClient

data = json.load(open("tgData.json", "r")) #create tgData.json file with api_id, api_hash, path attributes https://my.telegram.org
client = TelegramClient("anon", data["api_id"], data["api_hash"])

def callback(current, total): # Printing download progress
    global pbar
    global prev_curr
    pbar.update(current-prev_curr)
    prev_curr = current

async def main():
    global pbar
    global prev_curr
    async for message in client.iter_messages("me",reverse=True): #seq is from 1st message to last message i.e. oldest to recent
        try:
            if message.file.name and message.media and not message.file.name in os.listdir(data["path"]):
                prev_curr = 0
                print("Downloading [ " + str(message.file.name) + " ]")
                pbar = tqdm(total=message.file.size, unit='B', unit_scale=True)
                path = await message.download_media("{}/{}".format(data["path"],message.file.name), progress_callback=callback)
                pbar.close()
        except:
            print("There were some errors fetching the files !")
            os.remove(data["path"]+message.file.name) #currently idk how to resume so remove the old file cuz incomplete
with client:
    client.loop.run_until_complete(main())

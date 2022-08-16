#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 "with python3Packages; [ python-telegram-bot ]"
#only downloads files <= 20 MB

import json
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

bot_token = json.load(open("tgData.json", "r"))["bot_token"] #create tgData.json file with api_id, api_hash, path attributes

def file_handler(Update, context: CallbackContext):
    file = context.bot.getFile(Update.message.document.file_id)
    print("Downloading File: " + str(Update.message.document.file_name))
    file.download(custom_path=Update.message.document.file_name)
    print("Download Complete !"

def main():
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.document, file_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

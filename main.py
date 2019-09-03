import sys
import json
import telebot


from BLL.Services.BotDialogService import BotDialogService


# Get data from config file ####################################################################
with open(sys.path[1] + "/config.json") as json_file:
    data = json.load(json_file)
postgres = data["postgres"]
telegram_bot = data["telegram_bot"]


# Create bot instance ##########################################################################
bot = telebot.TeleBot(telegram_bot["token"])

# Run User Interface
dialog = BotDialogService(postgres)
dialog.main_dialog(bot)

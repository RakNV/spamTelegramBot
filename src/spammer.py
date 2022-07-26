from scraper.client import client
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
from src.scraper.config import message, sleep_time
import time
import sys


class Spammer:

    def message_users(self, users):
        for user in users:
            receiver = InputPeerUser(user["id"], user["access_hash"])
            try:
                print("Sending Message to:", user["name"])
                client.send_message(receiver, message.format(user["name"]))
                print("Waiting {} seconds".format(sleep_time))
                time.sleep(sleep_time)
            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print("Error:", e)
                print("Trying to continue...")
                continue

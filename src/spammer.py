from scraper.client import authorized_clients
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, FloodWaitError
from src.scraper.config import message, sleep_time
import time
import sys
import re
import csv


class Spammer:
    messaged_users = []

    @staticmethod
    def save_messaged_user(users):
        with open("members_messaged.csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'name'])
            for user in users:
                writer.writerow([user["username"],
                                 user["id"],
                                 user["access_hash"],
                                 user["name"]])

    @staticmethod
    def load_messaged_users():
        with open("members_messaged.csv", encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {'username': row[0],
                        'id': int(row[1]),
                        'access_hash': int(row[2]),
                        'name': row[3]}
                Spammer.messaged_users.append(user)

    @staticmethod
    def is_messaged(user):
        if user in Spammer.messaged_users:
            return True
        else:
            return False

    @staticmethod
    def message_user(client, user, receiver):
        print("Sending Message to:", user["name"])
        client.send_message(receiver, message.format(user["name"]))
        Spammer.messaged_users.append(user)
        print(user)
        print("Waiting {} seconds".format(sleep_time))
        time.sleep(sleep_time)

    @staticmethod
    def wait_flood(e):
        print(e.message)
        print("Trying to continue...")
        wait_time = int(re.search(r'\d+', e.message).group(0))
        print(f"Waiting {wait_time} seconds")
        time.sleep(wait_time)

    def message_all_users(self, users):
        Spammer.load_messaged_users()
        for user in users:
            receiver = InputPeerUser(user["id"], user["access_hash"])
            try:
                if Spammer.is_messaged(user):
                    continue
                else:
                    Spammer.message_user(authorized_clients[1],user, receiver)

            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                for i in range(0,len(authorized_clients)):
                    authorized_clients[i].disconnect()
                sys.exit()

            except FloodWaitError as e:
                Spammer.wait_flood(e)
                Spammer.message_user(user, receiver)
                Spammer.messaged_users.append(user)

            except Exception as e:
                print("Error:", e)
                print("Trying to continue...")
                continue

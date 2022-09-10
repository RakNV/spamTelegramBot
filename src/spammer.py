from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, FloodWaitError
from src.scraper.config import message, sleep_time
import time
import re
import csv


class Spammer:
    messaged_users = []

    def __init__(self, client):
        self.client = client
        self.target_group = None
        self.all_participants = None

    def get_group(self, group_list, target_group_name):
        for group in group_list:
            if group.title == target_group_name:
                self.target_group = group

    def get_all_participants(self):
        """gets participants data from group,chat,channel, ect."""
        print('Fetching Members...')
        self.all_participants = self.client.tlclient.get_participants(self.target_group)
        users = []
        for user_data in self.all_participants:
            if user_data.username:
                username = user_data.username
            else:
                username = ""
            if user_data.first_name:
                first_name = user_data.first_name
            else:
                first_name = ""
            if user_data.last_name:
                last_name = user_data.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            user = {
                "username": username,
                "id": user_data.id,
                "access_hash": user_data.access_hash,
                "name": name
            }
            users.append(user)
        self.all_participants = users

    def message_45_users(self, users):
        Spammer.load_messaged_users()
        counter = 0
        for user in users:
            if counter == 45:
                break
            receiver = InputPeerUser(user["id"], user["access_hash"])
            try:
                if Spammer.is_messaged(user):
                    continue
                else:
                    self.message_user(user, receiver) # have to change THIS line of code authorized clients[index] change  to client argument in function
                    counter += 1

            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                self.client.disconnect()
                exit(1)

            except FloodWaitError as e:
                Spammer.wait_flood(e)
                Spammer.message_user(user, receiver)

    @staticmethod
    def is_messaged(user):
        ids = [messaged_user["id"] for messaged_user in Spammer.messaged_users]
        if user["id"] in ids:
            return True
        else:
            return False

    @staticmethod
    def save_messaged_user(users):
        with open("members_messaged.csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user_id', 'access_hash', 'name'])
            for user in users:
                writer.writerow([user['username'],
                                 user['id'],
                                 user['access_hash'],
                                 user['name']])

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
                if user in Spammer.messaged_users:
                    continue
                else:
                    Spammer.messaged_users.append(user)

    def message_user(self, user, receiver):
        print("Sending Message to:", user["name"])
        self.client.tlclient.send_message(receiver, message)
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



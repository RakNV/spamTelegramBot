import csv
from client import result, client


class Parser:
    chats = []
    groups = []

    def __init__(self):
        self.target_group = None
        self.all_participants = None

        Parser.chats.extend(result.chats)

        for chat in Parser.chats:
            try:
                if chat.megagroup:
                    Parser.groups.append(chat)
            except:
                continue

    @staticmethod
    def print_groups():
        """prints available groups for scraping"""
        print('Choose a group to scrape members from:')
        i = 0
        for g in Parser.groups:
            print(str(i) + '- ' + g.title)
            i += 1

    def choose_group(self):
        """takes int input for group you want to scrap"""
        g_index = input("Enter a Number: ")
        self.target_group = Parser.groups[int(g_index)]

    def get_participants(self):
        """gets participants data from group,chat,channel, ect."""
        print('Fetching Members...')
        self.all_participants = client.get_participants(self.target_group)

    def save_in_csv(self):
        """saves scrapped data in .csv file"""
        print('Saving In file...')
        with open("members.csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
            for user in self.all_participants:
                if user.username:
                    username = user.username
                else:
                    username = ""
                if user.first_name:
                    first_name = user.first_name
                else:
                    first_name = ""
                if user.last_name:
                    last_name = user.last_name
                else:
                    last_name = ""
                name = (first_name + ' ' + last_name).strip()
                writer.writerow([username,
                                 user.id,
                                 user.access_hash,
                                 name,
                                 self.target_group.title,
                                 self.target_group.id])
        print('Members scraped successfully.')



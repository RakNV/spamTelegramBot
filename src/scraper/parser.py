class Parser:
    groups = []
    available_chat_names = None
    target_chat = None
    client_chat = None

    def __init__(self, clients):
        self.target_group_name = None
        self.all_participants = None
        self.users = []
        self.clients_list = clients

    def get_chats(self):
        chats = []
        for client in self.clients_list:
            current_client_chats = []
            for chat in client.result.chats:
                try:
                    if chat.megagroup:
                        current_client_chats.append(chat)
                    else:
                        continue
                except:
                    continue
            chats.append(current_client_chats)
        target = self.is_in_common(chats)

        Parser.available_chat_names = target
        Parser.client_chat = zip(self.clients_list, target)

    @staticmethod
    def print_groups():
        """prints available groups for scraping"""
        print('Choose a group to scrape members from:')
        i = 0
        for g in Parser.available_chat_names[0]:
            print('[' + str(i) + ']' + '-' + g.title)
            i += 1

    def choose_group(self):
        """takes int input for group you want to scrap"""
        try:
            g_index = input("Enter a Number: ")
            self.target_group_name = Parser.available_chat_names[0][int(g_index)].title
        except IndexError:
            print("Choose available number!!!")
            g_index = input("Enter a Number: ")
            self.target_group_name = Parser.available_chat_names[0][int(g_index)].title

    @staticmethod
    def is_in_common(obj_list):
        organized_obj_list = []
        for obj in obj_list:
            new_obj = []
            for group in obj:
                new_obj.append(group.title)
            organized_obj_list.append(new_obj)

        if len(organized_obj_list) == 1:
            return organized_obj_list[0]
        tmp = set(organized_obj_list[0]).intersection(set(organized_obj_list[1]))
        for obj in organized_obj_list:
            tmp = tmp.intersection(obj)

        res = []
        for obj in obj_list:
            final = []
            for group in obj:
                if group.title in list(tmp):
                    final.append(group)
            res.append(final)
        return res

    def save_user_data(self):
        """saves scrapped data in list"""
        for entity in self.all_participants:
            name = (str(entity.first_name) + ' ' + str(entity.last_name)).strip()
            user = {
                'username': entity.username,
                'id': entity.id,
                'access_hash': entity.access_hash,
                'name': name
            }
            self.users.append(user)

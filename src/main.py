from src.scraper.client import connect_all_clients
from src.scraper.parser import Parser
from src.spammer import Spammer


def main():
    authorized_clients = connect_all_clients()
    ps = Parser(authorized_clients)

    ps.get_chats()
    print(ps.available_chat_names)
    ps.print_groups()
    ps.choose_group()
    print(ps.target_group_name)
    for client, group_list in ps.client_chat:
        sp = Spammer(client)
        sp.get_group(group_list=group_list, target_group_name=ps.target_group_name)
        sp.get_all_participants()
        sp.message_45_users(sp.all_participants)
        print(len(sp.messaged_users))
        sp.save_messaged_user(sp.messaged_users)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaving messaged users...")
        Spammer.save_messaged_user(Spammer.messaged_users)
        print("Exiting...")
        exit()


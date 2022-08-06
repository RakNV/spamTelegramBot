from scraper.parser import Parser
from spammer import Spammer
from scraper.client import authorized_clients

if __name__ == "__main__":
    try:
        ps = Parser()
        sp = Spammer()
        ps.print_groups()
        ps.choose_group()
        ps.get_participants()
        ps.save_in_csv()
        ps.csv_to_list()
        sp.message_all_users(ps.users)
        print("\n\nSaving messaged users...")
        Spammer.save_messaged_user(Spammer.messaged_users)
        print("Exiting...")
    except KeyboardInterrupt:
        print("\n\nSaving messaged users...")
        Spammer.save_messaged_user(Spammer.messaged_users)
        print("Exiting...")
        for i in range(0, len(authorized_clients)):
            authorized_clients[i].disconnect()
        exit()


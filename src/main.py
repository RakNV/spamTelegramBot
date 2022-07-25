from scraper.parser import Parser
from spammer import Spammer

if __name__ == "__main__":
    ps = Parser()
    sp = Spammer()
    ps.print_groups()
    ps.choose_group()
    ps.get_participants()
    ps.save_in_csv()
    ps.csv_to_list()
    print(ps.users)
    sp.message_users(ps.users)


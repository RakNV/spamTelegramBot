from parser import Parser


if __name__ == "__main__":
    ps = Parser()
    ps.print_groups()
    ps.choose_group()
    ps.get_participants()
    ps.save_in_csv()

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, PhoneCodeEmptyError, PhoneCodeExpiredError
import csv


class Client:

    def __init__(self, phone, api_id, api_hash):
        self.phone = phone
        self.api_id = api_id
        self.api_hash = api_hash
        self.tlclient = None
        self.result = None

# authorization happens here
    def client_connect(self, phone, api_id, api_hash):
        session_path = f"D:\projects\spamBot\src\Sessions\{phone}.session"
        file = open(session_path, "a")
        file.close()

        tlclient = TelegramClient(session_path, api_id, api_hash)
        tlclient.connect()

        while not tlclient.is_user_authorized():

            try:
                tlclient.send_code_request(phone)
                tlclient.sign_in(phone, input('Enter the code: '))

            except PhoneCodeEmptyError:
                print("Empty code! Try again!")

            except PhoneCodeInvalidError:
                print("Wrong code! Try again!")

            except PhoneCodeExpiredError:
                print("Code expired! Try again!")

        self.tlclient = tlclient

    def get_result(self):
        dialogues = self.tlclient(GetDialogsRequest(
            offset_date=None,  # last_date = None
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,  # chunk_size = 200
            hash=0
        ))
        self.result = dialogues


def get_client_data(file_path):
    clients_list = []
    with open(file_path) as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            client_data = {
                    "api_id": row[0],
                    "api_hash": row[1],
                    "phone": row[2]
                }
            clients_list.append(client_data)
        return clients_list


def connect_all_clients():
    file = "clients_data.csv"
    clients_to_authorize = get_client_data(file)
    authorized_clients_list = []
    for cl_data in clients_to_authorize:
        current_client = Client(phone=cl_data["phone"], api_id=cl_data["api_id"], api_hash=cl_data["api_hash"])
        current_client.client_connect(current_client.phone, current_client.api_id, current_client.api_hash)
        current_client.get_result()
        authorized_clients_list.append(current_client)
    print(authorized_clients_list)
    return authorized_clients_list

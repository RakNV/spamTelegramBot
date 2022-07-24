from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = 15741274
api_hash = '551169796fc89f6dfc844e0046b197c9'
phone = '+380982159820'


client = TelegramClient(phone, api_id, api_hash)

# authorization happens here
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

result = client(GetDialogsRequest(
    offset_date=None,  # last_date = None
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=200,  # chunk_size = 200
    hash=0
))

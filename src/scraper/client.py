from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = 15741274
api_hash = '551169796fc89f6dfc844e0046b197c9'
phone = '+380982159820'
message = 'Здравствуй, я тестирую прогу, сорри за сообщение'

clientl = TelegramClient(phone, api_id, api_hash)

# authorization happens here
clientl.connect()
if not clientl.is_user_authorized():
    clientl.send_code_request(phone)
    clientl.sign_in(phone, input('Enter the code: '))

result = clientl(GetDialogsRequest(
    offset_date=None,  # last_date = None
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=200,  # chunk_size = 200
    hash=0
))

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from src.scraper.config import phone, api_id, api_hash


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

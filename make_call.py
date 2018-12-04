# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from ivr_phone_tree_python.user_data_list import user_data_list
from dotenv import load_dotenv
load_dotenv()

phone_numbers = [user_data.phone_number for user_data in user_data_list]
# Your Account Sid and Auth Token from twilio.com/console

account_sid=os.getenv("account_sid")
auth_token=os.getenv("auth_token")
client = Client(account_sid, auth_token)

for number in phone_numbers:
    print("number", number)
    call = client.calls.create(
        url='https://a71b7195.ngrok.io/welcome',
        status_callback="https://a71b7195.ngrok.io/completed",
        status_callback_event=["completed"],
        status_callback_method=["POST"],
        to=number,
        from_='+15512136905',
        record=True,
        recording_channels="dual"
    )
    print(call.sid)

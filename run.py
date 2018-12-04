from flask import Flask
from twilio.twiml.voice_response import Gather, VoiceResponse, Say

_name_ = "_main_"
app = Flask(_name_)


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""

    response = VoiceResponse()
    response.say("Hey there weew!", voice='alice')

    return str(response)


if _name_ == "_main_":
    app.run(debug=True)

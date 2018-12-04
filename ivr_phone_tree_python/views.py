# import urllib3
import urllib.request
from .BaseThread import BaseThread
import requests
from flask import (
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for,
)
from twilio.twiml.voice_response import Gather, VoiceResponse

from ivr_phone_tree_python import app
from ivr_phone_tree_python.view_helpers import twiml
from .user_data_list import user_data_list

recording_url_list = []


@app.route('/')
@app.route('/ivr')
def home():
    return render_template('index.html')


@app.route('/welcome', methods=['POST'])
def welcome():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/menu')
    name = ""
    for user_data in user_data_list:
        number_called = request.form["Called"]
        if number_called == user_data.phone_number:
            name = user_data.name

    response_text = "Welcome {}, please choose from one of the following options. To hear your location history, please say 'locations'. To hear your purchase history please say 'purchases'".format(name)

    gather.say(response_text)
    response.append(gather)
    return twiml(response)


# @app.route('/purchases', methods=['POST'])
def _list_purchases(response):
    response_text = "I don't know what you have purchased."
    for user_data in user_data_list:
        number_called = request.form["Called"]
        if number_called == user_data.phone_number:
            response_text = user_data.purchases

    response.say(response_text)
    return response


# @app.route('/location', methods=['POST'])
def _list_locations(response):
    response_text = "I don't know where you have been."
    for user_data in user_data_list:
        number_called = request.form["Called"]
        if number_called == user_data.phone_number:
            response_text = user_data.locations

    response.say(response_text)
    return response

option_actions = {'location': {"function": _list_locations, 'keywords': ["location", "locations", "where"]},
                  'purchases': {"function": _list_purchases, 'keywords': ["purchase", "purchases", "history", "purchase history"]}}


@app.route('/completed', methods=['POST'])
def completed():
    response = VoiceResponse()
    # recording_url_list.append(request.form["RecordingUrl"])
    mp3_url = request.form["RecordingUrl"]+".mp3"
    filename = mp3_url.split("/")[-1]
    #kxfilename = "jimmy2.mp3"
    print("filename:"+filename)
    print("mp3_url:"+mp3_url)
    r = requests.get(mp3_url)

    with open(filename, 'wb') as f:
        f.write(r.content)
        f.close()
    # urllib.request.urlretrieve(mp3_url, filename)
    return '', 204


@app.route('/menu', methods=['POST'])
def menu():
    selected_option = request.form["SpeechResult"]

    for option in option_actions:
        if selected_option in option_actions[option]["keywords"]:
            response = VoiceResponse()
            option_actions[option]["function"](response)
            return twiml(response)
    return _redirect_welcome()

def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('welcome'))

    return twiml(response)

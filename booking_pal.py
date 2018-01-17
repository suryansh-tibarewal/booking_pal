from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from datetime import datetime
import requests
import urllib
import re
import random
from transitions import Machine
from transitions import State
import json
from difflib import SequenceMatcher

# --------------------------------------------------------------------------------------------
# INITIALISATION

app = Flask(__name__)
ask = Ask(app, "/alexa")

@ask.launch
def new_ask():
    welcome = render_template('welcome')
    reprompt = render_template('reprompt')
    return question(welcome) \
        .reprompt(reprompt)

# --------------------------------------------------------------------------------------------

#states=[
#    State(name='initial', on_entry=welcome()),
#    State(name='manage_booking', outn_entry=manage_booking())
#    ]

# And some transitions between states. We're lazy, so we'll leave out
# the inverse phase transitions (freezing, condensation, etc.).
#transitions = [
#    { 'trigger': 'next', 'source': 'initial', 'dest': 'manage_booking' },
#    { 'trigger': 'back', 'source': 'manage_booking', 'dest': 'initial' },
#]

#machine = Machine(booking_pal, states=states, transitions=transitions, initial='initial')

@ask.intent('FollowUpWelcome')
def followUpWelcome():
    follow_up_welcome = render_template('follow_up_welcome')
    return question(follow_up_welcome)

@ask.intent('FollowUpActivities')
def followUpWelcome():
    follow_up_activities = render_template('follow_up_activities')
    return question(follow_up_activities)

@ask.intent('FollowUpThingsToDo')
def followUpWelcome():
    follow_up_things_to_do = render_template('follow_up_things_to_do')
    return question(follow_up_things_to_do)

@ask.intent('FollowUpInformationMuseum')
def followUpWelcome():
    follow_up_information_museum = render_template('follow_up_information_museum')
    return question(follow_up_information_museum)

@ask.intent('MuseumDetails')
def followUpWelcome():
    rijksmuseum_details = render_template('rijksmuseum_details')
    return question(rijksmuseum_details)


last_node = ""
def parse_json_file():
    json_file = None
    with open('info.json') as json_data:
        json_file = json.load(json_data)
    return json_file

json_file = parse_json_file()

def get_closest_mueseum(museum):
    word, cnt = None, 0
    for m in json_file['museums'].keys():
        print m
        temp = SequenceMatcher(None, museum, m).ratio()
        if temp >= cnt:
            cnt = temp
            word = m
    return word

@ask.intent("ListMuseums")
def list_museums():
    global last_node
    last_node = "ListMuseums"
    museums = ", ".join(json_file['museums'].keys())
    output = render_template('list_museums', museums=museums)
    return question(output)

@ask.intent("MuseumsOpeningTime")
def museums_opening_time(museum):
    global last_node
    last_node = "MuseumsOpeningTime"
    museum_guess = get_closest_mueseum(museum)
    session.attributes['current_museum'] = museum_guess
    time_range = json_file['museums'][museum_guess]["time_range"]
    output = render_template(
        'museum_ticket', museum=museum_guess, time_range=time_range)
    return question(output)

@ask.intent("NoThanks")
def museums_tickets_info():
    global last_node
    if last_node == "MuseumsOpeningTime":
        last_node = "NoThanksResendEmail"
        output = render_template('other_places')
        return question(output)


@ask.intent("YesThanks")
def yes_thanks():
    return question("Bye")
    

@ask.intent("BreweriesInfo")
def breweries_info():
    global last_node
    if last_node == "NoThanksResendEmail" or True:
        breweries = ", ".join(json_file['breweries'].keys())
        last_node = "ListBreweries"
        output = render_template('list_breweries', breweries=breweries)
        return question(output)

#@ask.intent('ReviewLatestIntent')
#def launchReview(show):
#    if (show is None):
#        reprompt_show = render_template("reprompt_show")
#        return question(reprompt_show)
#    else:
#        return statement(show) #\
            #.standard_card(title=review_title + " - " + score,
                            #text=description
                            #small_image_url=image_url,
                            #large_image_url=image_url)


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
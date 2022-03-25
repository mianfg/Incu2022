#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoMaker WebEx Bot
====================
WebEx bot that utilizes PictoMaker Lite API
More here: https://github.com/mianfg/pictomaker-lite
"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2022, mianfg"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "Creative Commons Zero v1.0 Universal"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "hello@mianfg.me"
__status__      = "Production"


import requests, database, urllib, json, os, datetime
from flask import Flask, make_response, request

botToken = '' # WebEx bot token
botMail = 'pictomaker@webex.bot'

header = {'content-type': 'application/json; charset=utf-8', 'authorization': f'Bearer {botToken}'}

# create database if not present
database_route = database.db_table_to_route('preferences')
if not os.path.exists(database_route):
    f = open(database_route, 'w')
    f.write('id,register_timestamp,language,background_color,font_color,uncolor,skin_tone,'+','.join([f'color_{pos}' for pos in ['VERB', 'NOUN', 'ADJ', 'ADV', 'DET', 'PRON', 'INTJ', 'CONJ', 'ADP', 'OTHER']])+'\n')
    f.close()

app = Flask(__name__)
app.secret_key = 's3cr3t' # make it more secret!
app.debug = True

def get_message(messageId):
    return requests.get(f'https://webexapis.com/v1/messages/{messageId}', headers=header, verify=True).json()

def register_user(id):
    if id != botMail:
        if id not in database.db_read('preferences').index:
            # we use email as id
            database.db_create('preferences', {
                'id': id,
                'register_timestamp': datetime.datetime.now(),
                # here are the default values
                'language': 'en',
                'background_color': 'white',
                'font_color': 'black',
                'uncolor': 'false',
                'skin_tone': 'mulatto',
                'color_VERB': "#ff6f00",
                'color_NOUN': "#d32f2f",
                'color_ADJ': "#2e7d32",
                'color_ADV': "#004d40",
                'color_DET': "#1565c0",
                'color_PRON': "#d32f2f",
                'color_INTJ': "#37474f",
                'color_CONJ': "#c2185b",
                'color_ADP': "#c2185b",
                'color_OTHER': "#eeeeee"
            })

def translate(text, _id):
    preferences = database.db_read('preferences').loc[_id]
    # get tokenization
    tokens = requests.get(
        'https://lite.pictomaker.mianfg.me/tokenize',
        params={'text': text, 'language': preferences['language']},
        headers={'content-type': 'application/json; charset=utf-8'}
    ).json()
    to_image = lambda token, preferences: \
        (f'https://api.arasaac.org/api/pictograms/{token["arasaac_ids"][0]}' \
        + f'?backgroundColor={preferences["background_color"]}&skin={preferences["skin_tone"]}' \
        + f'&color={"false" if preferences["uncolor"] else "true"}') if len(token['arasaac_ids']) > 0 else None
    cards = [{'text': token['text'], 'color': preferences[f'color_{token["pos"]}'], 'image': to_image(token, preferences)} for token in tokens]

    # get image based on config
    return f'https://lite.pictomaker.mianfg.me/generate?cards={urllib.parse.quote(json.dumps(cards))}' \
        + f'&background_color={preferences["background_color"]}&font_color={preferences["font_color"]}'

def respond(type, **kwargs):
    preferences = database.db_read('preferences').loc[kwargs['_id']]
    if type == 'help':
        response = 'Hello and welcome to PictoMaker!\n\n'
        response += 'Here are the commands you can use:\n'
        response += 'ℹ️ **/about**: more information about PictoMaker\n'
        response += '💬 **/translate**: translate a sentence into pictograms\n'
        response += '⚙️ **/preferences**: some preferences (here you can change the language!)\n\n'
        welcome_message = {
            'es': '¡Que tengas un buen día!',
            'en': 'Have a great day!',
            'pl': 'Miłego dnia!'
        }
        response += f'Try texting: */translate {welcome_message[preferences["language"]]}*'
        return response
    elif type == 'show_preferences':
        response = 'Here are your **preferences**:\n\n'
        response += f'👅 Preferred language (**language**): {preferences["language"]}\n'
        response += f'🎨 Preferred background color (**background_color**): {preferences["background_color"]}\n'
        response += f'🎨 Preferred font color (**font_color**): {preferences["font_color"]}\n'
        response += f'🖌️ Prefer to leave pictograms uncolored (**uncolor**): {"true" if preferences["uncolor"] else "false"}\n'
        response += f'👨 Preferred skin tone (**skin_tone**): {preferences["skin_tone"]}\n\n'
        response += '🎨 Part-of-speech tagging (syntactical analysis):\n'
        pos_descr = {'VERB': 'verbs', 'NOUN': 'nouns', 'ADJ': 'adjectives', 'ADV': 'adverbs',
            'DET': 'determinants', 'PRON': 'pronouns', 'INTJ': 'interjections',
            'CONJ': 'conjunctions', 'ADP': 'adpositions', 'OTHER': 'other'}
        for pos in pos_descr.keys():
            response += f' * {pos}, {pos_descr[pos]} (**color_{pos}**): {preferences["color_"+pos]}\n'
        response += '\nYou can modify these values by just simply inputting:\n'
        response += '> /preferences set <preference_name> <preference_value>\n\n'
        response += 'Where *preference_name* is the text in bold on the previous lines.\n\n'
        response += '**UNDER DEVELOPMENT.** You can currently only modify the values *language*, *uncolor* and *skin_tone*'
        return response
    elif type == 'set_preference':
        preferences = database.db_read('preferences').loc[kwargs['_id']].to_dict()
        if kwargs['_name'] == 'language':
            values = ['en', 'es', 'pl']
            if kwargs['_value'] in values:
                preferences[kwargs['_name']] = kwargs['_value']
                preferences['id'] = kwargs['_id']
                database.db_update('preferences', preferences)
                return f'Language correctly changed to {kwargs["_value"]}'
            else:
                return '**Error.** The value must be in: ' + ', '.join(values)
        if kwargs['_name'] == 'skin_tone':
            values = ['white', 'black', 'asian', 'mulatto', 'aztec']
            if kwargs['_value'] in values:
                preferences[kwargs['_name']] = kwargs['_value']
                preferences['id'] = kwargs['_id']
                database.db_update('preferences', preferences)
                return f'Skin tone correctly changed to {kwargs["_value"]}'
            else:
                return '**Error.** The value must be in: ' + ', '.join(values)
        if kwargs['_name'] == 'uncolor':
            values = ['true', 'false']
            if kwargs['_value'] in values:
                preferences[kwargs['_name']] = kwargs['_value']
                preferences['id'] = kwargs['_id']
                database.db_update('preferences', preferences)
                return f'Uncolor correctly changed to {kwargs["_value"]}'
            else:
                return '**Error.** The value must be in: ' + ', '.join(values)
    elif type == 'info':
        response = '**PictoMaker** is a project developed by [@mianfg](https://mianfg.me/en) 😀. You '
        response += 'can look at the source code of PictoMaker Lite (the API) [here](https://github.com/mianfg/pictomaker-lite) '
        response += 'and the source code of this WebEx bot [here](#). 👩‍💻\n\n'
        response += '🤷 **Why pictograms?**\n'
        response += 'Learning through pictograms is an essential tool for children with special '
        response += 'educational needs, as well as crutial for elder people with Alzheimer\'s disease '
        response += 'and dementia. I developed PictoMaker to make it easy for people to communicate '
        response += 'using the power of images.\n\n'
        response += '👓 **Why do a syntactical analysis?**\n'
        response += 'PictoMaker leverages the power of AI to lemmatize the different words you input '
        response += '(getting the basic form of the word) to search for the images, as well as it uses '
        response += 'it to construct a syntactical analysis tree and allow people (and especially children) '
        response += 'to better distinguish between words.\n\n'
        response += ' **Where are the pictograms coming from?**\n'
        response += 'All pictograms used by PictoMaker are property of [ARASAAC](https://arasaac.org/), '
        response += 'from the Aragonese Center of Augmentive and Alternative Communication (Spain).'
        return response
    else:
        raise ValueError('Incompatible respond type')

@app.route('/', methods=['POST'])
def index():
    try:
        data = request.json['data']
    except:
        return make_response('Invalid request', 400)
    
    try:
        message = get_message(data['id'])
    except:
        return make_response('Could not fetch message data', 400)
    
    register_user(message['personEmail'])
    response = {'toPersonEmail': message['personEmail']}

    if message['personEmail'] != botMail:
        # handle message
        if message['text'].startswith('/translate'):
            if len(message['text'].split()) > 1:
                response['files'] = [translate(message['text'][11:], message['personEmail'])]
                response['markdown'] = f"Here's your pictogram fresh from the bakery!"
            else:
                response['markdown'] = 'You must introduce a text to translate'
        elif message['text'].startswith('/preferences'):
            split_text = message['text'].split()
            if len(split_text) == 1:
                response['markdown'] = respond('show_preferences', _id=message['personEmail'])
            elif len(split_text) == 4 and split_text[1] == 'set':
                response['markdown'] = respond('set_preference', _id=message['personEmail'], _name=split_text[2], _value=split_text[3])
        elif message['text'].startswith('/about'):
            response['markdown'] = respond('info', _id=message['personEmail'])
        else:
            response['files'] = ['https://media.giphy.com/media/mW05nwEyXLP0Y/giphy.gif']
            response['markdown'] = respond('help', _id=message['personEmail'])
    
        requests.post('https://webexapis.com/v1/messages', data=json.dumps(response), headers=header, verify=True)
        return make_response('Executed successfully', 200)
    else:
        return make_response('Petition from bot', 400)

if __name__ == '__main__':
    # run app
    app.run(host='0.0.0.0', port=5040)

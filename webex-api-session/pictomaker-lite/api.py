#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoMaker Lite
===============
Lightweight API version of PictoMaker
"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2022, mianfg"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "Creative Commons Zero v1.0 Universal"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "hello@mianfg.me"
__status__      = "Production"


from flask import Flask, make_response, send_file
from flask import request, jsonify
import json
app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True

from src.images import PictoImageGenerator
from src.language import PictoLanguage

image_generator = PictoImageGenerator(
    font = "./static/fonts/escolar_bold.ttf",
    text_size = 90,
    card_dimensions = (600,750),
    image_margin = 50
)
language = PictoLanguage()

@app.route('/generate/', methods=['GET'])
def index():
    global image_generator

    try:
      cards = json.loads(request.args.get('cards'))
    except:
      return make_response("cards object not JSON-serializable", 400)

    if not cards:
      return make_response("cards object must be specified", 400)
    
    for card in cards:
      if not set(['text', 'color', 'image']).issubset(card.keys()):
        return make_response("cards object invalid", 400)
    
    io = image_generator.generate_PNG(cards)
    io.seek(0)
    return send_file(io, mimetype='image/png')

@app.route('/tokenize/', methods=['GET'])
def tokenize():
    global language

    text = request.args.get('text')
    lang = request.args.get('language')

    if not text:
        return make_response("text must be specified", 400)
    if not lang:
        return make_response("language must be specified", 400)
    print(tokens := language.tokenize(text, lang))

    return jsonify(tokens)


if __name__ == '__main__':
    """
    Main function
    """
    # run app
    app.run(host='0.0.0.0', port=5030)

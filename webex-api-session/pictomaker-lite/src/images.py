#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PictoImageGenerator
===================
This module generates images and files from card data
"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2022, mianfg"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "Creative Commons Zero v1.0 Universal"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "hello@mianfg.me"
__status__      = "Production"


# Python library imports
from PIL import Image, ImageOps, ImageDraw, ImageFont
#import fpdf
from io import BytesIO
import requests, zipfile


class PictoImageGenerator:
    def __init__(self, font, text_size, card_dimensions, image_margin):
        self.__font = font
        self.__text_size = text_size
        self.__card_dimensions = card_dimensions
        self.__image_margin = image_margin

    def generate_card(self, text, color, image):
        card_width, card_height = self.__card_dimensions
        image_margin = self.__image_margin
        image_dimensions = card_width - image_margin*2
        image_dimensions = (image_dimensions, image_dimensions)

        text_color = (0,0,0)

        img = Image.new('RGBA', (card_width, card_height), (255, 255, 255))

        try:
            picto = Image.open(requests.get(image, stream=True).raw)
        except:
            picto = Image.new('RGB', (card_width, card_height), (255,255,255))
        
        picto = ImageOps.fit(picto, image_dimensions, centering=(0.5,0.5)) # WIP check
        draw = ImageDraw.Draw(img)
        draw.rectangle([(self.__image_margin/4,self.__image_margin/4), (self.__card_dimensions[0]-self.__image_margin/4,self.__card_dimensions[1]-self.__image_margin/4)], fill=color)
        draw.rectangle([(3*self.__image_margin/4,3*self.__image_margin/4), (self.__card_dimensions[0]-3*self.__image_margin/4,self.__card_dimensions[1]-3*self.__image_margin/4)], fill=(255,255,255))

        picto = picto.resize(image_dimensions)
        img.paste(picto, (image_margin, image_margin))

        text_font = ImageFont.truetype(self.__font, self.__text_size)
        text_width, text_height = draw.textsize(text, font=text_font)
        draw.text((int((card_width-text_width)/2), image_margin*1.5 + image_dimensions[0]), text, text_color, font=text_font)

        bytes_io = BytesIO()
        img.save(bytes_io, "PNG")
        return bytes_io

    def generate_PNG(self, cards, join=False):
        # cards is a list of dict of keys: 'text', 'color', 'image'
        length = len(cards)
        _, cards_height = self.__card_dimensions

        if join:
            cards_width = self.__image_margin + (self.__card_dimensions[0] - self.__image_margin)*length
            cards_repeat = self.__card_dimensions[0] - self.__image_margin
        else:
            cards_width = self.__card_dimensions[0]*length
            cards_repeat = self.__card_dimensions[0]
        
        full = Image.new('RGB', (cards_width, cards_height), (255,255,255))

        i = 0
        for card in cards:
            img = self.generate_card(**card)
            #img.seek(0)
            card_img = Image.open(img)
            full.paste(card_img, (i*cards_repeat, 0))
            i += 1
        
        bytes_io = BytesIO()
        full.save(bytes_io, "PNG")
        
        return bytes_io

    def generate_ZIP(self, cards):
        beginning = "pictomaker-"
        files = []
        i = 0
        for card in cards:
            filename = beginning + str(i) + "_" + card['text'] + ".png"
            io = BytesIO()
            io = self.generate_card(**card)
            data = io.getvalue()
            io.close()
            files.append((filename, data))
            i += 1
        
        mem_io = BytesIO()

        with zipfile.ZipFile(mem_io, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.writestr(f[0], f[1])

        return mem_io

    @staticmethod
    def write_bytesio_to_file(filename, bytesio):
        with open(filename, "wb") as outfile:
            outfile.write(bytesio.getbuffer())

<p align="center">
    <a href="https://mianfg.me"><img src="https://github.com/mianfg/pictomaker-lite/blob/main/static/logos/logo.png?raw=true" alt="PictoMaker Lite" width="500px"></a>
</p>

<h1 align="center"><p align="center">PictoMaker Lite</h1></h1>
<p align="center" id="badges">
    <a href="https://github.com/mianfg/pictomaker-lite/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mianfg/pictomaker-lite" alt="License"></a> <a href="#"><img src="https://img.shields.io/github/languages/code-size/mianfg/pictomaker-lite" alt="Code size"></a> <a href="https://github.com/mianfg/pictomaker-lite/commits"><img src="https://img.shields.io/github/last-commit/mianfg/pictomaker-lite" alt="Last commit"></a> <a href="#"><img src="https://img.shields.io/badge/status-production-green" alt="More info"></a>
</p>

> Created by **Miguel Ángel Fernández Gutiérrez** (<https://mianfg.me/>)

A simple API to translate sentences into pictograms.

> This is a more advanced version of my previous [PictoMaker](https://github.com/mianfg/pictomaker).

## Description

This is a simple API that provides two endpoints:

* `/tokenize`, that syntactically analizes a sentence and lemmatizes its componentes.
* `/generate`, that generates a PNG image composed of pictograms.

### Some Q&A

###### 🤷 Why pictograms?

Learning through pictograms is an essential tool for children with special educational needs, as well as crutial for elder people with Alzheimer's disease and dementia. I developed PictoMaker to make it easy for people to communicate using the power of images.

###### 👓 Why do a syntactical analysis?

PictoMaker leverages the power of AI to lemmatize the different words you input (getting the basic form of the word) to search for the images, as well as it uses it to construct a syntactical analysis tree and allow people (and especially children) to better distinguish between words.

###### Where are the pictograms coming from?

All pictograms used by PictoMaker are property of [ARASAAC](https://arasaac.org/), from the Aragonese Center of Augmentive and Alternative Communication (Spain).

> This API extensively uses ARASAAC's [API](https://arasaac.org/developers/api).

## Usage cases

This API has been used:

* In [this Cisco WebEx bot](https://github.com/mianfg/Incu2022/tree/main/webex-api-session) developed for Cisco Incubator Program 9.0.

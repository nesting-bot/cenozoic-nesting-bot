
# Nesting Bot

This is a "Nesting Bot", used in the game The Cenozoic Era. It is a super scrappy prototype thrown together over the course of a week. It works by using a server admin account. Once in-game, it hooks up to both Discord and ChatGPT for "extras".

The base function of it is to provide grows and nests for players automatically, while storing and time-stamping chat logs. Players type `?command` in either Discord or in-game, and the bot completes the request automatically!

It does utilize your computer's mouse and keyboard, so you won't be able to do anything else while this is running. I would recommend putting it on an alternate PC for long-term usage.


## Installation

Look at the imports for the necessary libraries. Then just pip install whatever you're missing. Since it's thrown together, no venvs or actual best practices were used (:

- I even went so far as to simply run it out of the VSCode terminal so I could edit it on the fly.

After pip install'ing, then get PyTesseract .exe. The default path is in the code under tools.py

`'C:/Program Files/Tesseract-OCR/tesseract.exe'`


After you put your tesseract .exe there, then you need to hook up both Discord and ChatGPT. I put $5.00 into ChatGPT for a developer API, and it works alright. I spent about 2 cents ($0.02) over the course of a week, so it's cheap. 

I am running this on a 4k monitor, so all the chat logs and screengrabs are based off of the 4k resolution. If you have a 1080p or 1440p, then you'll need to change the screengrab locations accordingly. 

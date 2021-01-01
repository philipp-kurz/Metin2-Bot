# Metin2-Bot

This repo contains the code for Metin2 Online RPG bots - a personal project I did during the Christmas 2020 holidays!

An [elaborate project summary](https://philippkurz.net/?portfolio=online-rpg-bot) can be found on [my website](https://philippkurz.net/).

Two bots were implemented:
- Bravery Cape Bot

   - Prototype for interacting with the game UI
   - Sends key strokes and mouse presses to the game to automatically farm monsters for experience
   - Mostly an intermediate step for the Metin Farm Bot (see below)
   
- Metin (Snowman) Farm Bot

   - Takes sreenshots of the game client and pre-processes them using HSV filters
   - Detects snowmen using a Haar feature-based Cascade Classifiers
   - Multi-threaded bot implementation as state machine to farm snowmen automatically
   - Remote monitoring through Telegram Bot implementation

   ![Demo GIF](https://github.com/philipp-kurz/Metin2-Bot/blob/main/demo/demo.gif "Demo GIF")

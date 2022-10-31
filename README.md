# FISH - BOT

## Commands:

+ !FISH#loot - copy pasta all the dropped items after this to create a "loot message" for each item which players can react to when they need the item.
Reacting with a ✔ emote will result in the message getting pinned.
If the author / user that executed this command reacts with 🗑 the given message will be deleted.

+ !FISH#clean - deletes all loot messages that are not pinned. Adding "all" after this command will delete all loot messages.

## How to run:

### Running with python:

+ Clone the repository
+ python FISH.py

### Creating an executable:

+ Clone the repository
+ pyinstaller -F .\FISH.py
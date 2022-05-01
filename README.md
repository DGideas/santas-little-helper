# The "Santa's Little Helper" - Telegram helper bot
"Santa's Little Helper" is a Telegram helper bot could avoid spam and manage group chat.

# HOW-TO
## Use
1. Search @ideasLittleHelperBot via Telegram, and add it into your group
2. Grant this bot admin rights
3. `/active` this bot on group chat

## Development
1. create a Python virtual environment
2. `pip3 install -r requirements.txt && pip3 install -r requirements-dev.txt`

### Run unittest
1. create `local_settings.py` using `local_settings_example.py` as example
2. `python3 -m unittest discover -v` run all

If you want to add a new method to this bot framework, please use https://core.telegram.org/bots/api as reference.

### Set-up GitHub CI
1. from repo > settings > secrets, click "add secrets" button
2. 

## Host a Telegram bot
1. create a new Telegram bot using https://t.me/botfather
2. clone this repo & create a Python virtual environment
3. `pip3 install -r requirements.txt`
4. create `local_settings.py` using `local_settings_example.py` as example, you might read https://core.telegram.org/bots first.
5. run `main.py`
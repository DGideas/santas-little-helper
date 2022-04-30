# The "Santa's Little Helper" - Telegram helper bot
"Santa's Little Helper" is a Telegram helper bot could avoid spam and manage group chat.

# HOW-TO
## Use
1. create a Python virtual environment
2. `pip3 install -r requirements.txt`
3. create `local_settings.py` using `local_settings_example.py` as example

## Development
1. create a Python virtual environment
2. `pip3 install -r requirements.txt && pip3 install -r requirements-dev.txt`

### Run unittest
1. create `local_settings.py` using `local_settings_example.py` as example
2. `python3 -m unittest discover -v` run all

If you want to add a new method to this bot framework, please use https://core.telegram.org/bots/api as reference.

## Host a Telegram bot
1. create a new Telegram bot using https://t.me/botfather
2. 
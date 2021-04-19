# discord.py template project

This is a template project for discord.py-based Discord bots.
This only contains what I consider the essentials for getting a Discord-bot up and running.

The [Discord.py API documentation](https://discordpy.readthedocs.io/en/latest/)

# Why?

For quick and easy setup of discord.py projects.
Simple as that.

# Setup


In a python>=3.6 environment of your choice, run
```
python -m pip install -r requirements.txt
```
to install the necessary requirements.

Access the Discord Developer Portal at
https://discord.com/developers/applications
and create a new application.
Set up a bot for your new application and add the token to a .env file as
```
DISCORD_TOKEN = '<bot token here>'
```

Run the bot with
```
python base.py
```
It should output 

# License

[This project is under the MIT license.](LICENSE)
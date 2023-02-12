# Simple py-cord template

A template that is supposed to reduce the boilerplate you have to write to get a py-cord bot up
and running. Includes `black` for formatting and `python-dotenv` to support passing the bot token
via an environment variable. Also has a CodeQL Actions workflow for automatic security vulnerability
scanning.

## Starting the bot

* Create a virtual env with pipenv, venv, virtualenv, Docker or whatever you'd like.
* Install the dependencies with pip: pip install -r requirements.txt
* Run the bot with the following command: `TOKEN=yourdiscordbottokenhere python -m src`

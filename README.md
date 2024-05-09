# ANRdiscocatPOC

**BACKEND ONLY IMPLEMENTATION FROM MARCH 2024... NEW REPO UP**

The ever-elusive AnR Discocat idea that I've never quite implemented. Somehow able to do more than I ever have in a single day. I guess because I usually get too caught up in CSS lol. 

## Development

**The current implementation requires *two servers!*** You must run the Flask app from `app.py` *and* the [Spotify-Monthly-Listeners-API](https://github.com/toluooshy/Spotify-Monthly-Listeners-API) from `Spotify-Monthly-Listeners-API/main.py`, each running on ports 5000 and 8000s respectively.

My next task is looking to merge these before I dive much deeper in development.

Also, don't forget to **add the environment variables in `.env` to your dev environment!**

### How to Start

In one terminal, run:

`flask --app app run --debug`

In another, run:

`uvicorn main:spapi --reload`

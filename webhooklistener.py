import asyncio
import random
import os, re, aiohttp
from utils.db import db
from utils.defaults import guilddata, userdata
from discord.ext import commands
from random import choice as randchoice
from utils.dataIO import fileIO
import time
import dbl
import sys
import json
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def webhook():
    if request.method == 'GET':
        print("Solyx GET request?!")
        return '<h1>This is for top.gg only, what are you doing here?!</h1>'

    elif request.method == 'POST':
        data = request.json
        print("SOLYX VOTE: {}".format(request.json["user"]))

        userinfo = db.users.find_one({"_id": data['user']})
        # Account check
        if userinfo["class"] == "None" and userinfo["race"] == "None":
            return
        if request.json["isWeekend"] == "True":
            userinfo["voted"] = "weekend"
        else:
            userinfo["voted"] = "True"
        db.users.replace_one({"_id": data['user']}, userinfo, upsert=True)

        return '', 200

    else:
        abort(400)

if __name__ == "__main__":
    app.run(host='192.168.1.15', port=65000, threaded=True, debug=True) # will listen on port
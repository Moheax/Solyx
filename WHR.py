from quart import Quart, g, request, abort, render_template, session, redirect, url_for, flash, jsonify, send_file
from requests_oauthlib import OAuth2Session
from pymongo import MongoClient
import requests
from utils.db import db

settings = dataIO.load_json(config)

app = Quart(__name__)


@app.route('/', methods=["POST", "GET"])
async def votes_webhook():
	if request.method == 'GET':
		return abort(400)
	if request.method == 'POST':
		if not request.headers.get('authorization') == "387317544228487168":
			return
		data = (await request.json)
		print("VOTE: {}".format(data["user"]))

		userinfo = db.users.find_one({"_id": int(data['user'])})
		if not userinfo:
			return await render_template('404.html')

		userinfo["vote_info"] = True
		db.users.replace_one({"_id": int(data['user'])}, userinfo, upsert=True)

		return await render_template('home-no-login.html'), 200

	else:
		return abort(400)


if __name__ == "__main__":
	app.run(host="83.82.139.228", port=int(5000), debug=False) # hots="ip" port=port
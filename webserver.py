import json

import tswift
import tweets
import twitter

import partsofspeech

from flask import Flask, request, Response
app = Flask(__name__)

@app.route("/")
def index():
	f = open("static/index.html", "r")
	fc = f.read()

	f.close()

	return fc

@app.route("/generate", methods=["POST"])
def generate():
	if not request.data:
		pass #return error

	song_title = request.form["song_title"]
	song_artist = request.form["song_artist"]
	twitter_handle = request.form["twitter_handle"]

	try:
		song = tswift.Song(title=song_title, artist=song_artist)
		lyrics = song.format()

		retdict = {"original": lyrics}

		tweets.init()

		try:
			statuses = tweets.get_statuses(twitter_handle)

			retdict["generated"] = partsofspeech.generate(statuses, lyrics)
		except twitter.TwitterError:
			return Response('{"error": "Failed to find that Twitter user!"}', mimetype="application/json")

		return Response(json.dumps(retdict), mimetype="application/json")
	except KeyError:
		return Response('{"error": "Failed to find that song!"}', mimetype="application/json")


app.run()
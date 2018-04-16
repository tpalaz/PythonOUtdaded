import json
import urllib
import os
import sys

class songDownloader(object):

	def __init__(self):
		self.DEVELOPER_KEY = "AIzaSyAwF1yzv2ZA2kvKCOs0sRkYeXs5NnKDIFA"
		self.YOUTUBE_API_SERVICE_NAME = "youtube"
		self.YOUTUBE_API_VERSION = "v3"

		with open('settings.json', 'r') as data_file:
		    self.settings = json.load(data_file)


	def verifyNoDuplicateSong(self, query):
		filesInDirectory = os.listdir(os.getcwd())
		for fileName in filesInDirectory:
		    if fileName == query + ".mp3":
			print "The desired song \"" + query + ".mp3\" already exists in the directory"
			return False
		return True


	def downloadSongByQuery(self, query):
		os.chdir(self.settings["saveDirectory"])

		if self.verifyNoDuplicateSong(query) is not True:
		    return None

		youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
			        developerKey=self.DEVELOPER_KEY)

		search_response = youtube.search().list(
		    q=query,
		    part="id,snippet",
		    maxResults=10
		).execute()

		if self.verifySearchResults(search_response) is not True:
		    return None

		for search_result in search_response.get("items", []):
		    if search_result["id"]["kind"] == "youtube#video":
			print "Attempting to download video: https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
			os.system("youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
			print "Renaming file to: " + query + ".mp3"

			temp = search_result["snippet"]["title"].replace("\"", "\'").replace("|", "_")
			if os.path.exists(temp + "-" + search_result["id"]["videoId"] + ".mp3"):
			    os.rename(temp + "-" + search_result["id"]["videoId"] + ".mp3", query + ".mp3")
			    print "File was saved in: " + self.settings["saveDirectory"]
			    return None
			else:
			    print "Unable to rename file: " + temp + "-" + search_result["id"]["videoId"] + ".mp3" + "was not found"
			    return None

	print "No song with the specified duration +/- 5 seconds was found, are you sure you entered it correctly?"

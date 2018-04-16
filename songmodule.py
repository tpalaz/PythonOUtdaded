import __main__
import conversations

class songmodule:
	    if any(word in talk for word in conversations.song_list):
		if len(talk) == 2:
			artistname = talk.replace('play', '').split()[0]
			titlename = talk.split()[-1]
			# payload = {artistname, 'title' : titlename}
			payload = (('artist', artistname),('title', titlename))
			requestsong = requests.get('http://localhost:9999/get_by_search?type=song', params=payload)
			print(requestsong.url)

		elif len(talk) <= 3:
			artistname = talk.replace('play', '').split()[:1]
			titlename = talk.split()[-1]
			# payload = {artistname, 'title' : titlename}
			payload = (('artist',  artistname),('title', titlename))
			requestsong = requests.get('http://localhost:9999/get_by_search?type=song', params=payload)
			print(requestsong.url)

		elif len(talk) >= 4:
			artistname = talk.replace('play', '').split()[:2]
			titlename = talk.split()[-3:]
			# payload = {artistname, 'title' : titlename}
			payload = (('artist',  artistname),('title', titlename))
			requestsong = requests.get('http://localhost:9999/get_by_search?type=song', params=payload)
			print(requestsong.url)


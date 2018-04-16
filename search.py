import wikipedia


class wiki:

	def search():
		wikipedia.search(talk)

	def summary():
		try:
			wikipedia.summary(talk, sentences=2)
			print wikipedia.summary(talk)
		except wikipedia.exceptions.DisambiguationError as e:
			print e.options

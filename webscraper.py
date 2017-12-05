from bs4 import BeautifulSoup
import urllib
import re
import requests
import os
import urlparse
import psycopg2

db_url = "postgres://flnagkaphunlzd:58d06cddda4a7bb84af165d0e61a1268fa8d6bdb13fc401f0d999487203a504e@ec2-174-129-227-116.compute-1.amazonaws.com:5432/dddk3nffa4e1qb"
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(db_url)

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

num_movies = 0
metacritic_scores = []
imdb_scores = []
grosses = []
movies = []
budgets = []
directors = []
writers = []
genres = []
actors = []

def get_urls():
	global num_movies
	r1 = urllib.urlopen('http://www.imdb.com/chart/top').read()
	soup1 = BeautifulSoup(r1, 'html.parser')

	movie_entries = soup1.findAll("td", "titleColumn")
	urls = []
	for movie in movie_entries:
		href = movie.find("a")["href"]
		url = "http://www.imdb.com" + href
		urls.append(url)
		num_movies += 1

	return urls

def parse_url(url):
	global metacritic_scores
	global imdb_scores
	global grosses
	global movies
	global budgets
	global directors
	global writers
	global genres
	global actors

	# INITIALIZE BEAUTIFUL SOUP

	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'html.parser')

	# EVALUATION METRICS: METACRITIC & IMDB SCORES, GROSS PROFIT

	metacritic_score = soup.find('div', 'metacriticScore')
	if metacritic_score:	# for the rare case where a movie doesnt have a metacritic score (eg. "city lights" by charles chaplin)
		metacritic_score = int(metacritic_score.span.text)
	metacritic_scores.append(metacritic_score)

	imdb_score = soup.find('span', 'rating-rating ')
	if imdb_score:
		imdb_score = float(imdb_score.find('span', 'value').text)
	imdb_scores.append(imdb_score)

	gross = soup.find("h4", text=re.compile("Gross:"))
	if gross:
		gross = u''.join(gross.next_sibling).encode('utf-8')
		gross = gross.replace(' ', '')	# remove extra spaces at beginning
		gross = gross.replace('$', '')	# remove dollar sign
		gross = gross.replace('\n', '')	# remove extra newlines
		gross = gross.replace(',', '')	# remove commas so it can be converted to an int
		try:
			gross = int(gross)
		except:
			gross = None
	grosses.append(gross)

	# MOVIE DETAILS

	title = u''.join(soup.find('title').text).encode('utf-8')
	title = title[:title.index("(")]	# get rid of the "(date) - IMDb"
	url_string = u''.join(url).encode('utf-8')
	movie_id = url_string[28:35]
	movies.append((title, movie_id))

	budget = soup.find("h4", text=re.compile("Budget:"))
	if budget:	# there are a few movies that don't have budgets listed. for instance , "M".
		budget = budget.next_sibling
		budget = ''.join(x for x in budget if x.isdecimal())	# remove extra spaces, dollar sign, newlines, commas, etc.
		budget = int(budget)
	budgets.append(budget)

	director = soup.find("h4", text=re.compile("Director:"))
	director_id = None
	if director:
		director_id = director.find_next().find("a")['href'][8:15]
		director = u''.join(director.next_sibling.next_sibling.get_text()).encode('utf-8')
	else:
		director = u''.join(soup.find("h4", text=re.compile("Directors:")).next_sibling.next_sibling.get_text()).encode('utf-8')
	director = director.replace('\n', '')
	try:
		director = director[:director.index("(")]	# get rid of extra info like "(screenplay)"
	except ValueError:
		director = director
	directors.append((director, director_id))

	writer = soup.find("h4", text=re.compile("Writer:"))
	writer_id = None
	if writer:
		writer_id = writer.find_next().find("a")['href'][8:15]
		writer = u''.join(writer.next_sibling.next_sibling.get_text()).encode('utf-8')
	else:
		writer = u''.join(soup.find("h4", text=re.compile("Writers:")).next_sibling.next_sibling.get_text()).encode('utf-8')
	writer = writer.replace('\n', '')
	writer = writer.replace(',', '')	# if multiple writers are listed the comma will be attached to the first name; delete it
	try:
		writer = writer[:writer.index("(")]	# get rid of extra info like "(screenplay)"
	except ValueError:
		writer = writer
	writers.append((writer, writer_id))

	genre = u''.join(soup.find("h4", text=re.compile("Genres:")).next_sibling.next_sibling.get_text()).encode('utf-8')[1:]
	genres.append(genre)

	cast = soup.find("table", "cast_list")
	names = cast.findAll("span", itemprop="name")
	id_urls = cast.findAll("a", itemprop="url")
	ids = []
	for id_url in id_urls:
		href = id_url['href']
		href_as_string = u''.join(href).encode('utf-8')
		ids.append(href_as_string[8:15])
		# print "appending:"
		# print href_as_string[8:15]
	top_five_actors = []
	for x in xrange(min(5, len(names))):
		actor_name = u''.join(names[x].text).encode('utf-8')
		actor_id = ids[x]
		top_five_actors.append((actor_name, actor_id))
	actors.append(top_five_actors)

def print_results():
	for x in xrange(0, num_movies):
		print "//////////////////////////////////////////////////////////////////////"
		if movies[x]:
			if movies[x][0]:
				print "MOVIE TITLE: " + movies[x][0]
			if movies[x][1]:
				print "MOVIE ID: " + movies[x][1]
		if metacritic_scores[x]:
			print "METACRITIC SCORE: " + str(metacritic_scores[x])
		if imdb_scores[x]:
			print "IMDB SCORE: " + str(imdb_scores[x])
		if grosses[x]:
			print "GROSS: " + str(grosses[x])
		if budgets[x]:
			print "BUDGET: " + str(budgets[x])
		if directors[x]:
			if directors[x][0]:
				print "DIRECTOR: " + directors[x][0]
			if directors[x][1]:
				print "DIRECTOR ID: " + directors[x][1]
		if writers[x]:
			if writers[x][0]:
				print "WRITER: " + writers[x][0]
			if writers[x][1]:
				print "WRITER ID: " + writers[x][1]
		if genres[x]:
			print "GENRE: " + genres[x]
		if actors[x]:
			print "TOP 5 ACTORS: "
			print actors[x]

def connect_to_db():
	pass
	# example
	# cur = conn.cursor()
    #
	# cur.execute("SELECT * FROM test;")
	# print (cur.fetchone())

	# need to call conn.commit() for write operations to take effect permanently

def some_null(l):
	for elem in l:
		if not elem:
			return True
	return False

def add_to_db():
	cur = conn.cursor()

	# remove movies with null fields
	clean_idx = set()
	# for i in range(10):
	for i in range(num_movies):
		movie_name, movie_ID = movies[i]
		director_ID = directors[i][1]
		metacritic_score = metacritic_scores[i]
		imdb_score = imdb_scores[i]
		gross = grosses[i]
		budget = budgets[i]
		if not some_null([movie_name, movie_ID, director_ID, metacritic_score, imdb_score, gross, budget]):
			clean_idx.add(i)


	actor_seen = set()
	for i, top_five_actors in enumerate(actors):
		if i not in clean_idx:
			continue

		for name, ID in top_five_actors:
			if ID not in actor_seen:
				cur.execute("INSERT INTO Actor VALUES (%s, %s);",
							(int(ID), name))
			actor_seen.add(ID)

	director_seen = set()
	for i, director in enumerate(directors):
		if i not in clean_idx:
			continue

		name, ID = director
		if ID not in director_seen:
			cur.execute("INSERT INTO Director VALUES (%s, %s)",
						(int(ID), name))
			director_seen.add(ID)

	for i in range(num_movies):
	# for i in range(10):
		if i not in clean_idx:
			continue
		movie_name, movie_ID = movies[i]
		# actors[i] is top five actors for this movie
		for actor_name, actor_ID in actors[i]:
			cur.execute("INSERT INTO Stars VALUES (%s, %s)",
						(int(actor_ID), int(movie_ID)))

		genre = genres[i]
		cur.execute("INSERT INTO Genre VALUES (%s, %s)",
					(genre, int(movie_ID)))

		cur.execute("INSERT INTO Movie VALUES (%s, %s, %s, %s, %s, %s, %s)",
					(int(movie_ID), movie_name, int(directors[i][1]),
					int(metacritic_scores[i]), float(imdb_scores[i]),
					int(grosses[i]), int(budgets[i])))

	# cur.execute("SELECT * FROM Movie;")

	# res = cur.fetchall()
	# print '==========' + str(len(res)) + '=========='
	# print res

	conn.commit()



	print 'test is done'

# MAIN CALL
urls = get_urls()
for url in urls:
	parse_url(url)
connect_to_db()
# print_results()

add_to_db()

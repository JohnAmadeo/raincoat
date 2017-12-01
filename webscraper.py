from bs4 import BeautifulSoup
import urllib
import re
import requests
import os
from urllib import parse
import psycopg2

def get_urls():
	r1 = urllib.urlopen('http://www.imdb.com/chart/top').read()
	soup1 = BeautifulSoup(r1, 'html.parser')
	
	movie_entries = soup1.findAll("td", "titleColumn")
	urls = []
	for movie in movie_entries:
		href = movie.find("a")["href"]
		url = "http://www.imdb.com" + href
		urls.append(url)

	return urls

def parse_url(url):

	# INITIALIZE BEAUTIFUL SOUP

	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'html.parser')

	# EVALUATION METRICS: METACRITIC & IMDB SCORES, GROSS PROFIT

	metacritic_score = soup.find('div', 'metacriticScore')
	if metacritic_score:	# for the rare case where a movie doesnt have a metacritic score (eg. "city lights" by charles chaplin)
		metacritic_score = int(metacritic_score.span.text)

	imdb_score = soup.find('span', 'rating-rating ')
	if imdb_score:
		imdb_score = float(imdb_score.find('span', 'value').text)

	gross = soup.find("h4", text=re.compile("Gross:"))
	if gross:
		gross = u''.join(gross.next_sibling).encode('utf-8')
		gross = gross.replace(' ', '')	# remove extra spaces at beginning
		gross = gross.replace('$', '')	# remove dollar sign
		gross = gross.replace('\n', '')	# remove extra newlines
		gross = gross.replace(',', '')	# remove commas so it can be converted to an int
		gross = int(gross)

	# MOVIE DETAILS

	title = u''.join(soup.find('title').text).encode('utf-8')
	title = title[:title.index("(")]	# get rid of the "(date) - IMDb"

	budget = soup.find("h4", text=re.compile("Budget:"))
	if budget:	# there are a few movies that don't have budgets listed. for instance , "M".
		budget = budget.next_sibling
		budget = ''.join(x for x in budget if x.isdecimal())	# remove extra spaces, dollar sign, newlines, commas, etc.
		budget = int(budget)

	director = soup.find("h4", text=re.compile("Director:"))
	if director:
		director = u''.join(director.next_sibling.next_sibling.get_text()).encode('utf-8')
	else:
		director = u''.join(soup.find("h4", text=re.compile("Directors:")).next_sibling.next_sibling.get_text()).encode('utf-8')
	director = director.replace('\n', '')
	try:
		director = director[:director.index("(")]	# get rid of extra info like "(screenplay)"
	except ValueError:
		director = director

	writer = soup.find("h4", text=re.compile("Writer:"))
	if writer:
		writer = u''.join(writer.next_sibling.next_sibling.get_text()).encode('utf-8')
	else:
		writer = u''.join(soup.find("h4", text=re.compile("Writers:")).next_sibling.next_sibling.get_text()).encode('utf-8')
	writer = writer.replace('\n', '')
	writer = writer.replace(',', '')	# if multiple writers are listed the comma will be attached to the first name; delete it
	try:
		writer = writer[:writer.index("(")]	# get rid of extra info like "(screenplay)"
	except ValueError:
		writer = writer

	genre = u''.join(soup.find("h4", text=re.compile("Genres:")).next_sibling.next_sibling.get_text()).encode('utf-8')[1:]

	cast = soup.find("table", "cast_list").findAll("span", itemprop="name")
	top_five_actors = []
	for x in xrange(min(5, len(cast))):
		actor = u''.join(cast[x].text).encode('utf-8')
		top_five_actors.append(actor)

	# PRINT RESULTS

	print "//////////////////////////////////////////////////////////////////////"
	if title:
		print "TITLE: " + title
	if metacritic_score:
		print "METACRITIC SCORE: " + str(metacritic_score)
	if imdb_score:
		print "IMDB SCORE: " + str(imdb_score)
	if gross:
		print "GROSS: " + str(gross)
	if budget:
		print "BUDGET: " + str(budget)
	if director:
		print "DIRECTOR: " + director
	if writer:
		print "WRITER: " + writer
	if genre:
		print "GENRE: " + genre
	if top_five_actors:
		print "TOP 5 ACTORS: "
		print top_five_actors

def connect_to_db():
	db_url = "postgres://flnagkaphunlzd:58d06cddda4a7bb84af165d0e61a1268fa8d6bdb13fc401f0d999487203a504e@ec2-174-129-227-116.compute-1.amazonaws.com:5432/dddk3nffa4e1qb"
	parse.uses_netloc.append("postgres")
	url = parse.urlparse(db_url)

	conn = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)

	# example
	cur = conn.cursor()

	cur.execute("SELECT * FROM test;")
	print (cur.fetchone())

# MAIN CALL
urls = get_urls()
for url in urls:
	parse_url(url)
connect_to_db()
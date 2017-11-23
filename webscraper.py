from bs4 import BeautifulSoup
import urllib
import re

# INITIALIZE BEAUTIFUL SOUP

r = urllib.urlopen('http://www.imdb.com/title/tt0120338/?ref_=nv_sr_1').read()
soup = BeautifulSoup(r, 'html.parser')

# EVALUATION METRICS: METACRITIC & IMDB SCORES, GROSS PROFIT

metacritic_score = int(soup.find('div', 'metacriticScore').span.text)
print metacritic_score

imdb_score = float(soup.find('span', 'rating-rating ').find('span', 'value').text)
print imdb_score

gross = str(soup.find("h4", text=re.compile("Gross:")).next_sibling)
gross = gross.replace(' ', '')	# remove extra spaces at beginning
gross = gross.replace('$', '')	# remove dollar sign
gross = gross.replace('\n', '')	# remove extra newlines
gross = gross.replace(',', '')	# remove commas so it can be converted to an int
gross = int(gross)
print gross

# MOVIE DETAILS

title = str(soup.find('title').text)
print title

budget = str(soup.find("h4", text=re.compile("Budget:")).next_sibling)
budget = budget.replace(' ', '')	# remove extra spaces at beginning
budget = budget.replace('$', '')	# remove dollar sign
budget = budget.replace('\n', '')	# remove extra newlines
budget = budget.replace(',', '')	# remove commas so it can be converted to an int
budget = int(budget)
print budget

director = str(soup.find("h4", text=re.compile("Director:")).next_sibling.next_sibling.get_text())
director = director.replace('\n', '')
print director

writer = str(soup.find("h4", text=re.compile("Writer:")).next_sibling.next_sibling.get_text())
writer = writer.replace('\n', '')
print writer

genre = str(soup.find("h4", text=re.compile("Genres:")).next_sibling.next_sibling.get_text())[1:]
print genre

cast = soup.find("table", "cast_list").findAll("span", itemprop="name")
top_five_actors = []
for x in xrange(5):
	actor = str(cast[x].text)
	top_five_actors.append(actor)
print top_five_actors
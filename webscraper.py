from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen('http://www.imdb.com/title/tt0120338/?ref_=nv_sr_1').read()
soup = BeautifulSoup(r, 'html.parser')
print type(soup)

metacritic = int(soup.find('div', 'metacriticScore').span.text)
print metacritic
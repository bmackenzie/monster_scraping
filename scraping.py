import requests
from requests import session
from contextlib import closing
from bs4 import BeautifulSoup
from lxml.html import fromstring
from itertools import cycle

request_url = 'https://www.dndbeyond.com/monsters/'



headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

def scrape(url):
    with requests.Session() as session:
        stats = []
        raw = session.get(url, headers=headers  )
        soup = BeautifulSoup(raw.content, 'html.parser')
        #Grabs monster name
        for a in soup.select('.mon-stat-block__name-link'):
            stats.append(a.text.strip())
        #Grabs size, type, and alignment
        for div in soup.select('.mon-stat-block__meta'):
            array = div.text.split(',')
            sizetype=array[0].split(' ')
            stats.append(sizetype[0])
            stats.append(sizetype[1])
            stats.append(array[1].strip())
        #Grabs ac, hp, movement
        for span in soup.select('.mon-stat-block__attribute-data-value'):
            stats.append(span.text.strip())
        #Grabs saves,and total bonus
        stats.append(soup.select('.mon-stat-block__tidbit-data')[0].text.strip())
        total = 0
        for x in soup.select('.mon-stat-block__tidbit-data')[0].text.strip():
	        if x.isdigit():
		        total += int(x)
        stats.append(total)
        #Grabs Skills
        skills= ""
        for a in soup.select('.mon-stat-block__tidbit-data')[1].contents:
            stats.append(a)
            stats.append('break')
        print(stats)

def add_monster(monster):
    url = request_url + monster
    scrape(url)

add_monster('aboleth')

columns = ['name', 'size', 'type', 'alignment', 'ac', 'hp', 'move', 'saves', 'Totalsaves']

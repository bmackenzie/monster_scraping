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
        #THIS NEEDS TO BE ADJUSTED FOR MONSTERS THAT DON'T HAVE SKILLS
        #Grabs Skills
        stats.append(soup.select('.mon-stat-block__tidbit-data')[1].get_text().strip())
        #Grabs senses
        stats.append(soup.select('.mon-stat-block__tidbit-data')[2].get_text().strip())
        #Grabs Languages
        stats.append(soup.select('.mon-stat-block__tidbit-data')[3].get_text().strip())
        #Grabs CR
        stats.append(int(soup.select('.mon-stat-block__tidbit-data')[4].get_text().strip().split(' ')[0]))

        #set default value to null for monsters that don't have these traits
        #FIX THIS
        challenge,saves,skills,senses,languages,vulnerabilities,resistences,immunities,conimmunities = ('null','null','null','null','null','null','null','null','null')
        for i in range(len(soup.select('.mon-stat-block__tidbit-label'))-1):
                label = soup.select('mon-stat-block__tidbit-label')[i].get_text().strip()
                data = soup.select('mon-stat-block__tidbit-data')[i].get_text().strip()
                if label == 'Saving Throws':
                    saves = data
                elif label == 'Skills':
                    skills = data
                elif label == 'Damage Resistances':
                    resistances = data
                elif label == 'Damage Immunities':
                    immunities = data
                elif label == 'Damage Vulnerabilities':
                    vulnerabilities = data
                elif label == 'Condition Immunities':
                    conimmunities = data
                elif label == 'Senses':
                    senses = data
                elif label == 'Languages':
                    languages = data
                elif label == 'Challenge':
                    challenge = data
        stats.extend([challenge,saves,skills,senses,languages,vulnerabilities,resistences,immunities,conimmunities])

        print(stats)


def add_monster(monster):
    url = request_url + monster
    scrape(url)

add_monster('aboleth')

#redo columns before making DF
columns = ['name', 'size', 'type', 'alignment', 'ac', 'hp', 'move', 'saves', 'Totalsaves', 'challenge', 'skills', 'senses', 'languages', 'vulnerabilities', 'resistances', 'immunities', 'condition_immunities']

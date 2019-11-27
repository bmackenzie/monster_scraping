import requests
from requests import session
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

#scraping url and headers
request_url = 'https://www.dndbeyond.com/monsters/'

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
#List of monsters to be scraped
monster_list=['aboleth', 'acolyte', 'adult-black-dragon', 'adult-blue-dragon', 'adult-brass-dragon', 'adult-bronze-dragon', 'adult-copper-dragon', 'adult-gold-dragon', 'adult-green-dragon', 'adult-red-dragon', 'adult-silver-dragon', 'adult-white-dragon', 'air-elemental', 'allosaurus', 'ancient-black-dragon', 'ancient-blue-dragon', 'ancient-brass-dragon', 'ancient-bronze-dragon', 'ancient-copper-dragon', 'ancient-gold-dragon', 'ancient-green-dragon', 'ancient-red-dragon', 'ancient-silver-dragon', 'ancient-white-dragon', 'androsphinx', 'animated-armor', 'ankheg', 'ankylosaurus', 'ape', 'archmage', 'assassin', 'awakened-shruub', 'awakened-tree', 'axe-beak', 'azer', 'baboon', 'badger', 'balor', 'bandit', 'bandit-captain']

#Dataframe setup
columns = ['name', 'size', 'type', 'alignment', 'ac', 'hp', 'move', 'str', 'dex', 'con', 'int', 'wis', 'cha', 'challenge', 'saves', 'total_save_bonus', 'skills', 'senses', 'languages', 'damage_vulnerabilities', 'damage_resistances', 'damage_immunities', 'condition_immunities']
df= pd.DataFrame(columns=columns)



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
        #Get ability scores
        for span in soup.select('.ability-block__score'):
            stats.append(float(span.text.strip()))
        #set default value to null for monsters that don't have these traits
        challenge,saves,savetotal,skills,senses,languages,vulnerabilities,resistances,immunities,conimmunities = ('null','null','null','null','null','null','null','null','null','null')
        for i in range(len(soup.select('.mon-stat-block__tidbit-label'))):
                label = soup.select('.mon-stat-block__tidbit-label')[i].get_text().strip()
                data = soup.select('.mon-stat-block__tidbit-data')[i].get_text().strip()
                if label == 'Saving Throws':
                    saves = data
                    savetotal = 0
                    for x in data:
                        if x.isdigit():
                            savetotal += float(x)
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
                    challenge = data.split(' ')[0]
        stats.extend([challenge,saves,savetotal,skills,senses,languages,vulnerabilities,resistances,immunities,conimmunities])
        df.loc[len(df)] = stats


def add_monster(monster):
    url = request_url + monster
    scrape(url)

for monster in monster_list:
    add_monster(monster)
    sleep(20)

print(df.head())
df.to_csv('monster_data', index = False)

import requests
from requests import session
from requests.auth import HTTPProxyAuth
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd
from lxml.html import fromstring
from time import sleep
import random

#scraping url and headers
request_url = 'https://www.dndbeyond.com/monsters/'

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

#List of monsters to be scraped
done=['aboleth', 'acolyte', 'adult-black-dragon', 'adult-blue-dragon', 'adult-brass-dragon', 'adult-bronze-dragon', 'adult-copper-dragon', 'adult-gold-dragon', 'adult-green-dragon', 'adult-red-dragon', 'adult-silver-dragon', 'adult-white-dragon', 'air-elemental', 'allosaurus', 'ancient-black-dragon', 'ancient-blue-dragon', 'ancient-brass-dragon', 'ancient-bronze-dragon', 'ancient-copper-dragon', 'ancient-gold-dragon', 'ancient-green-dragon', 'ancient-red-dragon', 'ancient-silver-dragon', 'ancient-white-dragon', 'androsphinx', 'animated-armor', 'ankheg', 'ankylosaurus', 'ape', 'archmage', 'assassin', 'awakened-shrub', 'awakened-tree', 'axe-beak', 'azer', 'baboon', 'badger', 'balor', 'bandit', 'bandit-captain', 'banshee', 'barbed-devil', 'basilisk', 'bat', 'bearded-devil', 'behir', 'berserker', 'black-bear', 'black-dragon-wyrmling', 'black-pudding', 'blink-dog', 'blood-hawk', 'blue-dragon-wyrmling', 'boar', 'bone-devil', 'brass-dragon-wyrmling', 'bronze-dragon-wyrmling', 'brown-bear', 'bugbear', 'bulette', 'camel', 'cat', 'centaur', 'chain-devil', 'chimera', 'chuul', 'clay-golem', 'cloaker', 'cloud-giant', 'cockatrice', 'commoner', 'constrictor-snake', 'copper-dragon-wyrmling', 'couatl', 'crab', 'crocodile', 'cult-fanatic', 'cultist', 'cyclops', 'darkmantle', 'death-dog', 'deep-gnome-svirfneblin', 'deer', 'deva', 'dire-wolf', 'diseased-giant-rat', 'djinni', 'doppelganger', 'draft-horse', 'dragon-turtle', 'dretch', 'drider', 'drow', 'druid', 'dryad', 'duergar', 'dust-mephit', 'eagle', 'earth-elemental', 'efreeti', 'elephant', 'elk', 'erinyes', 'ettercap', 'ettin', 'fire-elemental', 'fire-giant', 'flameskull', 'flesh-golem', 'flying-snake', 'flying-sword', 'frog', 'frost-giant', 'gargoyle', 'gelatinous-cube', 'ghast', 'ghost', 'ghoul', 'giant-ape', 'giant-badger', 'giant-bat', 'giant-boar', 'giant-centipede', 'giant-constrictor-snake', 'giant-crab', 'giant-crocodile', 'giant-eagle', 'giant-elk', 'giant-fire-beetle', 'giant-frog', 'giant-goat', 'giant-hyena', 'giant-lizard', 'giant-octopus', 'giant-owl', 'giant-poisonous-snake', 'giant-rat', 'giant-scorpion', 'giant-sea-horse', 'giant-shark', 'giant-spider', 'giant-toad', 'giant-vulture', 'giant-wasp', 'giant-weasel', 'giant-wolf-spider', 'gibbering-mouther', 'glabrezu', 'gladiator', 'gnoll', 'goat', 'goblin', 'gold-dragon-wyrmling', 'gorgon', 'gray-ooze', 'green-dragon-wyrmling', 'green-hag', 'grick', 'griffon', 'grimlock', 'guard', 'guardian-naga', 'gynosphinx', 'half-red-dragon-veteran', 'harpy', 'hawk', 'hell-hound', 'hezrou', 'hill-giant', 'hippogriff', 'hobgoblin', 'homunculus', 'homunculus-servant', 'horned-devil', 'hunter-shark', 'hydra', 'hyena', 'ice-devil', 'ice-mephit', 'imp', 'improved-steel-defender', 'incubus', 'invisible-stalker', 'iron-golem', 'jackal', 'killer-whale', 'knight', 'kobold', 'kraken', 'lamia', 'lemure', 'lich', 'lion', 'lizard', 'lizardfolk', 'mage', 'magma-mephit', 'magmin', 'mammoth', 'manticore', 'marilith', 'mastiff', 'medusa', 'merfolk', 'merrow', 'mimic', 'minotaur', 'minotaur-skeleton', 'mule', 'mummy', 'mummy-lord', 'nalfeshnee', 'night-hag', 'nightmare', 'noble', 'nothic', 'ochre-jelly', 'octopus', 'ogre', 'ogre-zombie', 'oni', 'orc', 'otyugh', 'owl', 'owlbear', 'panther', 'pegasus', 'phase-spider', 'pit-fiend', 'planetar', 'plesiosaurus', 'poisonous-snake', 'polar-bear', 'pony', 'priest', 'pseudodragon', 'pteranodon', 'purple-worm', 'quasit', 'quipper', 'rakshasa', 'rat', 'raven', 'red-dragon-wyrmling', 'reef-shark', 'remorhaz', 'rhinoceros', 'riding-horse', 'roc', 'roper', 'rug-of-smothering', 'rust-monster', 'saber-toothed-tiger', 'sahuagin', 'salamander', 'satyr', 'scorpion', 'scout', 'sea-hag', 'sea-horse', 'shadow', 'shambling-mound', 'shield-guardian', 'shrieker', 'silver-dragon-wyrmling', 'skeleton', 'solar', 'spectator', 'specter', 'spider', 'spirit-naga', 'sprite', 'spy', 'steam-mephit', 'steel-defender', 'stirge', 'stone-giant', 'stone-golem', 'storm-giant', 'succubus', 'swarm-of-bats', 'swarm-of-insects', 'swarm-of-insects-beetles', 'swarm-of-insects-centipedes', 'swarm-of-insects-spiders', 'swarm-of-insects-wasps', 'swarm-of-poisonous-snakes', 'swarm-of-quippers', 'swarm-of-rats', 'swarm-of-ravens', 'tarrasque', 'thug', 'tiger', 'treant', 'tribal-warrior', 'triceratops', 'troll', 'twig-blight', 'tyrannosaurus-rex', 'unicorn', 'vampire', 'vampire-spawn', 'veteran', 'violet-fungus', 'vrock', 'vulture', 'warhorse', 'warhorse-skeleton', 'water-elemental', 'weasel', 'werebear', 'wereboar', 'wererat', 'weretiger', 'werewolf', 'white-dragon-wyrmling', 'wight', 'will-o-wisp', 'winter-wolf', 'wolf', 'worg', 'wraith', 'wyvern', 'xorn']

monster_list = ['yeti', 'young-black-dragon', 'young-blue-dragon', 'young-brass-dragon', 'young-bronze-dragon', 'young-copper-dragon', 'young-gold-dragon', 'young-green-dragon', 'young-red-dragon', 'young-silver-dragon', 'young-white-dragon', 'zombie']

remaining = []

#Dataframe setup
columns = ['name', 'size', 'type', 'alignment', 'ac', 'hp', 'move', 'str', 'dex', 'con', 'int', 'wis', 'cha', 'challenge', 'saves', 'total_save_bonus', 'skills', 'senses', 'languages', 'damage_vulnerabilities', 'damage_resistances', 'damage_immunities', 'condition_immunities']
df= pd.DataFrame(columns=columns)


def scrape(url):
    with requests.Session() as session:
        stats = []
        raw = session.get(url, headers=headers)
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
                    if "/" in data:
                        split = data.split(' ')[0]
                        numbers = split.split('/')
                        challenge = int(numbers[0])/int(numbers[1])
                    else:
                        challenge = data.split(' ')[0]
        stats.extend([challenge,saves,savetotal,skills,senses,languages,vulnerabilities,resistances,immunities,conimmunities])
        print(url)
        print(stats)
        df.loc[len(df)] = stats


def detour():
    randlist=['aboleth', 'acolyte', 'adult-black-dragon', 'adult-blue-dragon', 'adult-brass-dragon', 'adult-bronze-dragon', 'adult-copper-dragon', 'adult-gold-dragon', 'adult-green-dragon', 'adult-red-dragon', 'adult-silver-dragon', 'adult-white-dragon', 'air-elemental', 'allosaurus', 'ancient-black-dragon', 'ancient-blue-dragon', 'ancient-brass-dragon', 'ancient-bronze-dragon', 'ancient-copper-dragon', 'ancient-gold-dragon', 'ancient-green-dragon', 'ancient-red-dragon', 'ancient-silver-dragon', 'ancient-white-dragon', 'androsphinx']
    randstring = randlist[random.randint(0, len(randlist)-1)]
    url = request_url + randstring
    with requests.Session() as session:
        raw = session.get(url, headers=headers)
        sleep(random.randint(20,50))

def add_monster(monster):
    detour_check = random.randint(1,15)
    if detour_check == 1:
        detour()
    url = request_url + monster
    scrape(url)

for monster in monster_list:
    add_monster(monster)
    sleep(random.randint(20,50))

fulldf = pd.read_csv('monster_data.csv')
newdf = fulldf.append(df)
newdf.to_csv('monster_data.csv', index = False)

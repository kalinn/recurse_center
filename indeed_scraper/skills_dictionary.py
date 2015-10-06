# skills_dictionary.py
import re
import pandas as pd
import numpy as np

from urllib2 import urlopen
from bs4 import BeautifulSoup

# This function scrapes wikipedia for all programming languages
def getLanguages():
    wikiUrl = urlopen('https://en.wikipedia.org/wiki/List_of_programming_languages')
    wikiHtml = wikiUrl.read()
    parsed = BeautifulSoup(wikiHtml, 'html.parser')
    multicol = parsed.find_all("table", {"class": "multicol"})
    getA = []
    for letter in multicol:
        getA = getA + letter.find_all("a")
    languages = [t.get_text() for t in getA]
    for lang in languages:
        strip = re.search('\ \([A-Za-z]', lang)
        if strip is not None:
            stripStart = strip.start()
            languages[languages.index(lang)] = lang[0:stripStart]
        else:
            pass
    unique = list(set(languages))
    lowercase = sorted([l.lower() for l in unique])
    return lowercase

# This function scrapes wikipedia for all databases
def getDatabases():
    wikiUrl = urlopen('https://en.wikipedia.org/wiki/List_of_relational_database_management_systems')
    wikiHtml = wikiUrl.read()
    parsed = BeautifulSoup(wikiHtml, 'html.parser')
    cols = parsed.find_all("div", {"class": "div-col columns column-width"})
    getA = []
    for li in cols:
        getA = getA + li.find_all("a")
    databases = [d.get_text() for d in getA]
    for db in databases:
        strip = re.search('\ \([A-Za-z]', db)
        if strip is not None:
            stripStart = strip.start()
            databases[databases.index(db)] = db[0:stripStart]
        else:
            pass
    unique = list(set(databases))
    lowercase = sorted([l.lower() for l in unique])
    return lowercase

def getSkills():
    db_dict = getDatabases()
    language_dict = getLanguages()
    other_dict = ['mapreduce', 'map reduce', 'hive', 'pig',
    'mongodb', 'ec2', 'spark', 'apache pig', 'apache hadoop',
    'parallel', 'parallel computing', 'big data', 'massive data',
    'openmp', 'json', 'gridmp', 'grid mp', 'open mp', 'powerpoint',
    'power point', 'excel']
    db_strings = []
    for db in db_dict:
        try:
            db_strings.append(str(db))
        except:
            pass
    lang_strings = []
    for lang in language_dict:
        try:
            lang_strings.append(str(lang))
        except:
            pass
    complete_dict = db_strings + lang_strings + other_dict
    return complete_dict

############################################################
# CREATED DICTIONARY ON 8-25-15
############################################################
dict08_25_2015 = getSkills()
id = np.arange(len(dict08_25_2015))
dfSkills = pd.Series(dict08_25_2015)
dfSkills.to_csv('~/GitHub/recurse_center/indeed_scraper/skills.csv')





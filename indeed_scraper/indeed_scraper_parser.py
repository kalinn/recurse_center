import numpy as np
import re
import pandas as pd
import json
import os

from indeed import IndeedClient
from urllib2 import urlopen
from bs4 import BeautifulSoup
from indeed_private import client

#################################################################
# @function totalJobs() Returns total number of jobs with
#                       Data Science in the title
#                       Number of pages (incl 0) is totalJobs()/10
#################################################################
def totalJobs():
    url = urlopen('http://www.indeed.com/jobs?q=title%3A(Data+Scientist)&start='+str(0))
    html = url.read()
    parsed = BeautifulSoup(html, 'html.parser')
    parsed.find()
    text = parsed.find(id='searchCount').get_text()
    tot = re.split('of\s', text)[1]
    comma = re.split('\,', tot)
    if len(comma)==1:
        numJobs = int(comma)
    else:
        numJobs = int(''.join(comma))
    return numJobs

#################################################################
# @function getJobdata(n) extracts the dictionary-type
#                         data from each job posting
# @param n number of search pages (1, 2, ...) to get jobkeys from
#          (~10 jobs/page)
# @note Searching the Indeed API by keyword (e.g., title="Data
#       Scientist") limits results to 25 postings. The work-around
#       is to scrape job keys from all the job post URLs on the
#       search page and search by job key in the API.
#################################################################
def getJobData(client, n=5):
    jobkeys = []
    for j in range(0, 10*n, 10):
        print j
        # Search for "Data Scientist" in job title
        # str(j=0) gives jobs 1-10, str(j=10) gives jobs 11-20, etc.
        urlParent = urlopen('http://www.indeed.com/jobs?q=title%3A(Data+Scientist)&start='+str(j))
        # Parse the HTML of main search page
        htmlParent = urlParent.read()
        parsed = BeautifulSoup(htmlParent, 'html.parser')
        # Links are referenced by the 'a' html tag
        linksChildren = [link.get('href') for link in parsed.find_all('a')]
        # Find only the links with a job key, denoted jk=
        hasJk = [re.search("jk=", link).string for link in linksChildren if re.search("jk=", link) is not None]
        # Extract job keys (the 16char id that follows jk= in url)
        jks = [re.search('(?<==)\w+', jk).group(0) for jk in hasJk]
        jobkeys = jobkeys + jks
    t = tuple(jobkeys)
    tarray = np.array(t)
    # Job keys have 16 characters
    len16 = [len(j)==16 for j in t]
    t = tuple(tarray[np.ix_(len16)])
    # Call the job API
    jobData = []
    for j in range(len(t)):
        try:
            jb = client.jobs(jobkeys = t[j:(j+1)]).get('results')[0]
            jobData.append(jb)
        except:
            print "Bad job request"
            continue
    # jobData = [client.jobs(jobkeys = t[j:(j+1)]).get('results')[0] for j in range(len(t))]
    return jobData


class job:
    'Common base class for all job postings'
    jobCount = 0

    def __init__(self, dataDict):
        self.data = dataDict
        self.city = dataDict['city']
        self.company = dataDict['company']
        self.country = dataDict['country']
        self.date = dataDict['date']
        self.expired = dataDict['expired']
        self.formattedLocation = dataDict['formattedLocation']
        self.formattedLocationFull = dataDict['formattedLocationFull']
        self.formattedRelativeTime = dataDict['formattedRelativeTime']
        self.indeedApply = dataDict['indeedApply']
        self.jobkey = dataDict['jobkey']
        self.jobtitle = dataDict['jobtitle']
        self.sponsored = dataDict['sponsored']
        self.state = dataDict['state']
        self.url = dataDict['url']
        self.jobCount = job.jobCount
        job.jobCount += 1
        self.skills = dict()

#################################################################
# @function getPostingText parses the HTML of the original
#                          job postings (on the company sites)
#                          and then gets the text, returned as
#                          all lowercase
# @param data list of job data dictionaries returned by
#             function getJobData
#################################################################
    def getPostText(self):
        url = self.url
        try:
            page = urlopen(url).read()
            parsed = BeautifulSoup(page, 'html.parser')
            strParsed = parsed.get_text()
            parsedLower = strParsed.lower()
            self.postText = parsedLower
        except:
            print "Job posting %d encountered an error." %self.jobCount
            self.postText = None

#################################################################
# @function checkSkill parses the HTML of an original
#                      job posting (on the company site)
#                      and returns True if 'skill' is found
# @param skill string with a single language or other skill
# @param post String of lowercase text from a single posting
#             returned from function getPostingText()
#################################################################
    def checkSkill(self, skill):
        try:
            skillType = type(skill) is not str
            if skillType:
                raise TypeError
        except TypeError:
            print 'The skill must be a string'
        else:
            if '+' in skill:
                if '++' in skill:
                    front = str('(\s|\(|\/)(')
                    end = str(')(\%|\/|\.|,|\s|\))')
                    midSplit = re.split('(\++)', skill)
                    middle = midSplit[0] + '(\++)' + midSplit[2]
                    total = front + middle + end
                else:
                    front = str('(\s|\(|\/)(')
                    end = str(')(\%|\/|\.|,|\s|\))')
                    midSplit = re.split('(\+)', skill)
                    middle = midSplit[0] + '(\+)' + midSplit[2]
                    total = front + middle + end
            else:
                front = str('(\s|\(|\/)(')
                end = str(')(\%|\/|\.|,|\s|\))')
                middle = skill
                total = front + middle + end
            inPost = re.search(total, self.postText)
            skillVec = []
            snippetVec = []
            self.snippet = None
            self.skills[skill] = False
            if inPost is not None:
                allRegs = [m.regs for m in re.finditer(total, self.postText)]
                for k in range(len(allRegs)):
                    skillVec.append(True)
                    start = allRegs[k][0][0]
                    stop = allRegs[k][0][1]
                    snippetVec.append(None)
                    if start - 25 > 0:
                        if stop + 25 < len(self.postText):
                            print skill
                            snippet = self.postText[(start-25):(stop+25)]
                            snippetVec[k] = snippet
                            # Get rid of r in function calls
                            if skill=='r':
                                checkFn = re.search("function", snippet)
                                if checkFn is not None:
                                    skillVec[k] = False
                            # Get rid of r in .js function calls
                            if skill=='r':
                                checkFn = re.search("\.js", snippet)
                                if checkFn is not None:
                                    skillVec[k] = False
                            # get rid of google analytics junk
                            if skill=="analytics":
                                checkFn = re.search("\.com", snippet)
                                if checkFn is not None:
                                    skillVec[k] = False
                            # get rid of ajax junk
                            if skill=="ajax":
                                checkFn = re.search("src=", snippet)
                                if checkFn is not None:
                                    skillVec[k] = False
                            # get rid of javascript junk
                            if skill=="javascript":
                                checkFn = re.search("enable", snippet)
                                if checkFn is not None:
                                    skillVec[k] = False
                            # get rid of css junk
                            if skill=="css":
                                checkFn = re.search("href=", snippet)
                                if checkFn is not None:
                                    skillVec[k] = False
                            # get rid of json junk
                            if skill=="json":
                                checkFn1 = re.search("try", snippet)
                                checkFn2 = re.search("return", snippet)
                                checkFn3 = re.search("void", snippet)
                                checkFn4 = re.search("catch", snippet)
                                checkFn = (checkFn1 is None)+(checkFn2 is None)+(checkFn3 is None)+(checkFn4 is None)
                                if checkFn is not 0:
                                    skillVec[k] = False
                            # get rid of (c) copyright
                            if skill=="c":
                                checkFn = re.search("copyright", snippet)
                                if checkFn is not None:
                                    skillVec[k] = False
                            # get rid of c in function calls by only
                            # counting if java is also listed
                            if skill=="c":
                                checkFn = re.search("java", snippet)
                                if checkFn is None:
                                    skillVec[k] = False
                            if skillVec[k]==True:
                                self.snippet = snippetVec[k]
                                print snippetVec[k]
                                print '\n'
                        else:
                            pass
                    else:
                        pass
                if skillVec.count(1)>=1:
                    self.skills[skill] = True
                else:
                    self.skills[skill] = False
            else:
                pass

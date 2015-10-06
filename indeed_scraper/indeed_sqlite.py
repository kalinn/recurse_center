# sql_setup.py
import sqlite3 as lite
import sys
from indeed_scraper_parser import totalJobs, getJobData, job,

# Skills dictionary
skillsList = pd.read_csv("~/GitHub/recurse_center/indeed_scraper/skills.csv",
    index_col=None, names=["skill"], header=None)

totalPages = totalJobs()/10
# Collected 9-15-15
testData = getJobData(client=client, n=totalPages)

# Populate the SQL database:
con = lite.connect('indeed.db')
cur = con.cursor()
cur.execute("CREATE TABLE posts(id INT PRIMARY KEY, jobkey TEXT UNIQUE, company TEXT, postDate TEXT, url TEXT, state TEXT, city TEXT, jobtitle TEXT)")
cur.execute("CREATE TABLE skills(id INTEGER PRIMARY KEY, skill TEXT UNIQUE)")
cur.execute("CREATE TABLE post_skills(postId INT, skillId INT, snippet TEXT)")

for j in range(len(testData)):
    id = j+1
    try:
        jobkey = testData[j]['jobkey']
        company = testData[j]['company']
        date = testData[j]['date']
        url = testData[j]['url']
        state = testData[j]['state']
        city = testData[j]['city']
        jobtitle = testData[j]['jobtitle']
        # Update the posts table with the job post
        insertPost = "INSERT INTO posts VALUES(" + str(id) + ",\"" + jobkey + "\",\"" + company + "\",\"" + date + "\",\"" + url + "\",\"" + state + "\",\"" + city + "\",\"" + jobtitle + "\")"
        cur.execute(insertPost)
        con.commit()
        singleJob = job(testData[j])
        singleJob.getPostText()
        if singleJob.postText==None:
            pass
        else:
            for skill in skillsList.skill:
                singleJob.checkSkill(skill)
                if singleJob.skills[skill]==True:
                    insertSkill = "INSERT INTO skills(skill) VALUES(\"" + skill + "\")"
                    try:
                        cur.execute(insertSkill)
                        con.commit()
                    except:
                        print "Unexpected error: ", sys.exc_info()[0], "on skill: ", skill
                    finally:
                        querySkill = "SELECT id FROM skills WHERE skill=" + "\'" + skill + "\'"
                        execQuery = cur.execute(querySkill)
                        fetchId = execQuery.fetchall()[0][0]
                        insertRelation = "INSERT INTO post_skills VALUES(" + str(id) + "," + str(fetchId) + "," + "\'" + singleJob.snippet + "\'" + ")"
                        try:
                            cur.execute(insertRelation)
                            con.commit()
                        except:
                            print "Unexpected error: ", sys.exc_info()[0]
    except:
        print "Unexpected error: ", sys.exc_info()[0], "on testData[",j,"]"


# In sqlite3:
# select (select skill from skills where id=skillId), count(*) from post_skills group by skillId order by count(*);

###############################################
###############################################
# Next Steps:
# - Prune the dictionary some more?
# - DONE-ish: Regex stuff to find the languages that
#             map to each job post (but should do more testing
#             for weird cases, this is still buggy)
# - Figure out AJAX POST requests?
# - WORKING: Put data into database
# - Figure out how to update database automatically
# - Data viz of the results (d3? map by location?)
# - Build into a web app (Flask?) that would do a search, possibly
#   in a given area or for a particular skill set, and create
#   the viz in real time
###############################################
###############################################




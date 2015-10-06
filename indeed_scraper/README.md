# Indeed

This is currently my main project at RC. The goal is to collect and analyze data from "Data Scientist" job postings on Indeed.com. In particular, I'm interested in answering the question: "What skills are most desirable to employers looking to hire data scientists?"

I plan to answer this question by parsing the HTML from individual companies that have job postings for data scientists. The links on the Indeed.com search pages usually redirect to these individual job postings. 

The file indeed_scraper.py contains functions that parse the HTML from the job postings and check for the skills from the list in skills.csv. The file sqlite_setup.py populates my database, which consists of three tables: one that contains job posting data, one that is just a list of skills with an integer primary key, and a third table that keeps track of the many-to-many relationship between the job postings and skills. This is not a large project, and thus, I could have easily stored all the data in a pandas data frame. The structure of this project reflects my intent to learn new things and is not necessarily the best or most efficient data pipeline.  
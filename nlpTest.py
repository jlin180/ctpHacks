import bs4 as bs
import urllib.request
import re
import datetime
from urllib.error import HTTPError
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


lemmatizer = WordNetLemmatizer()

"""
this is the helper function for lemmatize_sentence
returns the correct part of speech tag
the argument takes in a tokenized sentence in a list format
"""
def nltk2wn_tag(nltk_tag):
  if nltk_tag.startswith('J'):
    return wordnet.ADJ
  elif nltk_tag.startswith('V'):
    return wordnet.VERB
  elif nltk_tag.startswith('N'):
    return wordnet.NOUN
  elif nltk_tag.startswith('R'):
    return wordnet.ADV
  else:
    return None

"""
a helper function for pullLink() and pullMonster()
argument takes in a string
string HAS TO BE cleaned beforehand with cleanData() before being passed in
returns lemmatized verison of the input string
"""
def lemmatize_sentence(sentence):
  nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
  wn_tagged = map(lambda x: (x[0], nltk2wn_tag(x[1])), nltk_tagged)
  res_words = []
  for word, tag in wn_tagged:
    if tag is None:
      res_words.append(word)
    else:
      res_words.append(lemmatizer.lemmatize(word, tag))
  return " ".join(res_words)

"""
this is a helper function for pullLink() and pullMonster()
argument takes in string which is going to be searched for unwanted words
the string that is the input SHOULD BE lemmatized before being sent in
returns true or false depending on if none of the searched words are found within it
"""
def find_keywords(job):

    badWords = ["senior","sr","p hd","phd","masters","master","ph d"]
    badYears =["yearsofexperience","years of experience","years of","years","year","year of"]

    if "bachlors" in job or "bachlor" in job:
        for word in badYears:
            if word in job:
                return False
    else:
        combined = badWords + badYears
        for word in combined:
            if word in job:
                return False

    return True
"""
this function goes to LinkedIn and pulls job posting data from it
it pulls information such as company, job title, dated posted, location, and description of the job
it then will fliter the job postings using find_keywords function, if it passes the filter it will be put into a dict
and appended to a return list
this function returns a list of dicts of the job postings pulled 
"""
def pullLink():
    #getting linkedin main job search page
    sauce = urllib.request.urlopen("https://www.linkedin.com/jobs/search?keywords=Software%2BEngineer&location=New%2BYork%2C%2BUnited%2BStates&geoId=105080838&trk=public_jobs_jobs-search-bar_search-submit&f_TP=1%2C2&f_E=2&redirect=false&position=1&pageNum=0").read()
    soup = bs.BeautifulSoup(sauce,"lxml")
    links = soup.find_all("a",{"class": "result-card__full-card-link"})

    jobs = []
    #going through all the links
    for i in links:
        #obtaining information
        try:
            subSauce = urllib.request.urlopen(i['href']).read()
        except UnicodeEncodeError:
            continue
        except HTTPError as err:
            continue
        subSoup = bs.BeautifulSoup(subSauce,"lxml")

        #grabbing company name
        try:
            company = subSoup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text
        except AttributeError:
            continue
        try:
            company = company.encode("ascii", "ignore").decode('utf-8')
        except UnicodeEncodeError:
            continue

        #grabbing job title
        jobTitle = subSoup.find("h2",{"class": "topcard__title"}).text
        jobTitle = jobTitle.encode("ascii", "ignore").decode('utf-8')

        #grabbing date posted
        datePosted = subSoup.find("span",{"class": "topcard__flavor--metadata posted-time-ago__text"})
        if(datePosted is not None):
            splitTime = datePosted.text.split(" ")
            today = datetime.datetime.now()
            d = datetime.timedelta(int(splitTime[0]))
            datePosted = (today - d).date()
        else:
            today = datetime.datetime.now()
            d = datetime.timedelta(1)
            datePosted = (today - d).date()

        datePosted = datePosted.strftime("%m/%d/%Y")

        #grabbing location
        location = subSoup.find("span",{"class": "topcard__flavor topcard__flavor--bullet"}).text
        location = location.encode("ascii","ignore").decode('utf-8')

        #grabbing desc
        desc = subSoup.find("div",{"class": "show-more-less-html__markup"})
        descText = desc.text
        list = []
        for j in desc.find_all("u"):
            descText = descText.replace(j.text,"")
        for j in desc.find_all("ul"):
            descText = descText.replace(j.text,"")

        #filtering the job posting
        descText = descText.encode("ascii","ignore").decode('utf-8')
        lemDesc = descText
        lemDesc = cleanData(lemDesc)
        lemDesc = lemmatize_sentence(lemDesc)

        #storing or not storing for output
        if find_keywords(lemDesc) is False:
            continue
        else:
            jobDict = {
                "company": company,
                "title": jobTitle,
                "reqs": descText,
                "datePosted": datePosted,
                "location": location,
                "link": i['href'].encode("ascii", "ignore").decode('utf-8')
            }

            jobs.append(jobDict)

    return jobs

"""
this function goes to Monster and pulls job posting data from it
it pulls information such as company, job title, dated posted, location, and description of the job
it then will fliter the job postings using find_keywords function, if it passes the filter it will be put into a dict
and appended to a return list
this function returns a list of dicts of the job postings pulled 
"""
def pullMonster():
    sauce = urllib.request.urlopen("https://www.monster.com/jobs/search/?q=Software-Engineer&tm=14").read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    links = soup.find_all("h2", {"class": "title"})

    jobs = []

    for i in links:
        #obtaining link
        link = i.find("a",href=True)
        try:
            subSauce = urllib.request.urlopen(link['href']).read()
        except UnicodeEncodeError:
            continue
        except HTTPError as err:
            continue

        subSoup = bs.BeautifulSoup(subSauce, "lxml")

        #grabbing company name
        try:
            company = subSoup.find("div", {"class": "job_company_name tag-line c-primary"}).text
            if (company is ""):
                continue
            else:
                try:
                    company = company.encode("ascii", "ignore").decode('utf-8')
                except UnicodeEncodeError:
                    continue
        except AttributeError:
            continue

        # grabbing job title
        jobTitle = subSoup.find("h1", {"class": "job_title c-primary-dk"}).text
        jobTitle = jobTitle.encode("ascii", "ignore").decode('utf-8')

        # grabbing date posted
        datePosted = subSoup.find("div", {"name": "value_posted"})
        if (datePosted.text == "Today"):
            datePosted = datetime.datetime.now().date()
        elif(datePosted.text == "30+ days ago"):
            today = datetime.datetime.now()
            d = datetime.timedelta(30)
            datePosted = (today - d).date()
        else:
            splitTime = datePosted.text.split(" ")
            today = datetime.datetime.now()
            d = datetime.timedelta(int(splitTime[1]))
            datePosted = (today - d).date()

        datePosted = datePosted.strftime("%m/%d/%Y")

        # grabbing location
        location = subSoup.find("div", {"name": "job_company_location"}).text
        location = re.sub("\d", "", location)
        location = location.encode("ascii", "ignore").decode('utf-8')

        # grabbing desc
        desc = subSoup.find("div", {"name": "job_description"})
        descText = desc.text
        for j in desc.find_all("u"):
            descText = descText.replace(j.text, "")
        for j in desc.find_all("ul"):
            descText = descText.replace(j.text, "")
            descText = descText + j.text

        #filtering the job posting
        descText = descText.encode("ascii", "ignore").decode('utf-8')
        lemDesc = descText
        lemDesc = cleanData(lemDesc)
        lemDesc = lemmatize_sentence(lemDesc)

        # storing or not storing for output
        if find_keywords(lemDesc) is False:
            continue
        else:
            jobDict = {
                "company": company,
                "title": jobTitle,
                "reqs": descText,
                "datePosted": datePosted,
                "location": location,
                "link": link['href'].encode("ascii", "ignore").decode('utf-8')
            }

            jobs.append(jobDict)

    return jobs

"""
this function is a helper function for pullLink() and pullMonster()
it takes in a string of the job description to be cleaned
uses several string manipulation functions to get data ready
returns a string of the cleaned verison of the data
"""
def cleanData(job):
    job = job.lower()
    job = job.replace("c++", "cplusplus").encode("ascii", "ignore").decode('utf-8')
    job = job .replace("Description", "").encode("ascii", "ignore").decode('utf-8')
    job = job .replace("description", "").encode("ascii", "ignore").decode('utf-8')
    job = re.sub('[\W_]+', " ", job ).encode("ascii", "ignore").decode('utf-8')
    job = job.replace("\n", "").encode("ascii", "ignore").decode('utf-8')
    job = job.replace("\t", "").encode("ascii", "ignore").decode('utf-8')

    return job

def main():
    jobs = pullLink()
    jobs2 = pullMonster()
    joinedJobs = jobs+jobs2
    for i in joinedJobs:
        print(i)


if __name__ == "__main__":
    main()

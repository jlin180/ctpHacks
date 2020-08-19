import bs4 as bs
import urllib.request
import re
import datetime

def pullLink():
    #getting linkedin main job search page
    sauce = urllib.request.urlopen("https://www.linkedin.com/jobs/search?keywords=Computer%2BScience&trk=public_jobs_jobs-search-bar_search-submit&f_TP=1%2C2&redirect=false&position=1&pageNum=0").read()
    soup = bs.BeautifulSoup(sauce,"lxml")
    links = soup.find_all("a",{"class": "result-card__full-card-link"})

    jobs = []
    #going through all the links
    for i in links:
        #obtaining information
        subSauce = urllib.request.urlopen(i["href"]).read()
        subSoup = bs.BeautifulSoup(subSauce,"lxml")

        #grabbing company name
        company = subSoup.find("a",{"class": "topcard__org-name-link topcard__flavor--black-link"}).text
        company = company.encode("ascii","ignore")

        #grabbing job title
        jobTitle = subSoup.find("h2",{"class": "topcard__title"}).text
        jobTitle = jobTitle.encode("ascii", "ignore")

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

        #grabbing location
        location = subSoup.find("span",{"class": "topcard__flavor topcard__flavor--bullet"}).text
        location = location.encode("ascii","ignore")

        #grabbing desc
        desc = subSoup.find("div",{"class": "show-more-less-html__markup"})
        descText = desc.text
        list = []
        for j in desc.find_all("u"):
            descText = descText.replace(j.text,"")
        for j in desc.find_all("ul"):
            descText = descText.replace(j.text,"")

        descText = descText.encode("ascii","ignore")

        jobDict = {
            "company": company,
            "title": jobTitle,
            "reqs": descText,
            "datePosted": datePosted,
            "location": location
        }

        jobs.append(jobDict)

    return jobs

def pullMonster():
    sauce = urllib.request.urlopen("https://www.monster.com/jobs/search/?q=Computer-Science&tm=14&jobid=219011797").read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    links = soup.find_all("h2", {"class": "title"})

    for i in links:
        #obtaining information
        link = i.find("a",href=True)
        print(link['href'])

def cleanData(jobs):
    for i in jobs:
        i["reqs"] = i["reqs"].lower()
        i["reqs"] = i["reqs"].replace("C++","cplusplus")
        i["reqs"] = re.sub('[\W_]+'," ",i["reqs"])

    return jobs

def main():
    pullLink()
    jobs = pullLink()
    #jobs = cleanData(jobs)
    for i in jobs:
        print(i["company"])
        print(i["title"])
        print(i["reqs"])
        print(i["datePosted"])
        print(i["location"])

if __name__ == "__main__":
    main()

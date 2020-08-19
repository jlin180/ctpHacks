import bs4 as bs
import urllib.request
import re
import datetime
import FirebaseAPI

def pullLink():
    #getting linkedin main job search page
    sauce = urllib.request.urlopen("https://www.linkedin.com/jobs/search/?f_E=2&keywords=computer%20science&f_TP=1%2C2&redirect=false&position=1&pageNum=0").read()
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
        company = company.encode("ascii","ignore").decode('utf-8')

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

        descText = descText.encode("ascii","ignore").decode('utf-8')

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
    sauce = urllib.request.urlopen("https://www.monster.com/jobs/search/?q=Computer-Science&intcid=skr_navigation_nhpso_searchMainPrefill&tm=14").read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    links = soup.find_all("h2", {"class": "title"})

    jobs = []

    for i in links:
        #obtaining link
        link = i.find("a",href=True)
        subSauce = urllib.request.urlopen(link['href']).read()
        subSoup = bs.BeautifulSoup(subSauce, "lxml")

        #grabbing company name
        company = subSoup.find("div", {"class": "job_company_name tag-line c-primary"}).text
        if(company is ""):
            continue
        else:
            company = company.encode("ascii", "ignore").decode('utf-8')

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

        descText = descText.encode("ascii", "ignore").decode('utf-8')

        jobDict = {
            "company": company,
            "title": jobTitle,
            "reqs": descText,
            "datePosted": datePosted,
            "location": location
        }

        jobs.append(jobDict)

    return jobs



def cleanData(jobs):
    for i in jobs:
        i["reqs"] = i["reqs"].lower()
        i["reqs"] = i["reqs"].replace("C++", "cplusplus").encode("ascii", "ignore").decode('utf-8')
        i["reqs"] = re.sub('[\W_]+', " ", i["reqs"]).encode("ascii", "ignore").decode('utf-8')

    return jobs

def main():
    jobs = pullLink()
    FirebaseAPI.insert(jobs)
    jobs2 = pullMonster()
    jobs = jobs +jobs2
    jobs = cleanData(jobs)

if __name__ == "__main__":
    main()

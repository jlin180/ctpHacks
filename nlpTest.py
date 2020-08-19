import bs4 as bs
import urllib.request

def pullData():
    #getting linkedin main job search page
    sauce = urllib.request.urlopen("https://www.linkedin.com/jobs/search/?keywords=computer%20science").read()
    soup = bs.BeautifulSoup(sauce,"lxml")
    links = soup.find_all("a",{"class": "result-card__full-card-link"})

    jobs = []
    #going through all the links
    for i in links:
        subSauce = urllib.request.urlopen(i["href"]).read()
        subSoup = bs.BeautifulSoup(subSauce,"lxml")

        company = subSoup.find("a",{"class": "topcard__org-name-link topcard__flavor--black-link"}).text.encode("utf-8")
        jobTitle = subSoup.find("h2",{"class": "topcard__title"}).text.encode("utf-8")
        desc = subSoup.find("div",{"class": "show-more-less-html__markup"})
        descText = desc.text
        list = []
        for j in desc.find_all("u"):
            descText = descText.replace(j.text,"")
        for j in desc.find_all("ul"):
            descText = descText.replace(j.text,"")

        jobDict = {
            "company": company,
            "title": jobTitle,
            "reqs": descText
        }

        jobs.append(jobDict)

    return jobs

#def cleanData(jobs):
    #for i in jobs:
        #i["reqs"] = i["reqs"].replace("."," ")
        #i["reqs"] = i["reqs"].replace(","," ")

    #return jobs

def main():
    jobs = pullData()
    #jobs = cleanData(jobs)
    for i in jobs:
        print(i["reqs"].encode("utf-8"))


if __name__ == "__main__":
    main()

import bs4 as bs
import urllib.request
import codecs as codec
#getting linkedin main job search page
sauce = urllib.request.urlopen("https://www.linkedin.com/jobs/search/?keywords=computer%20science").read()
soup = bs.BeautifulSoup(sauce,"lxml")

print(soup.text.encode("utf-8"))

links = soup.find_all("a",{"class": "result-card__full-card-link"})

for i in links:
    subSauce = urllib.request.urlopen(i["href"]).read()
    subSoup = bs.BeautifulSoup(subSauce,"lxml")

    company = subSoup.find("a",{"class": "topcard__org-name-link topcard__flavor--black-link"})
    print(company.text.encode("utf-8"))
    jobTitle = subSoup.find("h2",{"class": "topcard__title"})
    print(jobTitle.text.encode("utf-8"))

    print("\n")

    desc = subSoup.find("div",{"class": "show-more-less-html__markup"})
    descText = desc.text
    list = []
    for j in desc.find_all("u"):
        descText = descText.replace(j.text,"")
    for j in desc.find_all("ul"):
        descText = descText.replace(j.text,"")
        list.append(j.text)

    print("WITHOUT LIST")
    print(descText.encode("utf-8"))
    print("\n")

    print("THE LIST")
    for i in list:
        print(i)

    print("\n")

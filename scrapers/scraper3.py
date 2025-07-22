# Linkedin Scraper
import requests
from bs4 import BeautifulSoup
import math
from datetime import datetime

def scrape_linkedin_jobs():
    target_url = "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer%20New%20Grad&location=San%20Francisco%20Bay%20Area&geoId=90000084&f_JT=F%2CI&f_E=1%2C2&f_TPR=r86400&position=1&pageNum=0"
    res = requests.get(target_url)
    soup=BeautifulSoup(res.text,'html.parser')
    alljobs_on_this_page=soup.find_all("li")
    job_ids=[]

    for x in range(0,len(alljobs_on_this_page)):
            base_card_div = alljobs_on_this_page[x].find("div", {"class": "base-card"})
            if base_card_div and base_card_div.get("data-entity-urn"):
                jobid = base_card_div.get("data-entity-urn").split(":")[3]
                if jobid not in job_ids:
                    job_ids.append(jobid)

    jobs=[]
    field={}

    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for j in range(0,len(job_ids)):

        resp = requests.get(target_url.format(job_ids[j]))
        soup=BeautifulSoup(resp.text,'html.parser')

        try:
            field["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            field["company"]=None

        try:
            field["title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
        except:
            field["title"]=None

        try:
            field["location"] = soup.find("span", class_="topcard__flavor--bullet").text.strip()
        except:
            field["location"]=None

        try:
            field["url"] = soup.find("a", class_="topcard__link")["href"]
        except:
            field["url"] = None

        # Datetime
        now = datetime.now()
        field["date_posted"] = f"{now.year}-{now.month}-{now.day}"

        # Source
        field["source"] = "Linkedin"


        jobs.append(field)
        field={}

    return jobs




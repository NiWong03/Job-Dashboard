#!/usr/bin/env python3
# test_scraper2.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scrapers.scraper3 import scrape_linkedin_jobs
from scrapers.scraper1 import scrape_github_simplifyjobs
from scrapers.scraper2 import scrape_github_simplifyjobs2

def test_scraper():
    print("Testing linkedin scraper...")
    jobs = scrape_linkedin_jobs()
    # jobs = scrape_github_simplifyjobs()
    # jobs = scrape_github_simplifyjobs2()
    
    print(f"Found {len(jobs)} jobs")
    
    # Print first few jobs as examples
    for i, job in enumerate(jobs[:5]):
        print(f"\nJob {i+1}:")
        print(f"  Company: {job['company']}")
        print(f"  Title: {job['title']}")
        print(f"  Location: {job['location']}")
        print(f"  Date Posted: {job['date_posted']}")
        print(f"  URL: {job['url']}")
        print(f"  Source: {job['source']}")

if __name__ == "__main__":
    test_scraper() 
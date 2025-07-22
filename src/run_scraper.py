import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scrapers.scraper1 import scrape_github_simplifyjobs
from scrapers.scraper2 import scrape_github_simplifyjobs2
from scrapers.scraper3 import scrape_linkedin_jobs

from db_init import init_db, upsert_job


def run_scraper():
    init_db()

    # Step 2: Run your scraper
    jobs = scrape_github_simplifyjobs()
    jobs2 = scrape_github_simplifyjobs2()
    jobs3 = scrape_linkedin_jobs()

    # Step 3: Insert each job into the DB
    for job in jobs:
        upsert_job(job)

    print(f"[✓] Done. Inserted {len(jobs)} job(s) into the database.")

    for job in jobs2:
        upsert_job(job)

    print(f"[✓] Done. Inserted {len(jobs2)} job(s) into the database.")

    for job in jobs3:
        upsert_job(job)

    print(f"[✓] Done. Inserted {len(jobs3)} job(s) into the database.")



# def test_scraper():
#     print("Testing GitHub SimplifyJobs scraper...")
#     jobs = scrape_github_simplifyjobs()
#     print(f"Found {len(jobs)} jobs")
#     for i, job in enumerate(jobs):
#         print(f"\nJob {i+1}:")
#         print(f"  Company: {job['company']}")

if __name__ == "__main__":
    run_scraper() 
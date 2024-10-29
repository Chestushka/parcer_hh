import csv


def save_t0_csv(jobs):
    file = open("jobs.csv", mode="w", encoding="utf-8-sig")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "salary", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return

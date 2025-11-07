def load_job_offers(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        jobs = f.read().split("\n\n")
    return jobs

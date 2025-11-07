from cv_parserer import parse_cv
from job_loader import load_job_offers
from recommender import JobRecommender
import os

def main():
    recommender = JobRecommender()

    job_path = "data/jobs/job_offers.txt"
    job_offers = load_job_offers(job_path)

    if not os.path.exists(recommender.index_path):
        print("Tworzę bazę wektorową z ofert pracy...")
        recommender.build_index(job_offers)
    else:
        recommender.load_index()

    cv_file = input("Podaj ścieżkę do CV (PDF/DOCX): ")
    cv_text = parse_cv(cv_file)

    print("\nRekomendowane oferty pracy:\n")
    recommendations = recommender.recommend(cv_text)

    for i, (job, score) in enumerate(recommendations, 1):
        print(f"#{i}: [Dopasowanie: {score:.2f}]\n{job}\n{'-'*40}")

if __name__ == "__main__":
    main()

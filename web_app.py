import os
import streamlit as st
from recommender import JobRecommender
from cv_parserer import parse_cv
from job_loader import load_job_offers

st.set_page_config(page_title="Rekomendator ofert pracy", layout="centered")
st.title("📄🔍 Automatyczna analiza CV i rekomendacja ofert pracy")

# Inicjalizacja rekomendatora
recommender = JobRecommender(index_path="embeddings/faiss_index.bin")

# Załaduj oferty i zbuduj indeks, jeśli nie istnieje
if not os.path.exists("embeddings/faiss_index.bin"):
    st.info("Tworzę bazę wektorową z ofert pracy...")
    job_offers = load_job_offers("job_offers.txt")
    recommender.build_index(job_offers)
else:
    recommender.load_index()  # <- to jest kluczowe

# Wybór pliku CV
uploaded_file = st.file_uploader("Wgraj swoje CV (PDF lub DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    try:
        cv_text = parse_cv(uploaded_file)  # 🔧 przekazujemy obiekt pliku, nie nazwę
        results = recommender.recommend(cv_text, top_k=5)

        st.success("🎯 Oto najlepsze dopasowania ofert pracy:")
        for i, (text, score) in enumerate(results, 1):
            with st.expander(f"{i}. Dopasowanie: {score:.2f}"):
                st.write(text)

    except Exception as e:
        st.error(f"Błąd przetwarzania CV: {e}")

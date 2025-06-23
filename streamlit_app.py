import streamlit as st
from scraper import scrape_google_ai_overview

st.title("Google AI Overview Brand Tracker")

query = st.text_input("Enter a search query", "best cold plunge brands")
brands = st.text_area("Enter brand names (one per line)", "Plunge\nRenu Therapy\nPolar Monkeys")

if st.button("Run Scraper"):
    result = scrape_google_ai_overview(query, brands.strip().splitlines())
    st.markdown("### AI Overview Text")
    st.write(result["overview"] or "No overview text found.")
    
    st.markdown("### Brand Mentions Found")
    for brand in result["mentions"]:
        st.success(f"✅ {brand}")

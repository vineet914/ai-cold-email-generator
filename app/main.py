import streamlit as st
import requests
from bs4 import BeautifulSoup

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def scrape_website(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    return text[:3000]


def create_streamlit_app(chain, portfolio):
    st.set_page_config(
        page_title="AI Cold Email Generator",
        page_icon="📧",
        layout="wide"
    )

    st.title("📧 AI Cold Email Generator")

    url_input = st.text_input(
        "Enter a job posting URL",
        value="https://jobs.nike.com/job/R-33460"
    )

   if st.button("Generate Email"):
    try:
        with st.spinner("Scraping job page and generating email..."):
            raw_text = scrape_website(url_input)
            cleaned_text = clean_text(raw_text)

            jobs = chain.extract_jobs(cleaned_text)
            if not jobs:
                st.error("No job information found on this page.")
                return

            portfolio.load_portfolio()

            skills = jobs[0].get("skills", [])
            links_metadata = portfolio.query_links(skills)

            links = []
            if links_metadata and links_metadata[0]:
                links = [item["links"] for item in links_metadata[0]]

            email = chain.write_mail(jobs[0], links)

            st.success("Email generated successfully!")
            st.text_area("Generated Email", email, height=350)

    except Exception as e:
        st.error(f"Error: {e}")



if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio)

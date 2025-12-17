import streamlit as st
import requests
from bs4 import BeautifulSoup

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def scrape_website(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)[:3000]


def create_streamlit_app(chain, portfolio):
    st.set_page_config(
        page_title="Cold Email Generator",
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
            raw_text = scrape_website(url_input)
            cleaned_text = clean_text(raw_text)

            jobs = chain.extract_jobs(cleaned_text)
            portfolio.load_portfolio()
            emails = chain.write_mail(jobs, portfolio)

            st.success("Email generated successfully!")
            st.write(emails)

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio)

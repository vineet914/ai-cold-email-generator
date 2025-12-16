import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


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

    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            # Load webpage
            loader = WebBaseLoader([url_input])
            docs = loader.load()

            # Limit content size to avoid context overflow
            content = docs[0].page_content[:3000]
            data = clean_text(content)

            # Generate email
            jobs = chain.extract_jobs(data)
            portfolio.load_portfolio()
            emails = chain.write_mail(jobs, portfolio)

            st.success("Email generated successfully!")
            st.write(emails)

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio)

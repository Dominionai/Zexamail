import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Email Generator")

    url_input = st.text_input("Enter a URL:", 
                               value="https://www.linkedin.com/jobs/view/4415145028/")
    text_input = st.text_area("Or paste job description directly:")

    tone = st.selectbox(
        "Select tone:",
        ["Professional", "Friendly", "Confident", "Concise", "Enthusiastic"]
    )

    # Right-aligned submit button
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        submit_button = st.button("Submit", use_container_width=True)

    if submit_button:
        try:
            if url_input:
                loader = WebBaseLoader([url_input])
                data = loader.load().pop().page_content
                data = clean_text(data)
            elif text_input:
                data = text_input
            else:
                st.warning("Please enter a URL or paste a job description.")
                return

            portfolio.load_portfolio()
            portfolio.load_industry_portfolio()

            jobs = llm.extract_jobs(data)

            for job in jobs:
                company = job.get("company", "")
                skills = job.get("skills", [])

                industry = llm.extract_industry(job, company)
                tech_links = portfolio.query_tech_links(skills)
                industry_links = portfolio.query_industry_links(industry)

                email = llm.write_mail(job, industry, tech_links, industry_links, tone)

                st.subheader(f"{job.get('role', 'Role')} @ {company} — {tone} tone")
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="🤖")
    create_streamlit_app(chain, portfolio, clean_text)
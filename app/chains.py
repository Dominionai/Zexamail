import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
            max_retries=2,
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTIONS:
            The text you scraped is from the career page of a company website.
            Extract the job posting and return it in JSON format containing:
            'company', 'role', 'experience', 'skills', 'description'.
            Return JSON only — no preamble, no explanation, no extra text.

            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too large, unable to parse jobs")

        return res if isinstance(res, list) else [res]

    def extract_industry(self, job, company):
        """Return a single industry label for the given job/company."""
        prompt_industry = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### COMPANY NAME:
            {company_name}

            ### INSTRUCTIONS:
            Based on the job description and company name, identify the single industry this
            company most likely operates in (e.g. Retail, Healthcare, Finance, Banking,
            Education, Logistics, Manufacturing, Travel and Hospitality, Media and
            Entertainment, Telecommunications, Energy and Utilities, Agriculture,
            Government and Public Sector, Sports and Fitness, Legal, Automotive, Non-profit,
            E-commerce, or another industry if none of these fit).
            Return ONLY the industry name — no preamble, no punctuation.

            ### INDUSTRY (NO PREAMBLE):
            """
        )
        chain_industry = prompt_industry | self.llm
        res = chain_industry.invoke(
            {"job_description": str(job), "company_name": company}
        )
        return res.content.strip()

    def write_mail(self, job, industry, tech_links, industry_links, tone):
        # Bug fix: industry is now a separate param; tech and industry links are separate
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CLIENT INDUSTRY:
            {industry}

            ### INSTRUCTIONS:
            You are Dominion, an agentic AI engineer skilled in LangChain, LangGraph,
            FastAPI, Python, NLP, MCP, ChromaDB, ML and DL. You have built agentic systems,
            autonomous agents, and AI infrastructure.
            Write a short, compelling cold email to the hiring team showing how you can
            deliver value to their company based on the job description above.
            - Mention that you understand the {industry} industry and its unique challenges.
            - Include these tech-stack portfolio links to show technical credibility: {tech_link_list}
            - Include these industry-specific portfolio links to show domain experience: {industry_link_list}
            - Write the email in a {tone} tone.
            Do not add a preamble.

            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke(
            {
                "job_description": str(job),
                "industry": industry,
                "tone": tone,
                "tech_link_list": tech_links,
                "industry_link_list": industry_links
            }
        )
        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
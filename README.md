# Zexamail 📧🤖

**Zexamail** is an AI-powered cold email generator built with LangChain, Groq, and ChromaDB. Paste in a job posting URL (or the raw job description), and Zexamail extracts the role details, identifies the company's industry, pulls the most relevant portfolio links from two separate vector stores, and drafts a tailored cold email — in the tone of your choice — ready to send to the hiring team.

Built as a portfolio project by **Dominion**, an agentic AI engineer, to demonstrate production-style RAG pipelines, structured LLM output, and retrieval-augmented personalization for job outreach.

---

## ✨ Features

- **Flexible input** — paste a job posting URL or the raw job description text directly.
- **Automatic job extraction** — an LLM chain parses scraped/pasted text into structured JSON (`company`, `role`, `experience`, `skills`, `description`).
- **Industry classification** — a second chain infers the company's industry (Retail, Healthcare, Finance, Education, etc.) from the job description and company name.
- **Dual-portfolio retrieval (RAG)** — two independent ChromaDB collections:
  - a **tech-stack portfolio**, queried by the skills required for the role
  - an **industry portfolio**, queried by the inferred industry
  
  so the generated email can reference both technical credibility and domain experience.
- **Tone control** — choose between Professional, Friendly, Confident, Concise, or Enthusiastic.
- **Streamlit UI** — a simple, single-page app for generating and copying emails.

---

## 🧱 Architecture

```
                ┌─────────────────┐
   URL / Text ─▶│   utils.py       │  (HTML/URL/noise cleanup)
                │  clean_text()    │
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │   chains.py      │
                │  extract_jobs()  │──▶ structured job JSON (Groq + JSON parser)
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │  chains.py       │
                │ extract_industry()│──▶ single industry label
                └────────┬────────┘
                         ▼
                ┌─────────────────┐          ┌───────────────────────┐
                │  portfolio.py    │◀────────▶│  vector_store/        │
                │  query_tech_links()         │  ChromaDB collections: │
                │  query_industry_links()     │  "portfolio",          │
                └────────┬────────┘          │  "industry_portfolio"  │
                         ▼                    └───────────────────────┘
                ┌─────────────────┐
                │  chains.py       │
                │  write_mail()    │──▶ final cold email (Groq)
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │   main.py        │  Streamlit UI renders the email
                └─────────────────┘
```

---

## 📁 Project structure

```
ZEXAMAIL/
├── .venv/                          # Python virtual environment
├── app/
│   ├── __pycache__/
│   ├── resources/                  # my_portfolio.csv, my_industry_portfolio.csv (runtime copy)
│   ├── vector_store/                # persisted ChromaDB collections
│   ├── chains.py                   # LLM chains: extract_jobs, extract_industry, write_mail
│   ├── main.py                     # Streamlit app entry point
│   ├── portfolio.py                # ChromaDB-backed tech/industry portfolio retrieval
│   └── utils.py                    # Text cleaning helpers
├── .env                             # GROQ_API_KEY (not committed)
├── .gitignore
├── chromadb.ipynb                   # Notebook used to prototype ChromaDB collection logic
├── email-playground.ipynb           # Notebook used to prototype the full extraction → email pipeline
├── my_industry_portfolio.csv        # Industry → portfolio link mapping
└── my_portfolio.csv                 # Tech stack → portfolio link mapping
```

---

## 🛠️ Tech stack

| Layer | Tool |
|---|---|
| LLM | [Groq](https://groq.com/) via `langchain-groq` (`llama-3.1-8b-instant`) |
| Orchestration | LangChain (LCEL-style chains) |
| Vector store | [ChromaDB](https://www.trychroma.com/) (persistent client, two collections) |
| Web scraping | `langchain_community.document_loaders.WebBaseLoader` |
| UI | [Streamlit](https://streamlit.io/) |
| Data | Pandas (CSV portfolio sources) |

---

## 🚀 Getting started

### 1. Clone the repo
```bash
git clone https://github.com/Dominionai/zexamail.git
cd zexamail
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install streamlit langchain-groq langchain-core langchain-community chromadb pandas python-dotenv
```
*(Consider freezing these into a `requirements.txt` with `pip freeze > requirements.txt`.)*

### 4. Set up environment variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Add your portfolio data
Populate `resources/my_portfolio.csv` (columns: `Techstack`, `Links`) and `resources/my_industry_portfolio.csv` (columns: `Industry`, `Links`) with your own project links.

### 6. Run the app
```bash
streamlit run app/main.py
```

---

## 📓 Notebooks

- **`chromadb.ipynb`** — sandbox for learning/prototyping ChromaDB's `add`, `get`, `query`, and `delete` operations with metadata-backed documents.
- **`email-playground.ipynb`** — end-to-end prototyping notebook: scraping a live job posting, extracting structured job data, classifying industry, querying both portfolio collections, and generating the final email — the logic that was later refactored into `chains.py`, `portfolio.py`, and `main.py`.

---

## 🗺️ Roadmap / ideas for extension

- Gmail OAuth2 integration to send generated emails directly.
- Scheduling follow-ups with APScheduler.
- Support for multiple job postings scraped in a single batch.
- Swap `WebBaseLoader` for a more robust scraper to handle JS-heavy job boards (e.g. LinkedIn).
- Add a `requirements.txt` / `pyproject.toml` for reproducible installs.

---

## 👤 Author

**Dominion (Egwuatu Chibuike Dominion)** — Computer Science student, coding instructor, and aspiring remote agentic AI engineer.

---

## 📄 License

This project is available under the MIT License — feel free to fork and adapt it for your own cold outreach workflow.

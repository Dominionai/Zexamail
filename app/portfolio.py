import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(
        self,
        tech_path="resources/my_portfolio.csv",
        industry_path="resources/my_industry_portfolio.csv",
    ):
        # --- Tech-stack portfolio ---
        self.tech_data = pd.read_csv(tech_path)

        # --- Industry portfolio ---
        self.industry_data = pd.read_csv(industry_path)

        # Shared ChromaDB client
        self.client = chromadb.PersistentClient("vector_store")

        # Two separate collections
        self.tech_collection = self.client.get_or_create_collection(name="portfolio")
        self.industry_collection = self.client.get_or_create_collection(
            name="industry_portfolio"
        )

    def load_portfolio(self):
        """Load tech-stack entries into the tech collection."""
        if not self.tech_collection.count():
            for _, row in self.tech_data.iterrows():
                self.tech_collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())],
                )

    def load_industry_portfolio(self):
        """Load industry entries into the industry collection."""
        if not self.industry_collection.count():
            for _, row in self.industry_data.iterrows():
                self.industry_collection.add(
                    documents=row["Industry"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())],
                )

    def query_tech_links(self, skills):
        """Query tech-stack portfolio by skills list."""
        return (
            self.tech_collection.query(
                query_texts=skills,  # Bug fix: was query_text (singular)
                n_results=2,
            ).get("metadatas", [])
        )

    def query_industry_links(self, industry):
        """Query industry portfolio by industry string."""
        return (
            self.industry_collection.query(
                query_texts=[industry],  # Bug fix: was query_text, also wrap in list
                n_results=1,
            ).get("metadatas", [])
        )
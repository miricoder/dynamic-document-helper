import os
from typing import Any
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

# from web_scraper import scrape_website  # Import the scrape_website function
# from backend.web_scraper import scrape_website
from web_scraper import scrape_website


from dotenv import load_dotenv

load_dotenv()

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)


class SimpleDocument:
    def __init__(self, content, metadata):
        self.page_content = content
        self.metadata = metadata


def ingest_docs(website_url: str) -> Any:
    # Call scrape_website function to get the scraped data
    scraped_data = scrape_website(website_url)  # Use the provided website_url

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )

    # Create a SimpleDocument with the scraped data
    document = SimpleDocument(content=scraped_data, metadata={"source": website_url})

    # Split the document into chunks
    documents = text_splitter.split_documents(documents=[document])
    print(f"Splitted into {len(documents)} chunks.")

    for doc in documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url, "content": doc.page_content})

    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(
        documents, embeddings, index_name="langchain-doc-index"
    )  # Replace with the actual index name
    print("*************** Added to Pinecone Vectorstore Vectors")


if __name__ == "__main__":
    # Get the website URL from the user or your frontend input mechanism
    website_url = input("Enter the URL of the website: ")

    # Call ingest_docs with the provided website_url
    ingest_docs(website_url)  # embeddings_input is the OPEN AI API Key

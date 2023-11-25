# from pinecone import Pinecone
from langchain.vectorstores import Pinecone
import pinecone
import os


def store_in_pinecone(data):
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
    )

    try:
        # Initialize Pinecone client and set API key using Pinecone.init
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"])

        # Initialize Pinecone index
        index = pinecone.Index(index_name="langchain-doc-index")

        # Insert the data into Pinecone
        index.upsert(ids=["1"], embeddings=[data])

        return "Data stored in Pinecone successfully"
    except Exception as e:
        return f"Error storing data in Pinecone: {str(e)}"


if __name__ == "__main__":
    from web_scrape import scrape_website

    def main():
        # Prompt the user to input a website URL
        website_url = input("Enter the URL of the website: ")

        # Call the scrape_website function with the provided URL
        scraped_data = scrape_website(website_url)

        if scraped_data:
            # Print the scraped data
            print("\nScraped Data:")
            print(scraped_data)

            # Store the data in Pinecone
            store_result = store_in_pinecone(scraped_data)
            print(store_result)

    main()

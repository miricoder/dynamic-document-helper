import os
from dotenv import load_dotenv

load_dotenv()
import requests
from bs4 import BeautifulSoup
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.agents import tool

# Step 1: Scrape data from the website
url = input("Enter the URL of the website you want to scrape: ")
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
text = soup.get_text()


# Step 2: Split the text into chunks before storing vector store
def split_text(text, chunk_size):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


chunks = split_text(text, 1000)

# Step 3: Send the split data into chunks of data and store in Pinecone
pinecone_api_key = os.environ["PINECONE_API_KEY"]  # "your_pinecone_api_key"
pinecone_index_name = "langchain-doc-index"  # "your_pinecone_index_name"

pinecone_tool = Tool(api_key=pinecone_api_key, index_name=pinecone_index_name)

for chunk in chunks:
    pinecone_tool.store(chunk)

# Step 4: Scrape data from any user-given website link to respond to any user queries
llm = ChatOpenAI(model="gpt-4", temperature=0)


def answer_question(question):
    response = llm.ask(question)
    return response


question = input("What would you like to ask? ")
answer = answer_question(question)
print(answer)

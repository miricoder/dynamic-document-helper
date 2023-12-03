# Retrieve from Vectorstore

import os
from typing import Any, Dict, List
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import ConversationChain
import pinecone
from dotenv import load_dotenv

load_dotenv()

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = Pinecone.from_existing_index(
        index_name="langchain-doc-index", embedding=embeddings
    )
    chat = ChatOpenAI(verbose=True, temperature=0)
    # qa = RetrievalQA.from_chain_type(
    #     llm=chat,
    #     chain_type="stuff",
    #     retriever=docsearch.as_retriever(),
    #     return_source_documents=True,
    # )

    # How we can integrate Conversational Chat memory into  our App...
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
        # memory=ConversationBufferMemory()
    )
    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    # print(run_llm(query="According to the article when will the Bitcoin Price reach $100,000? Summarize your response in single senctence."))
    # print(run_llm(query="Who is Karlsson-on-the-Roof?"))
    # print(run_llm(query="When did this cartoon become popular in Soviet Union?"))
    # print(run_llm(query="Who is Elon Musk?"))
    # print(run_llm(query="What was the volume on Nov 27, 2023?"))
    # print(run_llm(query="Who is Flluffy?"))
    print(run_llm(query="What is jiu-jitsu? Explain in sigle sentence please."))

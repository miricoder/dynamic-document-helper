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


def run_llm(
    query: str,
    api_key: str,
    pinecone_api_key: str,
    pinecone_environment: str,
    chat_history: List[Dict[str, Any]] = [],
) -> Any:
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

    # Initialize OpenAIEmbeddings with the provided api_key
    embeddings = OpenAIEmbeddings(api_key=api_key)
    docsearch = Pinecone.from_existing_index(
        index_name="langchain-doc-index", embedding=embeddings
    )

    # Explicitly provide the api_key when initializing ChatOpenAI
    chat = ChatOpenAI(api_key=api_key, verbose=True, temperature=0)  # Corrected line

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    openai_api_key = input("Please Enter your OPEN AI API KEY: ")
    pinecone_api_key = input("Please Enter your PINECONE API KEY: ")
    pinecone_environment = input("Please Enter your PINECONE ENVIRONMENT REGION: ")

    print(
        run_llm(
            query="What is the article mentioning about Vlad Tenev?",
            api_key=openai_api_key,
            pinecone_api_key=pinecone_api_key,
            pinecone_environment=pinecone_environment,
        )
    )

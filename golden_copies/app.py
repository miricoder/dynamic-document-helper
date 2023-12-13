import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from typing import Set
import time
from backend.core import run_llm
from backend.ingestion2 import ingest_docs

# from backend.web_scraper import scrape_website
load_dotenv()


def main():
    st.title("Scrape any website, Store it and Chat with it....")

    # Step 1: User Enters OPEN AI API Key
    openai_api_key = st.text_input("Enter you OpenAI API Key:")
    if not openai_api_key:
        st.warning("Please enter your OpenAI Key.")
        st.stop()
    # Step 2: Verify the OpenAI API Key
    # Implement your OpenAI API Key verification logic here

    # Step 3: User Enters website link
    website_link = st.text_input("Enter the website link:")
    ingest_docs(website_link)
    message(
        "Web Scraping the text off of the link you have shared to ingest it into DB for further retrieval"
    )
    if not website_link:
        st.warning("Please enter a webite link.")
        st.stop()
    # Step 4: Web Scraping and Ingesting

    # Step 5: Chat Area and core.py logic implementation
    st.subheader("Chat")
    # user_input = st.text_input(
    #     "Query the Link you have provided for any information....."
    # )
    # if user_input:
    # Implement your chatbot logic here
    # st.info("Chatbot response: ....")  # Replace with actual chatbot response
    prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

    if "user_prompt_history" not in st.session_state:
        st.session_state["user_prompt_history"] = []

    if "chat_answer_history" not in st.session_state:
        st.session_state["chat_answer_history"] = []

    # Adding memory to our chat bot
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    def create_sources_string(source_urls: Set[str]) -> str:
        if not source_urls:
            return ""
        source_list = list(source_urls)
        source_list.sort()
        sources_string = "sources:\n"
        for i, source in enumerate(source_list):
            sources_string += f"{i+1}. {source}\n"
        return sources_string

    if prompt:
        with st.spinner("Generating Response..."):
            # time.sleep(3)
            generated_response = run_llm(
                query=prompt, chat_history=st.session_state["chat_history"]
            )
            # generated_response = run_llm(query=prompt)

            sources = set(
                [
                    doc.metadata["source"]
                    for doc in generated_response["source_documents"]
                ]
            )
            formatted_response = (
                f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
            )
            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_answer_history"].append(formatted_response)

            ## What is chat_history for?
            # Consider the following scenario when you are chatting with ChatGPT Bot or any other....
            # Prompt: Who created Langchain?
            # Bot-answer: Harrison Chase
            # Prompt: Do you have any videos of hime? (Note that we are just saying he, not specifying who "he" is)
            # Bot-answer: Sorry i don't have information on that. (Without prior chat memory present the Bot doesn't know
            #             who we are talking about unsless we explicitly ask for Specific Person's Youtube Videos)
            st.session_state["chat_history"].append(
                (prompt, generated_response["answer"])
            )

    if st.session_state["chat_answer_history"]:
        for generated_response, user_query in zip(
            st.session_state["chat_answer_history"],
            st.session_state["user_prompt_history"],
        ):
            message(user_query, is_user=True)
            message(generated_response)

        st.title("Streamlit Session Reset")

        # Your existing widgets and interaction code here

        # Button to clear the session
        if st.button("Reset Session"):
            st.caching.clear_cache()


if __name__ == "__main__":
    main()

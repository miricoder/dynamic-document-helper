import streamlit as st
from typing import Set
from backend.core2 import run_llm
# from core2 import run_llm
from backend.ingestion3 import ingest_docs
from openai import AsyncOpenAI
from langchain.embeddings import OpenAIEmbeddings
import asyncio
from streamlit_chat import message

# Function to validate OPEN AI API Key
async def validate_api_key(api_key=None) -> None:
    if api_key is None:
        api_key = st.text_input("Please Enter your OPEN AI API KEY:", type='password')

    client = AsyncOpenAI(api_key=api_key)

    try:
        # Attempt to create a chat completion for validation
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )

        # Check if the request was successful
        if chat_completion and hasattr(chat_completion, 'id'):
            st.success("API Key is valid. You can proceed to the chat page.")
            # Enable the chat functionality here
            st.session_state.api_key_valid = True
            st.session_state.api_key = api_key
        else:
            st.error("Invalid API Key. Please enter a valid key.")
            # Disable the chat functionality here
            st.session_state.api_key_valid = False

    except Exception as e:
        st.error("Error: {}".format(e))
        # Disable the chat functionality on error
        st.session_state.api_key_valid = False

# Function to handle web scraping and data ingestion
def scrape_and_ingest_data(website_link: str, api_key: str, pinecone_api_key: str, pinecone_environment: str):
    ingest_docs(website_link, api_key, pinecone_api_key, pinecone_environment)

# Function to run the chat logic
def run_chat(prompt: str, api_key: str, pinecone_api_key: str, pinecone_environment: str):
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
            # Pass the API key, pinecone_api_key, and pinecone_environment to run_llm
            generated_response = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history"],
                api_key=api_key,
                pinecone_api_key=pinecone_api_key,
                pinecone_environment=pinecone_environment
            )

            sources = set(
                [doc.metadata["source"] for doc in generated_response["source_documents"]]
            )
            formatted_response = (
                f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
            )
            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_answer_history"].append(formatted_response)

            st.session_state["chat_history"].append((prompt, generated_response["answer"]))

# Streamlit app
async def main():
    st.title("ChatGPT Interaction App")

    # Step 1: User enters OPEN AI API Key
    api_key = st.sidebar.text_input("Enter OPEN AI API Key:", type='password')

    # Step 2: User enters Pinecone API Key
    pinecone_api_key = st.sidebar.text_input("Enter Pinecone API Key:", type='password')

    # Step 3: User enters Pinecone Environment Region
    pinecone_environment = st.sidebar.text_input("Enter Pinecone Environment Region:", type='password')

    if st.sidebar.button("Validate API Key"):
        # (Integration of Code 1) Call the async validate_api_key function
        await validate_api_key(api_key)

        # Check if the API key is validated successfully
        if st.session_state.get('api_key_valid', False):
            st.sidebar.success("API Key validated successfully!")
            st.session_state.api_key_validated = True    
        else:
            st.sidebar.error("Invalid API Key. Please try again.")

    # Step 4: API Key validation successful, proceed to next steps
    if st.session_state.get('api_key_validated', False):
        # ... (Rest of your existing code in Code 2)

        # Step 5: User inputs website link for web scraping
        website_link = st.text_input("Enter Website Link for Web Scraping:", key="website_link")

        if st.button("Scrape and Ingest Data"):
            if website_link:
                # Pass the API key, pinecone_api_key, and pinecone_environment
                scrape_and_ingest_data(website_link, st.session_state.api_key, pinecone_api_key, pinecone_environment)
                st.success("Data scraped and ingested successfully!")
            else:
                st.warning("Please enter a valid website link.")

        # Step 6: User enters chat mode
        st.subheader("Chat Mode")

        # Allow the user to press Enter for sending the prompt
        new_chat_prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button("Submit")

        # Pass the API key, pinecone_api_key, and pinecone_environment to run_chat
        run_chat(new_chat_prompt, st.session_state.api_key, pinecone_api_key, pinecone_environment)

        # Button to reset chat
        if st.button("Reset Chat"):
            st.session_state["chat_history"] = []
            st.session_state["user_prompt_history"] = []
            st.session_state["chat_answer_history"] = []
            st.success("Chat history reset successfully!")

        # Display chat history
        if st.session_state.get("chat_answer_history"):
            history_zip = list(zip(
                st.session_state["chat_answer_history"], st.session_state["user_prompt_history"]
            ))
            for i, (generated_response, user_query) in enumerate(reversed(history_zip)):
                message(user_query, is_user=True, key=f"user_{len(history_zip) - i - 1}")
                message(generated_response, key=f"response_{len(history_zip) - i - 1}")

if __name__ == "__main__":
    asyncio.run(main())

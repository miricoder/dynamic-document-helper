import streamlit as st
from typing import Set
from backend.core import run_llm
from backend.ingestion2 import ingest_docs
from openai import AsyncOpenAI
import asyncio
from streamlit_chat import message

# Function to validate OPEN AI API Key
async def validate_api_key(api_key=None) -> None:
    if api_key is None:
        api_key = st.text_input("Please Enter your OPEN AI API KEY:")

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
        else:
            st.error("Invalid API Key. Please enter a valid key.")
            # Disable the chat functionality here
            st.session_state.api_key_valid = False

    except Exception as e:
        st.error("Error: {}".format(e))
        # Disable the chat functionality on error
        st.session_state.api_key_valid = False

# Function to handle web scraping and data ingestion
def scrape_and_ingest_data(website_link: str):
    ingest_docs(website_link)

# Function to run the chat logic
def run_chat(prompt: str):
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
            generated_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])

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
    api_key = st.sidebar.text_input("Enter OPEN AI API Key:")

    # New session state variables to track scraping and chat interactions
    if "scraping_performed" not in st.session_state:
        st.session_state["scraping_performed"] = False

    if "chat_interaction_started" not in st.session_state:
        st.session_state["chat_interaction_started"] = False

    if st.sidebar.button("Validate API Key"):
        await validate_api_key(api_key)

        if st.session_state.get('api_key_valid', False):
            st.sidebar.success("API Key validated successfully!")
            st.session_state.api_key_validated = True
        else:
            st.sidebar.error("Invalid API Key. Please try again.")

    if st.session_state.get('api_key_validated', False):
        # ... (Rest of your existing code in Code 2)

        # Step 3: User inputs website link for web scraping
        website_link = st.text_input("Enter Website Link for Web Scraping:", key="website_link")

        if st.button("Scrape and Ingest Data"):
            if website_link:
                scrape_and_ingest_data(website_link)
                st.success("Data scraped and ingested successfully!")
                # Set the flag when scraping is performed
                st.session_state["scraping_performed"] = True
                # Reset chat interaction flag
                st.session_state["chat_interaction_started"] = False

        # Step 4: User enters chat mode
        st.subheader("Chat Mode")

        # Check the flags before triggering the chat mode
        if st.session_state["scraping_performed"] and not st.session_state["chat_interaction_started"]:
            new_chat_prompt = st.text_input("Prompt", key="chat_prompt_manual", placeholder="Enter your message here...") or st.button(
                "Submit"
            )

            if new_chat_prompt:
                with st.spinner("🕊️"): 
                    run_chat(new_chat_prompt)
                    # Set the flag to indicate chat interaction has started
                    st.session_state["chat_interaction_started"] = True

        # Redesigned Reset button with graffiti text style
        if st.button("Reset Chat 🎨", key="reset_chat_button", help="Graffiti-style Reset Button"):
            st.session_state["chat_history"] = []
            st.session_state["user_prompt_history"] = []
            st.session_state["chat_answer_history"] = []
            st.success("Chat history reset successfully!")
            # Reset chat interaction flag when chat is reset
            st.session_state["chat_interaction_started"] = False

        # Display chat history
        if st.session_state.get("chat_answer_history"):
            for i, (generated_response, user_query) in enumerate(zip(
                st.session_state["chat_answer_history"], st.session_state["user_prompt_history"]
            )):
                message(user_query, is_user=True, key=f"user_{i}")
                message(generated_response, key=f"response_{i}")

if __name__ == "__main__":
    asyncio.run(main())

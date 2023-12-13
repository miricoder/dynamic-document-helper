import streamlit as st
from typing import Set
from backend.core import run_llm
from backend.ingestion2 import ingest_docs


# Function to validate OPEN AI API Key
def validate_api_key(api_key: str) -> bool:
    # Add your validation logic here
    # Return True if the API key is valid, otherwise False
    return True


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
            generated_response = run_llm(
                query=prompt, chat_history=st.session_state["chat_history"]
            )

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

            st.session_state["chat_history"].append(
                (prompt, generated_response["answer"])
            )


# Streamlit app
def main():
    st.title("ChatGPT Interaction App")

    # Step 1: User enters OPEN AI API Key
    api_key = st.sidebar.text_input("Enter OPEN AI API Key:")

    if st.sidebar.button("Validate API Key"):
        if validate_api_key(api_key):
            st.sidebar.success("API Key validated successfully!")
            st.session_state.api_key_validated = True
        else:
            st.sidebar.error("Invalid API Key. Please try again.")

    # Step 2: API Key validation successful, proceed to next steps
    if st.session_state.get("api_key_validated", False):
        # Step 3: User inputs website link for web scraping
        website_link = st.text_input(
            "Enter Website Link for Web Scraping:", key="website_link"
        )

        if st.button("Scrape and Ingest Data"):
            if website_link:
                scrape_and_ingest_data(website_link)
                st.success("Data scraped and ingested successfully!")
            else:
                st.warning("Please enter a valid website link.")

        # Step 4: User enters chat mode
        st.subheader("Chat Mode")

        # Allow user to press Enter for sending the prompt
        new_chat_prompt = st.text_input(
            "Prompt", key="new_chat_prompt", placeholder="Enter your prompt here..."
        )

        # Check if the user clicked "Send"
        if st.button("Send", key="new_chat_send"):
            run_chat(new_chat_prompt)

        # Display chat history
        if st.session_state.get("chat_answer_history"):
            for generated_response, user_query in zip(
                st.session_state["chat_answer_history"],
                st.session_state["user_prompt_history"],
            ):
                st.write(f"User: {user_query}")
                st.write(f"Bot: {generated_response}")

        # Step 5: Allow the user to input a new link and repeat steps 3 and 4
        st.sidebar.markdown("### Additional Options")
        if st.sidebar.button("Input New Website Link"):
            st.session_state.api_key_validated = False
            st.session_state.pop("chat_answer_history", None)
            st.session_state.pop("user_prompt_history", None)
            st.session_state.pop("chat_history", None)

            # Clear the existing input fiesld for a new website link
            st.session_state.pop("website_link", None)


if __name__ == "__main__":
    main()

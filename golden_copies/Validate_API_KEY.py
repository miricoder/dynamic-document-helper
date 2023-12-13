import streamlit as st
import asyncio
from openai import AsyncOpenAI


async def main(api_key=None) -> None:
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
        if chat_completion and hasattr(chat_completion, "id"):
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


if __name__ == "__main__":
    st.title("OpenAI Streamlit App")
    asyncio.run(main())

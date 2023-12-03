import streamlit as st
import asyncio
from openai import AsyncOpenAI

async def main(api_key=None) -> None:
    if api_key is None:
        api_key = st.text_input("Please Enter your OPEN AI API KEY:")

    client = AsyncOpenAI(api_key=api_key)

    try:
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
            st.success("Success! Chat completion ID: {}".format(chat_completion.id))
            # You can customize this success message further if needed.

        else:
            st.error("Unexpected response: {}".format(chat_completion))
            # You can customize this message for unexpected responses.

    except Exception as e:
        st.error("Error: {}".format(e))
        # You can customize this error message further if needed.

if __name__ == "__main__":
    st.title("OpenAI Streamlit App")
    asyncio.run(main())

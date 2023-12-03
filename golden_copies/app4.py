import asyncio
import os
import streamlit as st 
from typing import Set 
from key_validators.openai_key_validator import main

######
# Test whether the script will work in another script or not. 
# Comment out all UI before you test this
# ----------------------------------------
# def run_openai_script():
#     api_key = input("Please Enter your OPEN AI API KEY: ")
#     asyncio.run(main(api_key))

# if __name__ == "__main__":
#     run_openai_script()
# ----------------------------------------
######

def validate_openai_key(api_key):
    try:
        # Call the main function from your_latest_script to validate the OpenAI API key
        main(api_key)
        return True
    except Exception as e:
        return False

def main():
    st.title("OpenAI Key Validator")
    
    # Get user input for OpenAI API key
    api_key = st.text_input("Enter your OpenAI API Key:")
    
    # Validate the OpenAI API key
    if st.button("Validate"):
        st.write("Validating...")

        if validate_openai_key(api_key):
            st.success("**VALID OPEN AI API KEY**")
            # st.image("bruce_buffer.jpg", caption="IT'S TIME", use_column_width=True)
        else:
            st.error("INVALID OPEN AI API KEY. CHECK THE KEY AND RE-ENTER.")
            st.warning("Note: Make sure you have entered a valid OpenAI API key.")

if __name__ == "__main__":
    main()

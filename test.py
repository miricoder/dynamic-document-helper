import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print(f"Testing out the .env file \n {os.environ['OPENAI_API_KEY']}")

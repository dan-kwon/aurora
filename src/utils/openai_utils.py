import os
from openai import OpenAI
from dotenv import load_dotenv


def get_client():
    # Loading api key
    load_dotenv()
    openai_token = os.getenv("OPENAI_API_KEY")

    # Initialize client
    client = OpenAI(api_key=openai_token)
    return client

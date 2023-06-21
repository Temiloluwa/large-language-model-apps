import os
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
llm = OpenAI(openai_api_key=api_key)

def main(temperature: float):
    text = "What would be a good company name for a company that makes colorful socks?"
    print(llm(text))

if __name__ == "__main__":
    main(0.9)
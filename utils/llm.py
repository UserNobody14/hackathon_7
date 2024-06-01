import os
from dotenv import load_dotenv
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint

load_dotenv()
# OPENAI_API_KEY = os.environ["OPENAI_API_TOKEN"]
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

llm = OctoAIEndpoint(
    model_kwargs={
        "model": "mixtral-8x7b-instruct-fp16",
    },
    max_tokens=200,
    presence_penalty=0,
    temperature=0.1,
    top_p=0.9,
)

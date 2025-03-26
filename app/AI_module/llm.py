from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.8,
    max_tokens=None,
    timeout=None,
    max_retries=1,
)

parser = JsonOutputParser()

structured_output_llm = llm | parser

print("Initilized LLM successfully!")
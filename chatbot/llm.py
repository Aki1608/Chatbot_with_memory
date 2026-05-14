from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load API keys
load_dotenv()

# Connect to Groq's servers
print("Connecting to Groq...")
llm = ChatGroq(
    model="llama-3.1-8b-instant", # Using Meta's powerful Llama 3 model
    temperature=0.2,
)


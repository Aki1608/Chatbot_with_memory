import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationSummaryBufferMemory

# Load API keys (requires GROQ_API_KEY in .env)
load_dotenv()

class MemoryEngine:
    def __init__(self):
        print("Initializing Cognitive Memory Engine...")
        
        # Initialize the LLM
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.5,
        )
        
        # The Hybrid Memory Core
        # max_token_limit is set low (300) so we can easily watch the summarization trigger!
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=300 
        )
        
        # The Conversation Pipeline
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=False
        )

    def chat(self, user_input):
        """Processes user input and returns the AI response plus internal memory states."""
        
        # Generate the response
        ai_response = self.conversation.predict(input=user_input)
        
        # EXTRACTING MEMORY STATES FOR THE UI
        # State A: The LLM-Generated Summary
        summary = self.memory.moving_summary_buffer 
        if not summary:
            summary = "(Token limit not reached yet. No summary generated.)"
            
        # State B: The Raw Buffer (Recent Messages)
        buffer_messages = self.memory.chat_memory.messages
        buffer_text = ""
        for msg in buffer_messages:
            role = "User" if msg.type == "human" else "AI"
            buffer_text += f"{role}: {msg.content}\n\n"
            
        return ai_response, buffer_text, summary

    def clear_memory(self):
        """Wipes the memory core for a fresh start."""
        self.memory.clear()
        return "Memory completely wiped."
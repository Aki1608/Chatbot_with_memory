import gradio as gr
from memory_engine import MemoryEngine

# Initialize the backend engine
engine = MemoryEngine()

def process_chat(user_message, chat_history):
    """Bridges the Gradio UI with the LangChain memory engine."""
    
    # 1. Get response and memory states from the backend
    ai_response, raw_buffer, summary = engine.chat(user_message)
    
    # 2. Append using the modern dictionary format
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": ai_response})
    
    # 3. Return updated components
    return "", chat_history, raw_buffer, summary

def reset_chat():
    """Clears the backend memory and wipes the UI."""
    engine.clear_memory()
    return [], "", "Memory cleared."

# --- The UI Dashboard ---
# FIX 2: Removed the theme argument from the Blocks constructor
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Cognitive Chatbot: Memory Visualizer")
    gr.Markdown("Watch how the AI manages context limits! It keeps recent messages in a **Raw Buffer**, and compresses older ones into a **Summary** when it hits the token threshold.")
    
    with gr.Row():
        # Left Panel: The User Interface
        with gr.Column(scale=2):
            # FIX 1: Removed type="messages" (It is now the default in Gradio 6)
            chatbot = gr.Chatbot(height=500, label="Conversation")
            with gr.Row():
                msg = gr.Textbox(placeholder="Tell me your name and three facts about yourself...", show_label=False, scale=4)
                clear_btn = gr.Button("Clear Memory", scale=1)
        
        # Right Panel: The "Under the Hood" View
        with gr.Column(scale=1):
            gr.Markdown("### 🔍 Internal Memory State")
            raw_buffer_ui = gr.Textbox(label="Buffer Memory (Recent Messages)", lines=12, interactive=False)
            summary_ui = gr.Textbox(label="Summary Memory (Compressed History)", lines=8, interactive=False)

    # Event Triggers
    msg.submit(
        fn=process_chat, 
        inputs=[msg, chatbot], 
        outputs=[msg, chatbot, raw_buffer_ui, summary_ui]
    )
    
    clear_btn.click(
        fn=reset_chat, 
        inputs=None, 
        outputs=[chatbot, raw_buffer_ui, summary_ui]
    )

if __name__ == "__main__":
    # FIX 2: Moved the theme assignment to the launch method
    demo.launch(theme=gr.themes.Soft())
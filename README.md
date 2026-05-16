# Cognitive Chatbot: Hybrid Memory Visualizer

A full-stack, modular AI application that demonstrates advanced Large Language Model (LLM) context and session management. This project addresses a fundamental challenge in LLM engineering: maintaining a persistent conversation history across long sessions without exceeding the model's finite token context window or causing memory-overflow crashes.

The application implements a **hybrid memory pipeline** that retains recent interactions verbatim while autonomously utilizing an LLM in the background to compress older dialogue into a running summary. A custom dual-pane dashboard visualizes this internal cognitive state in real-time as you chat.

---

##  System Architecture & Data Flow

The codebase strictly adheres to the **Separation of Concerns** principle, isolating the user interface from the underlying machine learning components:

```
                  ┌──────────────────────────────┐
                  │      app.py (Gradio UI)      │
                  └──────────────┬───────────────┘
                                 │ User Input
                                 ▼
               ┌──────────────────────────────────┐
               │ memory_engine.py (MemoryEngine)  │
               └─────────────────┬────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           ▼                                           ▼
┌──────────────────────┐                     ┌────────────────────┐
│      Raw Buffer      │                     │  Summary Generator │
│ (Recent Text Tokens) │                     │ (Background LLM)   │
└──────────┬───────────┘                     └─────────┬──────────┘
           │ < max_token_limit                         │ > max_token_limit
           └─────────────────────┬─────────────────────┘
                                 ▼
                     ┌──────────────────────┐
                     │   Custom Prompt      │
                     │  (System Persona)    │
                     └───────────┬──────────┘
                                 │ Hydrated Prompt Context
                                 ▼
                     ┌──────────────────────┐
                     │  Groq Inference Engine│
                     │ (llama-3.1-8b-instant)│
                     └──────────────────────┘
```

1. **`app.py` (The Dashboard UI):** Built using modern Gradio Blocks. It accepts user input, displays the conversational dialogue, and features standalone diagnostic text areas that stream the real-time content of the AI's internal raw buffer and moving summary.
2. **`memory_engine.py` (The RAG/Memory Engine):** Orchestrates LangChain’s `ConversationSummaryBufferMemory` pipeline. It monitors session token counts, triggers background summarization when thresholds are passed, and formats state information back to the frontend.

---

## Project Structure

* `app.py` - The frontend entry point. It structures the multi-column layout, handles event listeners, manages state updates, and applies UI styling.
* `memory_engine.py` - The cognitive backend. It configures the Groq LLM client, constructs the `PromptTemplate`, runs the conversational pipeline, and exports raw and summary context states.
* `requirements.txt` - Dictates explicit project dependencies.

---

## Quick Start Guide

### 1. Environment Setup
Isolate your workspace dependencies by creating and starting a clean virtual environment:

```bash
# Clone and enter the directory
git clone <your-repo-url>
cd <your-repo-folder>

# Create the virtual environment sandbox
python -m venv venv

# Activate the sandbox (Mac/Linux)
source venv/bin/activate

# Activate the sandbox (Windows Command Prompt)
venv\Scripts\activate.bat

# Activate the sandbox (Windows PowerShell)
venv\Scripts\Activate.ps1
```

### 2. Dependency Installation
Install the strict pipeline libraries via `pip`:
```bash
pip install -r requirements.txt
```
*(Ensure your requirements file contains: `langchain`, `langchain-groq`, `python-dotenv`, and `gradio>=6.0.0`)*

### 3. Configure API Credentials
Create a file explicitly named `.env` in the root directory. Paste your Groq API console token into it:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

### 4. Launch the Dashboard
Run the primary application file:
```bash
python app.py
```
Open the local URL outputted to your terminal shell (e.g., `http://127.0.0.1:7860`) inside your browser to start interacting with the system.

---

## Hyperparameter Tuning Matrix

You can alter the entire cognitive capability, response style, and performance profile of the agent by adjusting the parameters initialized inside `memory_engine.py`:

| Component | Parameter | Allowed Range / Types | Default Value | Engineering Impact |
| :--- | :--- | :--- | :--- | :--- |
| **`ChatGroq`** | `temperature` | `0.0` to `2.0` | `0.7` | Controls model randomness. Set to **`0.0`** for factual/coding tasks to minimize hallucinations. Set to **`0.8+`** to maximize creative and witty personalities. |
| **`ChatGroq`** | `model` | `string` | `"llama-3.1-8b-instant"` | Toggles the processing core. Use `llama-3.1-8b-instant` for sub-second latency. Upgrade to `llama-3.3-70b-versatile` for heavy reasoning or advanced logic. |
| **`ChatGroq`** | `max_tokens` | `integer` | *None (Unlimited)* | Clamps the absolute output length of individual AI responses. Use this to force brief, concise, or punchy messaging. |
| **`Memory`** | `max_token_limit` | `integer` | `300` | **The Summarization Threshold.** Sets the token capacity before recent messages are deleted from the raw buffer and condensed into a summary paragraph. *Tune low (300-500) for rapid testing; tune high (2000+) for real-world deployments.* |
| **`Chain`** | `verbose` | `True` \| `False` | `True` | Standard logging tool. Set to `True` to force LangChain to stream the underlying raw text-payloads, state adjustments, and hidden execution prompts directly into your terminal. |

---

## Customizing System Behavior (Prompting)

The internal behavior and conversational guardrails are managed by a LangChain `PromptTemplate` inside `memory_engine.py`. You can change the agent's core identity by tweaking the string assigned to `custom_template`:

```python
custom_template = """You are a [Insert Persona Here]. 
Follow these rules strictly: [Insert Constraints Here].

Current conversation:
{history}

User: {input}
AI:"""
```
> **Critical Requirement:** The `{history}` and `{input}` tokens must remain exactly as named. LangChain relies on these placeholders to dynamically insert the moving memory buffers and incoming message payloads before routing the final text block to the cloud inference layer.
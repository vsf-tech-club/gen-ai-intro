# -*- coding: utf-8 -*-
"""Tavily Search with LLM and Gradio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pook5OAFJyGEqNP2gIgoib8YbQRrS1VW
"""

pip install tavily-python

## Please go to tavily.com and get a free api to continue and add to your secrets as TAVILY_API_KEY

from tavily import TavilyClient
import google.generativeai as genai
from google.colab import userdata

class ChatHistory:
    def __init__(self):
        self.history = []

    def add_message(self, message, search_result, ai_response):
        self.history.append({
            "message": message,
            "search_result": search_result,
            "ai_response": ai_response
        })

    def get_history(self):
        return self.history

def get_completion_from_messages(messages, model_name="gemini-2.0-flash", temperature=0):
    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )

    chat = model.start_chat()
    current_response = None

    for msg in messages:
        if msg['role'] == 'user':
            current_response = chat.send_message(msg['content'])

    return current_response.text

# Step 1: Setup API keys and clients
GOOGLE_API_KEY = userdata.get('GEMINI_API_KEY')
TAVILY_API_KEY = userdata.get('TAVILY_API_KEY')

# Configure APIs
genai.configure(api_key=GOOGLE_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
chat_history = ChatHistory()

def process_query(query):
    # Step 2: Get search results from Tavily with US news focus
    search_results = tavily_client.search(
        query,
        search_depth="advanced",
        include_domains=[
            "nytimes.com",
            "wsj.com",
            "usatoday.com",
            "washingtonpost.com",
            "latimes.com",
            "nypost.com",
            "foxnews.com",
            "cnn.com",
            "nbcnews.com",
            "abcnews.go.com",
            "cbsnews.com",
            "reuters.com",
            "bloomberg.com",
            "apnews.com"
        ],
        max_results=5  # Limit to top 5 most relevant results
    )

    # Step 3: Prepare context for Gemini Pro with US news focus
    context = f"""
    You are a US news specialist. Using only the following search results from major US news sources,
    provide a comprehensive answer that focuses on how this topic has been covered in US media and its impact
    on American audiences. If available, include relevant quotes from US news sources.

    Search Results:
    {search_results}

    Query: {query}

    Instructions:
    1. Only use information from the provided US news sources
    2. Focus on US media perspective and coverage
    3. Include specific US news source citations when possible
    4. If the topic has limited US coverage, acknowledge this fact
    """

    # Step 4: Get AI response using Gemini Pro
    messages = [{'role': 'user', 'content': context}]
    ai_response = get_completion_from_messages(messages)

    # Step 5: Store in chat history
    chat_history.add_message(query, search_results, ai_response)

    return {
        'query': query,
        'search_results': search_results,
        'ai_response': ai_response
    }

# Test the integration
query = "What is deepseek and what impact has had on US"
result = process_query(query)

print("Query:", result['query'])
print("\nAI Response:", result['ai_response'])
print("\nFull History:", chat_history.get_history())

pip install gradio

import gradio as gr

def gradio_process(query: str) -> str:
    """
    Processes the user query using the process_query function.
    """
    try:
        # Using the process_query function defined in the previous cell
        result = process_query(query)
        return result['ai_response']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create and launch the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# US News Chat AI")
    gr.Markdown("Enter a query about US news topics and get insights from our AI powered by Gemini Pro.")

    with gr.Row():
        input_text = gr.Textbox(
            lines=2,
            placeholder="Enter your query here...",
            label="Your Query"
        )
        output_text = gr.Textbox(
            lines=10,
            label="AI Response"
        )

    submit_btn = gr.Button("Submit")
    submit_btn.click(
        fn=gradio_process,
        inputs=input_text,
        outputs=output_text
    )

    gr.Examples(
        examples=[
            "Who is Lionel Messi and what impact has he had on US soccer since joining Inter Miami?",
            "What are the latest developments in AI regulation in the United States?",
            "How has the US housing market changed in recent months?"
        ],
        inputs=input_text
    )

demo.launch(share=True, debug=True)
import os
import openai
import pandas as pd
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import ServiceContext
from . import config as cfg
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

# Set openai API key here 
openai.api_key = cfg.LLM_API_KEY

def load_documents(folder_path):
    reader = SimpleDirectoryReader(folder_path)
    try: 
        documents = reader.load_data()
    except:
        print(f"Error Processing files!")
        documents = "";  
    return documents

def create_nodes(documents):
    return documents

def create_index(nodes, embed_model):
    text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)
    Settings.text_splitter = text_splitter
    index = VectorStoreIndex.from_documents(
        nodes,
        embed_model=embed_model, transformations=[text_splitter]
    )
    return index

def initialize_query_engine(folder_path):
    documents = load_documents(folder_path)
    nodes = create_nodes(documents)
    embed_model = OpenAIEmbedding()
    index = create_index(nodes, embed_model)
    query_engine = index.as_query_engine(similarity_top_k=3)
    return query_engine

def query_index(prompt, query_engine):
    response = query_engine.query(prompt)
    if len(response.source_nodes) > 0:
        return response.source_nodes
    else:
        return None

def generate_response(prompt, retrieved_nodes, chat_initializer):
    messages = chat_initializer.copy()
    messages.append({'role': 'user', 'content': prompt})
    for node in retrieved_nodes:
        if hasattr(node, 'text'):
            messages.append({'role': 'user', 'content': node.text})
        else:
            print(f"Skipping node: {node}")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=messages
    )
    print(f"Type:: {type(response.choices)}")
    # return response.choices[0].message.content
    return response.choices

def initialize_conversation():
    """
    Initialize a conversation with the user, allowing them to ask questions
    about candidate shortlisting based on the provided skillsets, industry, experience, and domain.
    The user can type 'exit' to end the conversation.
    """
    format = "response : Candidate_Name: Skill_Match_Percentage: Experience: Industry: Domain: Job_Title"
    delimiter = "####"

    chat_prompt = f"""You are an expert assistant who helps users shortlist candidates based on job descriptions (JD).
    You need to interact with the user to answer their questions about resume selection. Here is the format:

    {delimiter}
    You will go through the following chain of thoughts to provide information:
    Thought 1. Start with a message introducing yourself and asking how you can help with resume selection.
    Thought 2. If the user asks a question, retrieve relevant information from the provided candidate pool and match it with the required JD.
    Thought 3. Provide a concise and clear answer based on the retrieved information in {format}.
    Thought 4. Ask if the user needs help with anything else.
    {delimiter}

    {delimiter}
    Here is a sample conversation for you to learn from.
    {delimiter}

    Sample conversation 1:
    Assistant: Hello, I am an expert assistant. How can I help you with candidate selection for your role?
    User: Who is the best match for the role of Python Developer for e-commerce with skills like Python, Flask, API, and JavaScript?
    Assistant: Sure, let me check... Candidate John Doe has the best match for this role. He has 95% of the required skills, including Python, Flask, API, and JS, with 6 years of experience in the e-commerce domain. Is there anything else you need help with?
    User: No, that’s all. Thanks!
    Assistant: You're welcome! Have a great day!
    {delimiter}

    {delimiter}
    Sample conversation 2:
    Assistant: Hello, I am an expert assistant. How can I assist you with your candidate shortlisting?
    User: Can you shortlist candidates with Python and Flask skills who have worked in a Product company with at least 5 years of experience?
    Assistant: Let me check... Candidate Jane Smith has 90% skill match with Python and Flask and 7 years of experience in Product companies. Would you like to explore more candidates?
    User: Yes, please show me others.
    Assistant: Candidate Richard Roe has 85% match and 6 years of experience in a Product company. Do you need more information about them?
    User: No, that’s all for now.
    Assistant: Alright, have a nice day!
    {delimiter}

    {delimiter}
    Sample conversation 3:
    Assistant: Hello! How can I help you with the candidate shortlisting process?
    User: I’m looking for candidates with experience in both Product and Service companies for the role of Senior API Developer.
    Assistant: Sure, let me check... Candidate Alan Brown has 10 years of experience with API development in both Product and Service companies. He also has skills in Python, Flask, and JavaScript. Would you like to see more details?
    User: Yes, please.
    Assistant: Alan Brown has worked with e-commerce and finance domains and has led several API development teams. Would you like to schedule an interview?
    User: Not right now. Thanks!
    Assistant: You're welcome! Let me know if you need help later.
    {delimiter}

    Start with just the first message.
    """

    chat_init = [{'role': 'system', 'content': chat_prompt}]
    return chat_init

def query_response(prompt, query_engine, chat_initializer=None):
    if chat_initializer is None:
        chat_initializer = initialize_conversation()
    retrieved_nodes = query_index(prompt, query_engine)
    if not retrieved_nodes:
        return "I'm sorry, I couldn't find any information related to your query."
    return generate_response(prompt, retrieved_nodes, chat_initializer)
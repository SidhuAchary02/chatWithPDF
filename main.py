import os
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from openai import OpenAI
from db import db
from models import Chat
from datetime import datetime

def save_chat(username, question, answer):
    chat = Chat(username=username, question=question, answer=answer, timestamp=datetime.now())
    db.chats.insert_one(chat.dict())

def get_chat_history(username):
    return list(db.chats.find({"username": username}))

# Set GROQ API key
os.environ["GROQ_API_KEY"] = "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"

# Constants
pdfs_directory = "pdfs/"
index_directory = "vector_store/"
os.makedirs(pdfs_directory, exist_ok=True)
os.makedirs(index_directory, exist_ok=True)


# Embeddings - very fast
embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# Groq Client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

# Prompt template
template = """
you are a helpful assistant. answer the user's question strictly using only the information provided in the context below. do not use any outside knowledge. if the answer is not found in the context, say "i could not find that information in the document."

question: {question}  
context: {context}  
answer:
"""

# Upload PDF
def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

# Cache FAISS vectorstore per file
def create_or_load_vector_store(file_path):
    index_path = os.path.join(index_directory, os.path.basename(file_path) + ".pkl")
    if os.path.exists(index_path):
        with open(index_path, "rb") as f:
            return pickle.load(f)

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)

    db = FAISS.from_documents(chunks, embeddings)

    with open(index_path, "wb") as f:
        pickle.dump(db, f)

    return db

# Retrieve documents
def retrieve_docs(db, query, k=4):
    return db.similarity_search(query, k)


conversation_history = []

# Query model with conversation history
def question_pdf(question, documents):
    global conversation_history

    # Get the context from documents
    context = "\n\n".join([doc.page_content for doc in documents])

    # Add the user's question to the conversation history
    conversation_history.append(f"User: {question}")
    conversation_history.append(f"Context: {context}")

    # Construct the prompt with all previous messages
    # prompt = "\n".join(conversation_history) + f"\nAnswer:"

    prompt = template.format(question=question, context=context)


    # Make the API call with the full context
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Use appropriate model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512
    )

    # Get the model's answer
    answer = response.choices[0].message.content

    # Append the model's response to the conversation history
    conversation_history.append(f"Assistant: {answer}")

    return answer

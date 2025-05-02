# 📄 Chat with PDF (Streamlit App)

An intelligent document assistant that allows users to **upload PDFs** and **ask questions** about them using an LLM (LLaMA 3 via Groq API). Built with `Streamlit`, `FAISS`, `MongoDB`, and `Groq`.

---

## Features

- Chat with any uploaded PDF
- User authentication (signup & login with 7-day session validity)
- Chat history stored securely in MongoDB
- Fast, streaming LLM responses via Groq API
- Supports multiple users with individual chat sessions

---

## Technologies Used

- `Streamlit` for UI
- `MongoDB` for user & chat data
- `FAISS` + `HuggingFace` for semantic search
- `Groq API` for LLM responses
- `Sentence Transformers` for vector embeddings

---

## Setup Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/chat-with-pdf.git
cd chat-with-pdf

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create required folders
mkdir vector_store pdfs

# Set environment variables
export MONGODB_URI=your_mongo_uri
export GROQ_API_KEY=your_groq_api_key

# Run the app
streamlit run streamlit.py

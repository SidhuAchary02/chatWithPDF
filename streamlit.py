# import streamlit as st
# import main as main
# from auth import signup_user, login_user
# from main import save_chat, get_chat_history
# import db as db_func

# st.set_page_config(page_title="Chat with PDF", layout="centered")

# if "user" not in st.session_state:
#     auth.login()
#     st.stop()

# st.title("📄 Chat with your PDF")

# # Initialize chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []  # List of (question, answer) tuples
# if "db" not in st.session_state:
#     st.session_state.db = None
# if "uploaded_file_name" not in st.session_state:
#     st.session_state.uploaded_file_name = None

# # Upload PDF
# uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

# if uploaded_file:
#     # Save and load vector store only once
#     if uploaded_file.name != st.session_state.uploaded_file_name:
#         main.upload_pdf(uploaded_file)
#         st.session_state.db = main.create_or_load_vector_store(
#             "pdfs/" + uploaded_file.name)
#         st.session_state.uploaded_file_name = uploaded_file.name
#         st.session_state.chat_history.clear()  # Clear old history for new PDF

#     # Input box for user's question
#     # user_input = st.text_input("Ask a question:", key="user_input")
#     user_input = st.chat_input("Ask a question")

#     # When user submits a question
#     if user_input:
#         # Search related documents
#         related_docs = main.retrieve_docs(st.session_state.db, user_input)

#         # Get answer from LLM
#         answer = main.question_pdf(user_input, related_docs)

#         # Add to chat history
#         st.session_state.chat_history.append((user_input, answer))

#         # Clear input field
#         st.session_state.user_input = ""

# # Display chat history
# for q, a in st.session_state.chat_history:
#     with st.chat_message("user"):
#         st.markdown(q)
#     with st.chat_message("assistant"):
#         st.markdown(a)


import streamlit as st
import main as main
import auth
from main import save_chat, get_chat_history

st.set_page_config(page_title="Chat with PDF", layout="centered")

# Check login
if not auth.is_logged_in():
    auth.auth_form()
    st.stop()

username = st.session_state["user"]
st.sidebar.success(f"Logged in as: {username}")
if st.sidebar.button("🚪 Logout"):
    auth.logout()

st.title("📄 Chat with your PDF")

# Chat session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [(item["question"], item["answer"]) for item in get_chat_history(username)]
if "db" not in st.session_state:
    st.session_state.db = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    if uploaded_file.name != st.session_state.uploaded_file_name:
        main.upload_pdf(uploaded_file)
        st.session_state.db = main.create_or_load_vector_store("pdfs/" + uploaded_file.name)
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.chat_history.clear()

    user_input = st.chat_input("Ask a question")

    if user_input:
        related_docs = main.retrieve_docs(st.session_state.db, user_input)
        answer = main.question_pdf(user_input, related_docs)

        st.session_state.chat_history.append((user_input, answer))
        save_chat(username, user_input, answer)

# Display chat
for q, a in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        st.markdown(a)

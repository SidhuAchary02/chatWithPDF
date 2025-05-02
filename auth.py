import hashlib
import streamlit as st
from db import db
from models import User
from datetime import datetime, timedelta

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(username, password):
    if db.users.find_one({"username": username}):
        return False, "Username already exists."
    user = User(username=username, password=hash_password(password))
    db.users.insert_one(user.dict())
    return True, "Signup successful. Please log in."

def login_user(username, password):
    user = db.users.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True, "Login successful."
    return False, "Invalid credentials."

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def auth_form():
    st.sidebar.title("🔐 Login / Signup")

    choice = st.sidebar.radio("Select Option", ("Login", "Signup"))
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Signup":
        if st.sidebar.button("Create Account"):
            success, msg = signup_user(username, password)
            st.sidebar.success(msg) if success else st.sidebar.error(msg)

    elif choice == "Login":
        if st.sidebar.button("Login"):
            success, msg = login_user(username, password)
            if success:
                st.session_state["user"] = username
                st.session_state["login_time"] = datetime.now().timestamp()
                st.sidebar.success(msg)
                st.rerun()
            else:
                st.sidebar.error(msg)

def is_logged_in():
    if "user" in st.session_state and "login_time" in st.session_state:
        login_time = datetime.fromtimestamp(st.session_state["login_time"])
        if datetime.now() - login_time < timedelta(days=7):
            return True
        else:
            logout()
            return False
    return False

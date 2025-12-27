# import streamlit as st
# from groq import Groq
# import json, os
# from datetime import date, datetime
# from pymongo import MongoClient

# mongo_client = MongoClient(st.secrets["MONGODB_URI"])
# db = mongo_client["aura_db"]
# chat_collection = db["chats"]


# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="AURA", layout="centered")

# # ---------------- GROQ CLIENT ----------------
# client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# # ---------------- CONSTANTS ----------------
# CHAT_FILE = "chats.json"
# TODAY = str(date.today())

# SYSTEM_PROMPT = """
# Your name is AURA.
# You are a personal AI assistant created by Abuzar Maroof.

# Rules:
# - If asked your name → say "My name is AURA."
# - If asked who made you → say "I was created by Abuzar Maroof."
# - Never mention OpenAI, Groq, Meta, or GPT.
# """

# # ---------------- CSS ----------------
# st.markdown("""
# <style>
# body { background-color: #0e0e0e; }

# .header {
#     text-align: center;
#     color: #92487A;
#     margin-bottom: 4px;
# }

# .sub {
#     text-align: center;
#     color: #aaa;
#     margin-bottom: 15px;
# }

# .msg-row { display: flex; margin-bottom: 10px; }
# .user-row { justify-content: flex-end; }
# .bot-row { justify-content: flex-start; }

# .user-msg {
#     background: #85409D;
#     color: white;
#     padding: 12px 16px;
#     border-radius: 18px 18px 4px 18px;
#     max-width: 70%;
# }

# .bot-msg {
#     background: #666F80;
#     color: white;
#     padding: 12px 16px;
#     border-radius: 18px 18px 18px 4px;
#     max-width: 70%;
# }

# .clear-btn {
#     display: flex;
#     justify-content: center;
#     margin-bottom: 15px;
# }
# .intro {
#     text-align: center;
#     color: #aaa;
#     font-size: 16px;
#     margin-top: 10px;
# }

# .help {
#     text-align: center;
#     color: #ffffff;
#     font-size: 20px;
#     font-weight: 500;
#     margin-bottom: 20px;
# }
            
# </style>
# """, unsafe_allow_html=True)

# # ---------------- HELPERS ----------------
# # def load_chats():
# #     if os.path.exists(CHAT_FILE):
# #         with open(CHAT_FILE, "r") as f:
# #             return json.load(f)
# #     return {}

# # def save_chats(data):
# #     with open(CHAT_FILE, "w") as f:
# #         json.dump(data, f, indent=2)

# def get_today_chat(username, today, session_key):
#     chat = chat_collection.find_one({
#         "username": username,
#         "date": today,
#         "session": session_key
#     })

#     if not chat:
#         chat = {
#             "username": username,
#             "date": today,
#             "session": session_key,
#             "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
#         }
#         chat_collection.insert_one(chat)

#     return chat

# def save_messages(chat_id, messages):
#     chat_collection.update_one(
#         {"_id": chat_id},
#         {"$set": {"messages": messages}}
#     )

# # ---------------- SESSION INIT ----------------
# if "username" not in st.session_state:
#     st.session_state.username = None

# if "session_start" not in st.session_state:
#     st.session_state.session_start = datetime.now().strftime("%H:%M:%S")

# # ---------------- USER NAME (ONCE ONLY) ----------------
# if st.session_state.username is None:
#     st.markdown("<h2 style='text-align:center'>Welcome </h2>", unsafe_allow_html=True)
#     name = st.text_input("Enter your name")
#     if name:
#         st.session_state.username = name.strip().title()
#         st.rerun()
#     st.stop()

# username = st.session_state.username

# # ---------------- LOAD CHAT DATA ----------------
# chat_doc = get_today_chat(username, TODAY, st.session_state.session_start)
# current_chat = chat_doc["messages"]


# # ---------------- HEADER ----------------
# st.markdown('<h1 class="header">AURA</h1>', unsafe_allow_html=True)

# st.markdown(
#     '<div class="intro">Your personal AI assistant</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     f'<div class="help">How can I help, {username}?</div>',
#     unsafe_allow_html=True
# )


# # ---------------- CLEAR CHAT BUTTON ----------------
# with st.container():
#     if st.button(" Clear Chat"):
#         st.session_state.session_start = datetime.now().strftime("%H:%M:%S")
#         st.rerun()

# # ---------------- CHAT DISPLAY ----------------
# for msg in current_chat:
#     if msg["role"] == "user":
#         st.markdown(f"""
#         <div class="msg-row user-row">
#             <div class="user-msg">{msg['content']}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     elif msg["role"] == "assistant":
#         st.markdown(f"""
#         <div class="msg-row bot-row">
#             <div class="bot-msg">{msg['content']}</div>
#         </div>
#         """, unsafe_allow_html=True)

# # ---------------- INPUT ----------------
# user_input = st.chat_input("Type your message...")

# if user_input:
#     current_chat.append({"role": "user", "content": user_input})

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=current_chat,
#         temperature=0.7,
#         max_tokens=250
#     )

#     reply = response.choices[0].message.content
#     current_chat.append({"role": "assistant", "content": reply})

#     save_messages(chat_doc["_id"], current_chat)

#     st.rerun()

import streamlit as st
from groq import Groq

from datetime import date, datetime
from pymongo import MongoClient

# ---------------- DB CONNECTION ----------------
mongo_client = MongoClient(st.secrets["MONGODB_URI"])
db = mongo_client["aura_db"]
chat_collection = db["chats"]

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AURA", layout="centered")

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

TODAY = str(date.today())

SYSTEM_PROMPT = """
Your name is AURA.
You are a personal AI assistant created by Abuzar Maroof.

Rules:
- If asked your name → say "My name is AURA."
- If asked who made you → say "I was created by Abuzar Maroof."
- Never mention OpenAI, Groq, Meta, or GPT.
"""

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #0e0e0e; }
.header { text-align:center;color:#92487A; }
.intro { text-align:center;color:#aaa;margin-top:10px; }
.help { text-align:center;color:#fff;font-size:20px;margin-bottom:20px; }
.msg-row { display:flex;margin-bottom:10px; }
.user-row { justify-content:flex-end; }
.bot-row { justify-content:flex-start; }
.user-msg { background:#85409D;color:white;padding:12px 16px;
            border-radius:18px 18px 4px 18px;max-width:70%; }
.bot-msg { background:#666F80;color:white;padding:12px 16px;
           border-radius:18px 18px 18px 4px;max-width:70%; }
</style>
""", unsafe_allow_html=True)

# ---------------- DB HELPERS ----------------
def get_today_chat(username, today, session_key):
    chat = chat_collection.find_one({
        "username": username,
        "date": today,
        "session": session_key
    })

    if not chat:
        chat = {
            "username": username,
            "date": today,
            "session": session_key,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
        }
        result = chat_collection.insert_one(chat)
        chat["_id"] = result.inserted_id

    return chat

def save_messages(chat_id, messages):
    chat_collection.update_one(
        {"_id": chat_id},
        {"$set": {"messages": messages}}
    )

# ---------------- SESSION INIT ----------------
if "username" not in st.session_state:
    st.session_state.username = None

if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now().strftime("%H:%M:%S")

# ---------------- USER NAME ----------------
if st.session_state.username is None:
    st.markdown("<h2 style='text-align:center'>Welcome</h2>", unsafe_allow_html=True)
    name = st.text_input("Enter your name")
    if name:
        st.session_state.username = name.strip().title()
        st.rerun()
    st.stop()

username = st.session_state.username

# ---------------- LOAD CHAT ----------------
chat_doc = get_today_chat(username, TODAY, st.session_state.session_start)
current_chat = chat_doc["messages"]

# ---------------- HEADER ----------------
st.markdown('<h1 class="header">AURA</h1>', unsafe_allow_html=True)
st.markdown('<div class="intro">Your personal AI assistant</div>', unsafe_allow_html=True)
st.markdown(f'<div class="help">How can I help, {username}?</div>', unsafe_allow_html=True)

# ---------------- CLEAR CHAT ----------------
if st.button("Clear Chat"):
    st.session_state.session_start = datetime.now().strftime("%H:%M:%S")
    st.rerun()

# ---------------- CHAT DISPLAY ----------------
for msg in current_chat:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-row user-row"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="msg-row bot-row"><div class="bot-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    current_chat.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=current_chat,
        temperature=0.7,
        max_tokens=250
    )

    reply = response.choices[0].message.content
    current_chat.append({"role": "assistant", "content": reply})

    save_messages(chat_doc["_id"], current_chat)
    st.rerun()

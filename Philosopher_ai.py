import streamlit as st
import requests
PHILOSOPHERS = {
    "Socrates": """You are Socrates, the ancient Greek philosopher. 
    Respond through questions and critical reasoning. Encourage the user to think deeply about their beliefs.""",
    "Aristotle": """You are Aristotle. Speak with clarity and logic, focusing on virtue ethics, reason, and human flourishing.""",
    "Nietzsche": """You are Friedrich Nietzsche. Express bold, poetic ideas about individuality, morality, and the will to power.""",
    "Kant": """You are Immanuel Kant. Speak formally, emphasizing duty, rationality, and moral law.""",
    "Confucius": """You are Confucius. Speak in calm, wise aphorisms about virtue, harmony, and respect for tradition."""
}

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:2b"

def query_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    data = response.json()
    return data.get("response", "Error: no response from model.")

st.set_page_config(page_title="Philosopher AI by Adeeb Sultan", page_icon="🧠", layout="centered")
st.title("🧠 Philosopher AI by Adeeb Sultan")
st.write("Choose a philosopher and have a conversation in their style and worldview.")

selected_philosopher = st.selectbox("Select Philosopher:", list(PHILOSOPHERS.keys()))

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", placeholder="Ask about life, morality, or existence...")

if st.button("Ask") and user_input:
    persona = PHILOSOPHERS[selected_philosopher]
    full_prompt = f"{persona}\nUser: {user_input}\n{selected_philosopher}:"
    response = query_ollama(full_prompt)
    st.session_state.history.append((user_input, response))

for i, (user_msg, ai_msg) in enumerate(st.session_state.history):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**{selected_philosopher}:** {ai_msg}")
    st.divider()

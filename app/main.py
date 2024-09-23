import streamlit as st
from generator import response_generator, response_writer


st.title("AI Chatbot")

# initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# if history exists, show it
for ch in st.session_state.chat_history:
    with st.chat_message(ch["role"]):
        st.write(ch["message"])

# when user send text, show it as the latest chat
if prompt := st.chat_input("What's up ?"):
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.chat_history.append({"role": "user", "message": prompt})
    
    with st.chat_message("assistant"):
        response = response_generator(prompt)
        st.write(response_writer(response))
        
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    
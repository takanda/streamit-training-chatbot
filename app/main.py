import streamlit as st
from generator import response_generator, GeminiClient
from assistant import CONVERSATION_LIST, assistant_response


st.title("Qiita Chatbot")
st.info("あなたにおすすめの最新記事を提案します。")

# init chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# init conversation number and system ask a first question
if "conversation_number" not in st.session_state:
    st.session_state.conversation_number = 0

    with st.chat_message("assistant"):
        response =  st.write(response_generator(CONVERSATION_LIST[st.session_state.conversation_number]))

# init gemini client
if "client" not in st.session_state:
    st.session_state.client = GeminiClient()


# if history exists, show it
for ch in st.session_state.chat_history:
    with st.chat_message(ch["role"]):
        st.write(ch["message"])

# when user send a text, show it as the latest chat
if input := st.chat_input("入力してください"):
    with st.chat_message("user"):
        st.write(input)
    
    st.session_state.chat_history.append({"role": "user", "message": input})
    st.session_state.conversation_number += 1
    
    # system response
    if st.session_state.conversation_number > 0:
        with st.chat_message("assistant"):
            if response := assistant_response(st.session_state.conversation_number, st.session_state, input):
                # loop conversation    
                if st.session_state.conversation_number == len(CONVERSATION_LIST) - 1:
                    st.session_state.conversation_number = 0
                    response += "\n" + CONVERSATION_LIST[st.session_state.conversation_number]
                st.write(response_generator(response))
            
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    
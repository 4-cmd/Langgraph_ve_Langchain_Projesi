import streamlit as st 
from  langchain_core.messages import HumanMessage,AIMessage

def printing_the_message():
        # Mesajları Yazdirir 
    for message in st.session_state.messages:
        if isinstance(message,HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message,AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)


def adding_the_state_message(icerik,is_human = True):
    if is_human:
        with st.chat_message("human"):
            st.markdown(icerik)
            st.session_state.messages.append(HumanMessage(icerik))
    else:
        with st.chat_message("assistant"):
            st.markdown(icerik)
            st.session_state.messages.append(AIMessage(icerik))


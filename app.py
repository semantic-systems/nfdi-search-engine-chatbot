# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_chat import message

from nfdichat.chat import NFDIChatModel
from nfdichat.datasets import ToyDataset

query, items = ToyDataset().fetch()
chatbot = NFDIChatModel()
chatbot.set(docs=items)

# Setting page title and header
st.set_page_config(page_title="NFDI4DS ChatBot", page_icon="🤖", layout="wide")

st.title("NFDI4DS ChatBot 🤖")
st.divider()

# Initialise session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

st.sidebar.title("NFDI4DS ChatBot 🤖")
sidebar_note = """
#### Greetings, I am the NFDI4DS ChatBot, a distinguished digital entity.
My purpose is to adeptly handle your inquiries, delivering meticulously
tailored responses in accordance with the parameters of your search.

###### [My Github Repository](https://github.com/semantic-systems/nfdi-search-engine-chatbot)
"""
st.sidebar.write(sidebar_note)


# generate a response
def generate_response(prompt):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    response = chatbot.chat(question=prompt)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    return response


# container for chat history
response_container = st.container()
# container for text box
container = st.container()
# clear conversation button
counter_placeholder = st.sidebar.empty()
clear_button = st.button("Clear Conversation", key="clear")

if clear_button:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    chatbot.reset(docs=items)


with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area(
            "Human", placeholder="Enter your message here.", key="input", height=30
        )
        submit_button = st.form_submit_button(label="Send Message")

    if submit_button and user_input:
        with st.spinner("NFDI4DS ChatBot 🤖: Let me to think! 🤔"):
            output = generate_response(user_input)
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)

if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i))

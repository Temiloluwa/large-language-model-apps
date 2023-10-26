import re
import json
import requests
import streamlit as st
from st_pages import  add_page_title
from lingua_trainer import send_post_request, send_streaming_post_request

# FAST API server port
HOST='backend'
SERVER_PORT=8100

add_page_title() 
st.subheader("Give a German word and Explore")
st.markdown("***You could vary the quantity of explanations you see***")

def explain_word(word:str, temperature:float):
    """Generates explanations for a word

    Args:
        word (str): _description_
        api_key (str): _description_
        temperature (float): _description_
    """
    url = f'http://{HOST}:{SERVER_PORT}/api/v1/challenges/word_explorer/word_explainer'
    data = {
        'word': word
    } 
    params = {'temperature': temperature}

    with st.spinner("Exploring..."):
        response = send_post_request(url, data, params)
        if type(response) is list:
            for item in response:
                st.subheader(word.capitalize())
                st.markdown(f"{item['explanation']}")
                st.markdown(f"**Synonyms:** {item['synonyms']}")
        else:
            st.error(f"An error occurred: {response}")
            st.stop()


def generate_sentences(word: str, num_sentences:int, temperature: float):
    """Generates sentences that further explains the word

    Args:
        word (str): _description_
        api_key (str): _description_
        num_sentences (int): _description_
        temperature (float): _description_
    """
    url = f'http://{HOST}:{SERVER_PORT}/api/v1/challenges/word_explorer/generate_sentences'
    data = {
        'word': word,
        'num_sentences': num_sentences
    } 
    params = {'temperature': temperature}

    st.subheader("Explanations")
    answer_placeholder = st.empty()
    answers = ""

    with st.spinner("Exploring..."):
        replace_text = lambda x, y, z, text: re.sub(rf'\[{x}\]|\[{y}\]', f"**{z}:** ", text)
        response = send_streaming_post_request(url, data, params)
        if type(response) is requests.Response:
            for it, chunk in enumerate(response.iter_content(chunk_size=30)):
                answers += chunk.decode("utf-8")
                answers = re.sub(r'\[Context1\]|\[context1\]', "**Background:** ", answers)
                answers = re.sub(r'\[Context[2-9]\]|\[context[2-9]\]', "\n_______\n **Background:** ", answers)
                answers = re.sub(r'\[German(\d+)\]|\[german(\d+)\]', "\n**You could say in German:** ", answers)
                answers = re.sub(r'\[English(\d+)\]|\[english(\d+)\]', "\n**In English:** ", answers)
                answer_placeholder.markdown(f"{answers}")
        else:
            st.error(f"An error occurred: {response}")
            st.stop()
  
with st.sidebar:
    temperature = st.slider("Select a temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.1)
    
word = st.text_input("Enter a word:")
num_sentences = st.slider("Number of sentences to generate:", min_value=1, max_value=5, value=1, step=1)

if st.button("Explore"):
    if not word:
        st.warning("Please enter a word.")
    else:
        explain_word(word, temperature)
        generate_sentences(word, num_sentences, temperature)
import streamlit as st
import json
from apps.utils import send_post_request, send_streaming_post_request
from st_pages import Page, Section, add_page_title, show_pages

show_pages(
    [
        Page("run.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Section(name="Lingua Trainer", icon=":teacher:"),
        Page("apps/word_explorer.py", "Word Explorer", ":books:"),
    ]
)

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
    url = 'http://localhost:8100/api/v1/challenges/word_explorer/word_explainer'
    data = {
        'word': word
    } 
    params = {'temperature': temperature}

    with st.spinner("Exploring..."):
        response = send_post_request(url, data, params)
        if response.get('status') == 200:
            explanations = response['body']
            for item in explanations:
                st.subheader(word.capitalize())
                st.markdown(f"{item['explanation']}")
                st.markdown(f"**Synonyms:** {item['synonyms']}")
        
        else:
            st.error(f"An error occurred: {response['body']}")
            st.stop()


def generate_sentences(word: str, num_sentences:int, temperature: float):
    """Generates sentences that further explains the word

    Args:
        word (str): _description_
        api_key (str): _description_
        num_sentences (int): _description_
        temperature (float): _description_
    """
    url = 'http://localhost:8100/api/v1/challenges/word_explorer/generate_sentences'
    data = {
        'word': word,
        'num_sentences': num_sentences
    } 
    params = {'temperature': temperature}

    st.subheader("Explanations")
    with st.spinner("Exploring..."):
        response = send_streaming_post_request(url, data, params)
        for it, chunk in enumerate(response.iter_content(chunk_size=1000)):
            chunk = json.loads(chunk)
            st.markdown(f"**Background:** {chunk['context']}")
            st.markdown(f"**You could say in German:** {chunk['german sentence']}")
            st.markdown(f"**In English:** {chunk['english translation']}")
            st.markdown("---")
            if it == num_sentences - 1: break
        else:
            st.error(f"An error occurred: {response}")
            st.stop()


if 'api_key' not in st.session_state:
    st.warning("Please supply an OpenAI api key and ensure to deactive it once you are done.")
    
with st.sidebar:
    st.title("API Key")
    def form_callback():
        st.session_state['api_key'] = st.session_state['api_key_temp']
        st.session_state['api_key_temp'] = ""

    with st.form(key='api_form'):
        _ = st.text_input("Enter your API key:", key='api_key_temp')
        api_key_submit = st.form_submit_button(label='Supply API key', on_click=form_callback)
    temperature = st.slider("Select temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.1)
    
word = st.text_input("Enter a word:")
num_sentences = st.slider("Number of sentences to generate:", min_value=1, max_value=5, value=1, step=1)

if st.button("Explore"):
    if not word:
        st.warning("Please enter a word.")
    else:
        explain_word(word, temperature)
        generate_sentences(word, num_sentences, temperature)

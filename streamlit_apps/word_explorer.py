import streamlit as st
from lingua_trainer.app.word_explorer import word_explanator, sentence_generator, get_llm
from st_pages import Page, Section, add_page_title, show_pages

show_pages(
    [
        Page("app.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Section(name="Lingua Trainer", icon=":teacher:"),
        Page("streamlit_apps/word_explorer.py", "Word Explorer", ":books:"),
    ]
)

add_page_title() 

st.subheader("Give a German word and Explore")
st.markdown("***You could vary the quantity of explanations you see***")

gpt = None

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

if st.session_state.get('api_key', None):
    gpt = get_llm(st.session_state.get('api_key'), temperature)

if st.button("Explore"):
    if not word:
        st.warning("Please enter a word.")
    else:
        st.info("Exploring")
        explanations = word_explanator(word, gpt)
        for item in explanations:
            st.subheader(word.capitalize())
            st.markdown(f"{item['explanation']}")
            st.markdown(f"**Synonyms:** {item['synonyms']}")

        st.info("Exploring")

        sentences = sentence_generator(word, num_sentences, gpt)

        if sentences:
            st.subheader("Explanations")
            for item in sentences:
                st.markdown(f"**Background:** {item['context']}")
                st.markdown(f"**You could say in German:** {item['german sentence']}")
                st.markdown(f"**In English:** {item['english translation']}")
                st.markdown("---")

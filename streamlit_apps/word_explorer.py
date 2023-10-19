import streamlit as st
from lingua_trainer.app.word_explorer import word_explanator, sentence_generator
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

# User input for the word and number of sentences
word = st.text_input("Enter a word:")
num_sentences = st.number_input("Number of sentences to generate:", min_value=1, value=5)

if st.button("Explore"):
    if not word:
        st.warning("Please enter a word.")
    else:
        st.info("Exploring...")
        explanations = word_explanator(word)
        for item in explanations:
            st.subheader(word.capitalize())
            st.markdown(f"{item['explanation']}")
            st.markdown(f"**Synonyms:** {item['synonyms']}")

        st.info("Exploring")

        sentences = sentence_generator(word, num_sentences)

        if sentences:
            st.subheader("Explanations...")
            for item in sentences:
                st.markdown(f"**Background:** {item['context']}")
                st.markdown(f"**You could say in German:** {item['german sentence']}")
                st.markdown(f"**In English:** {item['english translation']}")
                st.markdown("---")

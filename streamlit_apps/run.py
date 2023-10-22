import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

app_list = [
    "📚 Word Explorer",
]

show_pages(
    [
        Page("run.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Section(name="Lingua Trainer", icon=":teacher:"),
        Page("apps/word_explorer.py", "Word Explorer", ":books:"),
    ]
)

add_page_title() 

def main_page():
    st.title("Welcome to LLM Apps!")
    st.subheader("Lingua Trainer")
    st.markdown(f"1. [{app_list[0]}](Word%20Explorer): Improve your German vocabulary learning")


if __name__ == "__main__":
    main_page()

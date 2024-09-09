import streamlit as st
from agent import generate_response
import os

# app title and subtitle
st.set_page_config(page_title="CooKin", page_icon=":fork_and_knife:")
st.title("CooKin")
st.caption(
    "Kin spécialiste en cuisine pour vous donner une recette selon votre"
    " localisation."
)

# check if API key is set
if "api_key" not in st.session_state:
    # set API key to None
    st.session_state["api_key"] = None

# if API key is set
if st.session_state["api_key"]:
    # set API key as environment variable
    os.environ["OPENAI_API_KEY"] = st.session_state["api_key"]

    # form to enter city and get recipe
    with st.form("my_form"):
        # text area to enter city
        text = st.text_area(
            "Donnez moi votre ville, je vais regarder la météo "
            "et vous préparer une recette sur mesure : "
        )
        # submit button
        submitted = st.form_submit_button("Submit")
        # if submitted, generate response and display it
        if submitted:
            response = generate_response(text)
            st.write(response)
else:
    # if API key is not set, ask user to enter it
    api_key = st.text_input(
        "Entrez votre clé d'API ChatGPT pour commencer :",
        type="password",
    )
    # link to get API key
    st.markdown(
        "[Obtenez une clé d'API OpenAI](https://platform.openai.com/api-keys)",
    )
    # if API key is entered, set it and rerun the app
    if api_key:
        st.session_state["api_key"] = api_key
        st.rerun()

# sidebar with option to change API key
with st.sidebar:
    # button to change API key
    if st.session_state["api_key"]:
        if st.button("Changer de clé d'API"):
            # reset API key and rerun the app
            st.session_state["api_key"] = None
            st.rerun()

    # link to source code
    st.markdown("[source code](https://github.com/GuillaumeSachet/CooKin)")

import streamlit as st
from backend.utils import *


def RUN():
    st.sidebar.title("Smart Eye")
#creat a dropdown box in the side bar to choose app mode
    app_choice = st.sidebar.selectbox("Choose Mode",
                ["About","Run Application"])
    #checks the app mode and display appropriate content
    if app_choice == "About":
        about()

    elif app_choice == "Run Application":
        application()

def about():
    about_path = "README.md"
    f = open(about_path)
    code = f.read()
    st.markdown(code)

def application():
    picture = st.camera_input(label="Take a Picture", disabled=False)

    if picture is not None:
        #st.image(picture)
        img = read_img(picture)


RUN()
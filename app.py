import streamlit as st
name = st.text_input("Your name")
if st.button("Click me"):
    st.text("Hello,"+ name)


import streamlit as st
import pandas as pd


def log_reg():
    users = pd.read_table('users.txt', sep=' ', header=None)
    st.markdown('''<h2 style='color: blue;text-align: center;'>🏥Indicators of Heart Disease</h2>''', unsafe_allow_html=True)
    st.markdown('''
        <p style='font-family: Times New Roman'>The dataset originally comes from the CDC and is a major part of the Behavioral "
        "Risk Factor Surveillance System (BRFSS), which conducts annual telephone surveys to collect data on the health status of U.S. residents.</p>
        <p style='font-family: Times New Roman'>According to the CDC, heart disease is a leading cause of death for people of most races in the U.S. (African Americans, American Indians and Alaska Natives, and whites).<p>
        <p style='font-family: Times New Roman'>About half of all Americans (47%) have at least 1 of 3 major risk factors for heart disease: high blood pressure, high cholesterol, and smoking."
        "Other key indicators include diabetes status, obesity (high BMI), not getting enough physical activity, or drinking too much alcohol.</p>
        <p style='font-family: Times New Roman'>Data source: <a>https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease</a></p>
        ''', unsafe_allow_html=True)

    st.text_input(label="**username**", key="username", placeholder="Please enter your username")
    st.text_input(label="**password**", key="password", type='password', placeholder="Please enter the corresponding password")
    if st.button("Login", type="primary"):
        if st.session_state["username"] not in users[0].tolist():
            st.error('No such user')
            st.stop()
        elif st.session_state["username"] in users[0].tolist() and st.session_state["password"] == users.set_index(0).loc[st.session_state["username"]][1]:
            st.session_state["user"] = st.session_state["username"]
            st.experimental_rerun()
        else:
            st.error('Login parameters are incorrect, please try again')
            st.stop()

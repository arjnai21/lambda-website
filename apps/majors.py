import streamlit as st
import pandas as pd

def app(db):

    st.title("Majors List")

    #majorsFilter = st.text_input(label='Filter')

    allMajors = sorted(list(db.get_collection('majors').find()), key=lambda x: x['name'])

    majorTable = pd.DataFrame([m['name'] for m in allMajors], columns=['Name'])

    st.table(majorTable)
    
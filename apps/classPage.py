import streamlit as st

def app(classInfo):

    st.title(f"{classInfo['id']}: {classInfo['name']}")

    semesters = sorted(classInfo['semesters'], key=lambda x: x['year'][-4:])

    for s in semesters:

        st.header(s['year'])

        for name in s['usernames']:

            st.write(name)
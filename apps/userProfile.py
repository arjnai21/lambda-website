import streamlit as st

def app(userInfo):

    st.title(f"Profile for {userInfo['name']}")
    
    st.header("Contact Information")
    st.write(f"Email: {userInfo['email']}")
    st.write(f"Phone Number: {userInfo['phoneNumber']}")

    st.header(f"School Information")
    st.write(f"Year: {userInfo['year']}")
    st.write(f"Major: {userInfo['major']}")
    st.write(f"Double Major: {userInfo['doubleMajor']}")
    st.write(f"Minor: {userInfo['minor']}")

    st.header("Class Information")

    for s in userInfo['semesters']:

        st.subheader(s['year'])

        for c in s['classes']:
            st.write(f"{c['classId']}: {c['className']}")
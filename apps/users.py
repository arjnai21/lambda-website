import streamlit as st
import pandas as pd

def filterUsers(users, filter):
    users = [u for u in users if filter.lower() in u['name'].lower()]

    return users

def app(db):
    st.title("Brother Information")

    nameFilter = st.text_input(label='Filter')

    allUsers = list(db.get_collection('users').find())

    allUsers = filterUsers(allUsers, nameFilter)

    users = [[u['name'], u['year'], u['major'], u['doubleMajor'], u['minor'], u['email'], u['phoneNumber']] for u in allUsers]

    userTable = pd.DataFrame(users, columns=['Name', 'Year', 'Major', 'Double Major', 'Minor', 'Email', 'Phone Number'])
    st.table(userTable)
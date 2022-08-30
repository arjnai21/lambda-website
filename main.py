import streamlit as st
from multiapp import MultiApp
import pymongo

from apps import upload_transcript, users, majors, classes, userProfile

st.set_page_config(
     page_icon="🧊",
     layout="wide",
 )

@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()
db = client.get_database('lambda')

usersDB = list(db.get_collection('users').find())
classDB = list(db.get_collection('classes').find())
majorsDB = list(db.get_collection('majors').find())

app = MultiApp(db)

# TODO somehow change current page onchange of each of the selects

app.add_app("Home Page", upload_transcript.app)
app.add_app("Users", users.app)
app.add_app("Classes", classes.app)
app.add_app("Majors", majors.app)
app.run()

userList = sorted([u['name'] for u in usersDB])
classList = sorted([c['id'] for c in classDB])
majorList = sorted([m['name'] for m in majorsDB])

userPage = st.sidebar.multiselect('View User Profile', userList)
classPage = st.sidebar.multiselect('View Class Info', classList)
majorPage = st.sidebar.multiselect('View Major Info', majorList)
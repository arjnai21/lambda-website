import streamlit as st
from multiapp import MultiApp
import pymongo

from apps import upload_transcript, users, majors, classes, userProfile, classPage, majorPage

st.set_page_config(
     page_icon="🧊",
     layout="wide",
 )

if 'app_view' not in st.session_state:
    st.session_state['app_view'] = 'main'

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

def changePage(type):
    st.session_state['app_view'] = type

app = st.sidebar.selectbox('Go To', app.apps, format_func=lambda app: app['title'], on_change=changePage, args=['main'])

userList = sorted([u['name'] for u in usersDB])
classList = sorted([c['id'] for c in classDB])
majorList = sorted([m['name'] for m in majorsDB])

userInput = st.sidebar.selectbox('View User Profile', userList, on_change=changePage, args=['userProfile'])
classInput = st.sidebar.selectbox('View Class Info', classList, on_change=changePage, args=['classPage'])
majorInput = st.sidebar.selectbox('View Major Info', majorList, on_change=changePage, args=['majorPage'])

if st.session_state['app_view'] == 'main':
    app['function'](db)
elif st.session_state['app_view'] == 'userProfile':
    userProfile.app(userInput)
elif st.session_state['app_view'] == 'classPage':
    classPage.app(classInput)
elif st.session_state['app_view'] == 'majorPage':
    majorPage.app(majorInput)
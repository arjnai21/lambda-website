import streamlit as st
import pandas as pd

def filterClasses(classes, filter):
    classes = [c for c in classes if filter in c['id'].lower() or filter in c['name'].lower()]

    return classes

def app(db):

    st.title("Classes List")

    classFilter = st.text_input(label='Filter')

    items = db.get_collection('classes').find()
    allClasses = sorted(list(items), key= lambda x: x['id']) 

    allClasses = filterClasses(allClasses, classFilter.lower())

    users = [[c['id'], c['name']] for c in allClasses]

    classTable = pd.DataFrame(users, columns=['Id', 'Name'])
    st.table(classTable)

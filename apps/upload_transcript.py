
import streamlit as st
import os
from scraper import extractMain

def app(db):

    users = db.get_collection('users')
    classes = db.get_collection('classes')
    majors = db.get_collection('majors')

    st.title('Lambda Database')
    
    st.write("Please submit your unofficial transcript below.")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        
        # Read file as bytes
        bytes_data = uploaded_file.getvalue()

        with open('transcripts/file.pdf', 'wb') as f:
            f.write(bytes_data)

        # extract information from pdf file
        userInfo, classInfo, majorInfo = extractMain('transcripts/file.pdf')

        os.remove('transcripts/file.pdf')

        st.write(f"Thank you for uploading your transcript {userInfo['name']}.")
        st.write(f'Update your information as necessary. Please provide contact information as comfortable.')

        name = st.text_input("Name", value=userInfo['name'])
        year = st.selectbox("Year", ['Freshman', 'Sophomore', 'Junior', 'Senior', '5th Year+'])
        email = st.text_input("Email", value=userInfo['email'])
        phoneNumber = st.text_input("Phone Number")

        st.text_area("Major", userInfo['major'])
        st.text_area("Double Major", userInfo['doubleMajor'])
        st.text_area("Minor", userInfo['minor'])

        userInfo['name'] = name
        userInfo['year'] = year
        userInfo['email'] = email
        userInfo['phoneNumber'] = phoneNumber

        # TODO Add validation
        st.button('Submit', on_click=uploadUser, args=[userInfo, classInfo, majorInfo, users, classes, majors])

def uploadUser(userInfo, classInfo, majorInfo, users, classes, majors):

    # Insert new user into database, replaces if name already exists
    users.replace_one({'name': userInfo['name']}, userInfo, upsert=True)

    # Insert new major into database
    # Need to check if major exists
    for major in majorInfo:

        oldMajor = majors.find_one({'name': major['name']})

        # If major is already in database
        if oldMajor:

            # Remove all previous majors to account for dropping major or changing from minor -> major
            oldMajor['users'] = list(filter(lambda x: x['name'] != userInfo['name'], oldMajor['users']))

            # Add new MajorUser
            oldMajor['users'].append(major['users'][0])

            # Replace Major object
            majors.replace_one({'name': major['name']}, oldMajor)

        # Otherwise, add new major
        else:
            majors.insert_one(major)


    # Insert all new classes
    # need to check if id exists
    for cls in classInfo:

        # get old class info then update it 
        oldClass = classes.find_one({'id': cls['id']})

        # if class is already in database
        if oldClass:

            # go through new semesters added
            for semester in cls['semesters']:

                # if new semester already in database, update names, use sorted to avoid duplicates
                if semester['year'] in [s['year'] for s in oldClass['semesters']]:

                    semesterToEdit = None
                    for s in oldClass['semesters']:
                        if s['year'] == semester['year']:
                            semesterToEdit = s

                    semesterToEdit['usernames'] = list(set(semesterToEdit['usernames'] + semester['usernames']))

                # otherwise, add new semester
                else:
                    oldClass['semesters'].append(semester)
            
            # replace given class
            classes.replace_one({'id': cls['id']}, oldClass)

        #otherwise add new class
        else:
            classes.insert_one(cls)

    return userInfo['name']


def allowed_file(filename):
    # fix, return True for now
    return True
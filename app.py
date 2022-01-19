from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from scraper import extractMain
import os
from bson.json_util import dumps

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/lambda"
app.config['UPLOAD_FOLDER'] = "pdf"
mongo = PyMongo(app)
users = mongo.db.get_collection('users')
classes = mongo.db.get_collection('classes')

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/users')
def displayUsers():
    testUsers = users.find()
    return render_template('users.html', users=testUsers)

@app.route('/getUsers/', methods=['GET'])
@app.route('/getUsers/<query>', methods=['GET'])
def getUsers(query = None):
    allUsersCursor = users.find()
    allUsers = list(allUsersCursor)
    if query:
        allUsers = filter(lambda x: query.lower() in x['name'].lower(), allUsers)
    return dumps(allUsers)

@app.route('/profile/<name>')
def displayUserProfile(name):
    user = users.find_one({'name': name})
    return render_template('profile.html', user = user)

@app.route('/classes')
def displayClasses():
    testClasses = classes.find()
    return render_template('classes.html', classes=testClasses)

@app.route('/getClasses/', methods=['GET'])
@app.route('/getClasses/<query>', methods=['GET'])
def getClasses(query = None):
    allClassesCursor = classes.find()
    allClasses = sorted(list(allClassesCursor), key= lambda x: x['id']) 
    if query:
        allClasses = filter(lambda x: query.lower() in x['id'].lower() or query.lower() in x['name'].lower(), allClasses)
    return dumps(allClasses)

@app.route('/classPage/<classId>')
def displayClassPage(classId):
    cls = classes.find_one({'id': classId})
    print(cls)
    return render_template('classPage.html', cls = cls)

@app.route('/upload', methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            uploadUser(file.filename)
            return redirect(request.url)

    return render_template('base.html')

def uploadUser(filename):
    # extract information from pdf file
    userInfo, classInfo = extractMain(filename)

    # insert new user into database
    # test for duplicates/updating user instead?
    users.find_one_and_replace({'name': userInfo['name']}, userInfo)

    # insert all new classes
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
            classes.find_one_and_replace({'id': cls['id']}, oldClass)

        #otherwise add new class
        else:
            classes.insert_one(cls)


def allowed_file(filename):
    # fix, return True for now
    return True

# to do:
# add ui to update user or hardcode user info if applicable (user/number/etc)
        # ui to add name/number/better email, pass in before uploading anything

# enable scraper to get year and double major

# add major page (combine major/minor)
    # major database-- name -> users: name, type (major/double/minor)\
    # need to standardize major/minor names, maybe store as all uppercase

# fix upload redirect
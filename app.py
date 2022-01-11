from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from scraper import extractMain
import os

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/lambda"
app.config['UPLOAD_FOLDER'] = "pdf"
mongo = PyMongo(app)
users = mongo.db.get_collection('users')

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/users')
def displayUsers():
    testUsers = users.find()
    return render_template('users.html', users=testUsers)

@app.route('/classes')
def displayClasses():
    return render_template('classes.html')

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
    userInfo, classInfo = extractMain(filename)


        
    users.insert_one(userInfo)

def allowed_file(filename):
    # fix, return True for now
    return True
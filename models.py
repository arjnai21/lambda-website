class User:
    def __init__(self, name, semesters, major=None, doubleMajor=None, minor=None, email=None, phoneNumber=None, year=None):
        self.name = name
        self.major = major
        self.doubleMajor = doubleMajor
        self.minor = minor
        self.email = email
        self.phoneNumber = phoneNumber
        self.year = year
        self.semesters = semesters

# Semesters with only year and list of classes
class Semester:
    def __init__(self, year, classes):
        self.year = year
        self.classes = classes

# Just stores id and name of each class
class ClassBasics:
    def __init__(self, classId, className):
        self.classId = classId
        self.className = className

# Semesters with only year and users of that year
class ClassSemester:
    def __init__(self, year, usernames):
        self.year = year
        self.usernames = usernames

# User: contains id, name, and list of semesters
class Class: 
    def __init__(self, classId, name, semesters):
        self.id = classId
        self.name = name
        self.semesters = semesters

# Major: contains name of major and list of people in that major
class Major:
    def __init__(self, name, users):
        self.name = name
        self.users = users

# Stores username and type of major
class MajorUser:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        
# todo maybe: create ToUser (converting dict to user?)



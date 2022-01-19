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

# todo maybe: create ToUser (converting dict to user?)

testSemester = Semester("Fall 2020",["C1","C2"])
testUser = User("Name1",[testSemester],["Major1"])



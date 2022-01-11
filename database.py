from pymongo import MongoClient
from models import Semester, User
from util import to_dict

client = MongoClient(port=27017)
db=client['users']
col = db['users']

testEntry = {
    "major":['testajor'],
    "name": "testName",
    "semesters": [
       { "year": "Spring2021",
         "classes": ["Class01","class02"]
       },
       {
         "year": "Spring2022",
         "classes": ["Class03"]
       }
    ]
}

testSemester = Semester("Fall 2020",["C1","C2"])
testUser = User("Name1",[testSemester],["Major1"])

print(to_dict(testUser))
#col.insert_one(to_dict(testUser))

#for x in col.find():
#    print(x)


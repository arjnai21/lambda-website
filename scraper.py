from pdfminer.high_level import extract_text
import re
from models import User, Semester, Class, ClassSemester, ClassBasics, Major, MajorUser
from util import to_dict

# Extract email/major/double major/minors
def extractBasics(text):
    # Establish regex for email
    emailPattern = "[\w\.]+@\w+\..*"
    matcher = re.compile(emailPattern)

    # later: check for edge cases/error proof
    emailMatch = matcher.search(text)
    email = emailMatch.group()
    emailIndex = emailMatch.start()
    
    # get date index to extract name
    datePattern = "As of:\s+\d{2}/\d{2}/\d{2}"
    matcher = re.compile(datePattern)
    dateMatch = matcher.search(text[:emailIndex])
    dateIndex = dateMatch.end()

    # extract name
    namePattern = "(?P<name>[a-zA-Z\-]+, ([a-zA-Z-]+ )*[a-zA-Z-]+)"
    matcher = re.compile(namePattern)
    name = matcher.search(text[dateIndex:emailIndex]).group()

    # Establish regex for major
    majorPattern = "Major:\s+(?P<major>[\w: | & | *]+)\n"
    matcher = re.compile(majorPattern)
    major = matcher.search(text).group('major')

    # Establish regex for double major
    doubleMajor = "None"
    doubleMajorPattern = "Double Major:\s+(?P<doubleMajor>[\w ]+)\n"
    matcher = re.compile(doubleMajorPattern)

    match = matcher.search(text)
    if match:
        doubleMajor = match.group('doubleMajor')

    # Establish regex for minor
    minor = "None"
    minorPattern = "Minor:\s+(?P<minor>[\w ]+)\n"
    matcher = re.compile(minorPattern)

    match = matcher.search(text)
    if match:
        minor = match.group('minor')
    
    return (name, email, major, doubleMajor, minor)

def extractClasses(curText):
    # Establish regex expressions for parts of each class
    # Class ID is 4 chars then 3 numbers with a potential letter at the end
    classIdRegex = "(?P<classID>\w{4}[\d]{3}\w?)"

    # Class Name is a series of strings (letters, dashes, ampersand) separated
    # by 1 space. Regex weirdness is to avoid spaces at end of match
    classNameRegex = "(?P<className>(([\da-zA-Z&\-,;/]+ )*[\da-zA-Z&\-,;/]+)|(\*Repeated Course\*))"
    
    # Grade List is just list of grades (letter followed by potential - or +)
    # Update if I forgot certain grades
    gradeListRegex = "(?P<grade>(A|B|C|D|P|F|W|NG)(\+|\-)?)\s"
    pattern = classIdRegex + "\s+" + classNameRegex + "\s+" + gradeListRegex

    matcher = re.compile(pattern)

    # Extract all class info into a list
    classes = []
    for match in matcher.finditer(curText):
        classes.append(match.groupdict())
    
    return classes

# Main method to extract all necessary info
def extractMain(filepath):

    # Use pdfminer to extract raw text from pdf
    text = extract_text(filepath)

    basics = extractBasics(text)
    
    # Establish regex to identify all semesters a student has taken classes in
    semesterRegex = "(?P<semester>(Fall|Spring|Summer I|Summer II|Winter)[ ]+[\d]{4})\s+MAJOR"
    matcher = re.compile(semesterRegex)

    endIndices = []
    semesters = []

    # Extract all semesters and indices in the text where this match was found
    for match in matcher.finditer(text):
        semesters.append(match.group('semester'))
        endIndices.append(match.end())

    numSemesters = len(semesters)

    finalClasses = {}

    # Call extractClasses only on the slice of the text between each semester to
    # only find classes for that given semester
    for i in range(numSemesters):

        slicedText = ""
        classes = []

        # Not most recent semester
        if i != numSemesters - 1:
            classes = extractClasses(text[endIndices[i]:endIndices[i+1]])
        # Most recent semester
        else:
            classes = extractClasses(text[endIndices[i]:])

        finalClasses[semesters[i]] = classes
    
    # print("Name: " + basics[0])
    # print("Email: " + basics[1])
    # print("Major: " + basics[2])
    # print("Double Major: " + basics[3])
    # print("Minor: " + basics[4])
    # for year, classes in finalClasses.items():
    #     print(year)
    #     for c in classes:
    #         print(c['classID'] + " " + c['className'] + " " + c['grade'])

    name = basics[0]
    email = basics[1]
    major = basics[2].strip().upper()
    doubleMajor = basics[3].strip().upper()
    minor = basics[4].strip().upper()

    # Put major/doubleMajor/minor in proper use for Mongo
    majorInfo = []
    if major != "NONE":
        majorUser = MajorUser(name,'major')
        majorInfo.append(Major(major, [majorUser]))
    if minor != "NONE":
        majorUser = MajorUser(name,'minor')
        majorInfo.append(Major(minor, [majorUser]))
    if doubleMajor != "NONE":
        majorUser = MajorUser(name,'doubleMajor')
        majorInfo.append(Major(doubleMajor, [majorUser]))

    majorInfo = to_dict(majorInfo)

    # Extract semesters for use in User class
    semesters = []
    for year, classes in finalClasses.items():
        classObjs = [ClassBasics(c['classID'], c['className']) for c in classes]
        semester = Semester(year, classObjs)
        semesters.append(semester)

    userInfo = to_dict(User(name, semesters, major=major, minor=minor, doubleMajor=doubleMajor, email=email))

    # Extract classes for use in Class class
    # Make new Class for each sem the class was taken
    userClasses = []

    for year, classes in finalClasses.items():
        for c in classes:
            curYear = ClassSemester(year, [name])
            repeatClass = False

            # First check if class is a retake
            for userClass in userClasses:
                # If retake, add new ClassSemester to that Class
                if c['classID'] == userClass.id:
                    repeatClass = True
                    userClass.semesters.append(curYear)

            # If not a repeat, make a new Class
            if repeatClass == False:
                cls = Class(c['classID'],c['className'], [curYear])
                userClasses.append(cls)

    classInfo = to_dict(userClasses)

    return userInfo, classInfo, majorInfo






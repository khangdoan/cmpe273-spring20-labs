from flask import Flask, escape, request, url_for, redirect, Response

"""
# request
{

"""

app = Flask(__name__)
student = {}
classesList = {}

StudentID = 0
ClassID = 0

"""
POST /students

# Request
{
    "name": "Bob Smith"
}

# Response
# HTTP Code: 201
{
    "id" : 1234456,
    "name" : "Bob Smith"
}

"""


@app.route('/', methods=['POST', 'GET'])
def resolve_menu():
    if request.method == "GET":
        return '''
        <input type=submit name="create_student" value="create student">
        <input type=submit name="retrieve_student" value="retrieve student">
        <input type=submit name="create_class" value="Create Class">
        <input type=submit name="retrieve_class" value="retrieve class">
        <input type=submit name="add_student" value="Add student">
        '''


@app.route('/students/<int:Id>/', methods=['GET'])
@app.route('/students/', methods=['POST', 'GET'])
def students(Id=0):
    if request.method == "POST":
        global StudentID
        status_code = Response(status=201)
        student[StudentID + 1] = {"name": request.form['Student'], "id": StudentID + 1}
        StudentID = StudentID + 1
        print(f'Student added! {student[StudentID]}')
        return status_code
    print(f'student id {Id}')
    if request.method == 'GET' and Id is not 0:
        print(f'Student found{student[Id]}')
        return student[Id]
    return '''<form method="POST">
                  Student: <input type="text" name="Student"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


@app.route('/classes/<int:classID>/', methods=['GET'])
@app.route('/classes/<int:classID>/<int:studentID>/', methods=['PATCH'])
@app.route('/classes/', methods=['POST', 'GET'])
def classes(classID=0, studentID=0):
    if request.method == "POST":
        global ClassID
        status_code = Response(status=201)
        classesList[ClassID + 1] = {"name": request.form['Class'], "id": ClassID + 1, "Student": []}
        ClassID = ClassID + 1
        return status_code
    elif request.method == "GET" and classID is not 0:
        return classesList[classID]
    elif request.method == "PATCH" and studentID is not 0:
        classesList[classID]['Student'].append(student[studentID])
    return '''<form method="POST">
                  Class: <input type="text" name="Class"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''
# if __name__ == '__main__':
#     app.run()

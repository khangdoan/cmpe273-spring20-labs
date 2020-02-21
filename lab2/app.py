from flask import Flask, escape, request
"""
# request
{

"""


app = Flask(__name__)
student=[]
classes=[]


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

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

@app.route('/students',methods=['POST','GET'])
def student():

    if request.method=="POST":
        student.append({"name":request.form['Student'],"id":len(student)})

    elif request.method == "GET":
        return student[request.form['id']]
    return '''<form method="POST">
                  Student: <input type="text" name="Student"><br>
                  ID: <input type="text" name="ID"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/classes',method=['POST','GET'])
def classes():
    if request.method=="POST":
        classes.append({"name":request.form['name'],"id":len(classes),"student":[]})
    elif request.method=="GET":
        return 
    

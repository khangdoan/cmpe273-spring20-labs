from ariadne import QueryType, graphql_sync, make_executable_schema, MutationType, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify, Response

# from schema import schema

students = {}
classes = {}
studentID = 200
classID = 300
query = QueryType()
mut = MutationType()
student = ObjectType("Student")
classs = ObjectType("Class")
type_defs = """
    type Query {
        hello: String!
        students(id:Int!): Student!
        classes(id: Int!): Class!
    }
    type Mutation {
        createStudent(name: String!): Student!
        createClass(name: String!): Class!
        addStudent(studentID: Int!, classID: Int!): Class! 
    }
    type Student {
        id: Int!
        name: String!
    }
    type Class {
        id: Int!
        name: String!
        students: [Student]!
    }
"""

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {name}!'


"""
# Request
mutation {
	createStudent(name: "Khang") {
    name
    id
  }
}
#Response
{
  "data": {
    "createStudent": {
      "id": 201,
      "name": "Khang"
    }
  }
}
"""

@mut.field("createStudent")
def createStudent(_, info, name):
    global studentID
    students[studentID+1] = {"id": studentID + 1, "name": name}
    # print(f'student: {studentID}')
    studentID = studentID + 1
    # print(f'Adding student: {name}')
    return {"id": studentID, "name": name}


"""
# Request
query  {
  students(id:201) {
    name
  }
}
#Response
{
  "data": {
    "students": {
      "name": "Khang"
    }
  }
}
"""
@query.field('students')
def getStudents(_, info, id):
    return students[id]

"""
# Request
mutation{
  createClass(name: "Name1") {
    id
    name
    students{
      name
      id
    }
  }
}
#Response
{
  "data": {
    "createClass": {
      "id": 301,
      "name": "Name1",
      "students": []
    }
  }
}
"""

@mut.field("createClass")
def createClass(_, info, name):
    global classID
    classes[classID +1] = {
        "id": classID+1,
        "name": name,
        "students": []
    }
    classID = classID+1
    return classes[classID]

"""
# Request
 mutation  {
    addStudent(studentID: 201, classID: 301) {
      id
      name
      students{
        name
        id
      }
    }
  }
#Response
{
  "data": {
    "addStudent": {
      "id": 301,
      "name": "Name1",
      "students": [
        {
          "id": 201,
          "name": "Khang"
        }
      ]
    }
  }
}
"""

@mut.field("addStudent")
def addStudent(_, info, studentID, classID):
    if classID not in classes or studentID not in students:
        return Response(status=400)
    classes[classID]["students"].append(students[studentID])
    return classes[classID]
"""
# Request
  query  {
    classes(id:100000) {
      name
      id
      students{
        name
        id
      }
    }
  }
#Response
{
  "data": {
    "classes": {
      "id": 100000,
      "name": "test1",
      "students": []
    }
  }
}
"""
@query.field("classes")
def getClass(_, info, classID):
    return classes[classID]


schema = make_executable_schema(type_defs, [query, mut])


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

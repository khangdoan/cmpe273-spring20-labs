from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from schema import schema

students = []
query = QueryType()
mut = MutationType()
student = ObjectType("Student")

app = Flask(__name__)
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {name}!'

@mut.field("createStudent")
def createStudent(name):
    students.append(name)
    return {"id" : len(students), "name" : name}

@mut.field('getStudent')
def getstudent(ID):
    return {'name': students[ID]}

@mut.field("createClass")
def resolve_createClass(name):
    pass

@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
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
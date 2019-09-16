from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_restful import fields, marshal_with
import werkzeug.datastructures
import random
# from werkzeug import datastructures


parser = reqparse.RequestParser(bundle_errors=True)  # bundle_errors=True will return all errors, not the first parse error(default)
# args = parser.parse_args(strict=True)


parser.add_argument(
    'rate',
    type=int,
    help='Rate to charge for this resource',
    action='append',
    dest='public_name')

parser.add_argument(
    'foooo',
    choices=('one', 'two'),
    help='Bad choice: {error_msg}')
# If a request comes in with a value of "three" for `foo`:
# {
#     "message":  {
#         "foo": "Bad choice: three is not a valid choice",
#     }
# }


# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From file uploads
parser.add_argument(
    'picture',
    type=werkzeug.datastructures.FileStorage,
    location='files')

parser.add_argument('text', location=['headers', 'values'])





parser.add_argument('foo', type=int)

parser_copy = parser.copy()

# parser_copy has both 'foo' and 'bar'
parser_copy.add_argument('bar', type=int)

# 'foo' is now a required str located in json, not an int as defined by original parser
parser_copy.replace_argument('foo', type=str, required=True, location='json')

parser_copy.remove_argument('foo')  # parser_copy no longer has 'foo' argument


resource_fields = {
    'name': fields.String(attribute='private_name', default='Anonymous User'),
    'address': fields.String(attribute=lambda x: x._private_address),
    'date_updated': fields.DateTime(dt_format='rfc822'),
}


resource_fields = {
    'task': fields.String,
    'uri': fields.Url('toodoo')
}

app = Flask(__name__)
# app.config['BUNDLE_ERRORS'] = True
api = Api(app)

todos = {}


class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}, 201, {'Etag': 'some-opaque-string'}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}, 201, {'Etag': 'some-opaque-string'}


class RandomNumber(fields.Raw):
    def output(self, key, obj):
        return random.random()

fields = {
    'uri': fields.Url('todo_resource', absolute=True),
    'https_uri': fields.Url('todo_resource', absolute=True, scheme='https')
}



api.add_resource(
    TodoSimple,
    '/<string:todo_id>',
    '/todo/<string:todo_id>',
    endpoint='toodoo')

if __name__ == '__main__':
    # print(app.view_functions)
    # print(app.url_map)
    app.run(host='0.0.0.0',port=5008, debug=True)

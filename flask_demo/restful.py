from flask import Flask, abort, jsonify, url_for
from flask_restful import Api, Resource, fields, marshal
from flask_restful import reqparse
from flask_httpauth import HTTPBasicAuth


# auth = HTTPBasicAuth()


app = Flask(__name__)
api = Api(app)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

# def make_public_task(task):
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for(
#                 'get_task', task_id=task['id'], _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task


class TaskListAPI(Resource):
    # decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            type=str,
            required=True,
            help='No task title provided',
            location='json')
        self.reqparse.add_argument(
            'description',
            type=str,
            default="",
            location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        task_list = []
        for task in tasks:
            task = marshal(task, task_fields)
            task_list.append(task)
        return {'tasks': task_list}, 201

    def post(self):
        pass


class TaskAPI(Resource):
    # decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        task = list(filter(lambda t: t['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        # for k, v in args:
        #     if v is not None:
        #         task[k] = v
        # return jsonify({'task': make_public_task(task)})
        # return {'task': make_public_task(task)}, 201
        return {'task': marshal(task, task_fields)}, 201

    def delete(self, id):
        pass

class LoginPage(Resource):
    def __init__(self):
        super(LoginPage, self).__init__()

    def get(self):
        return ("login.html", 201)

api.add_resource(TaskListAPI, '/todo/api/v2.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v2.0/tasks/<int:id>', endpoint='task')
api.add_resource(LoginPage, '/todo/api/v2.0/login', endpoint='login')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5009, debug=True)
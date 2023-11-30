#!/usr/bin/python3
"""return json"""
from api.app import app
from flask import jsonify, abort, request
from data.task import Task
from data import storage


@app.route('/tasks/<user_id>')
def get_tasks(user_id):
    tasks = storage.all(Task, user_id)
    res = []
    for i in tasks:
        res.append(i.to_dict())
    return jsonify(res)

@app.route('/priority/<user_id>')
def priority(user_id):
    tasks = storage.priority(user_id)
    res = []
    for i in tasks:
        res.append(i.to_dict())
    return jsonify(res)

@app.route('/deadline/<user_id>')
def deadline(user_id):
    tasks = storage.deadline(user_id)
    res = []
    for i in tasks:
        res.append(i.to_dict())
    return jsonify(res)

@app.route('/tasks/<task_id>/<user_id>',  methods=['PUT'])
def put_tasks(task_id, user_id):
    tasks = list(storage.all(Task, user_id))
    res = None
    for i in tasks:
        if i.id == task_id:
            res = i
    if res is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    state = request.get_json()
    for key, value in state.items():
        if key == "id" or key == "created_at":
            continue
        if key == "updated_at":
            continue
        setattr(res, key, value)
    storage.save()
    return jsonify(res.to_dict()), 200



@app.route('/tasks/<task_id>/<user_id>', methods=['DELETE'])
def del_task(task_id, user_id):
    tasks = list(storage.all(Task, user_id))
    res = None
    for i in tasks:
        if i.id == task_id:
            res = i
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app.route('/tasks', strict_slashes=False, methods=['POST'])
def post_task():
    if not request.json:
        abort(400, "Not a JSON")
    task = request.get_json()
    if "name" not in task:
        abort(400, "Missing name")
    res = Task(task)
    storage.new(res)
    storage.save()

    return jsonify(res.to_dict), 201


from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local imports
from instance.config import app_config

#initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
  from app.models import TodoList, TodoItem
  app = FlaskAPI(__name__, instance_relative_config=True)
  app.config.from_object(app_config[config_name])
  app.config.from_pyfile('config.py')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)

  @app.route('/api/todolists/', methods=['POST', 'GET'])
  def todolist():
    if request.method == 'POST':
      name = str(request.data.get('name', ' '))
      if name:
        todolist = TodoList(name=name)
        todolist.save()
        response = jsonify({
          'id': todolist.id,
          'name': todolist.name,
          'date_created': todolist.date_created,
          'date_modified': todolist.date_modified
        })
        response.status_code = 201
        return response
    else:
      #GET
      todolists = TodoList.get_all()
      results = []

      for todolist in todolists:
        obj = {
          'id': todolist.id,
          'name': todolist.name,
          'date_created': todolist.date_created,
          'date_modified': todolist.date_modified
        }
        results.append(obj)
        print(results, 'todos')
        response = jsonify(results)
        response.status_code = 200
      return response

  @app.route('/api/todolists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
  def todolist_manipulation(id, **kwargs):
    todolist = TodoList.query.filter_by(id=id).first()
    if not todolist:
      abort(404)

    if request.method == 'GET':
      response = jsonify({
        'id': todolist.id,
        'name': todolist.name,
        'date_created': todolist.date_created,
        'date_modified': todolist.date_modified
      })
      response.status_code = 200
      return response

    elif request.method == 'DELETE':
      todolist.delete()
      return {
        "message": "todolist {} deleted successfully" .format(todolist.id)
      }, 200

    elif request.method == 'PUT':
      name = str(request.data.get('name', ' '))
      todolist.name = name
      todolist.save()
      response = jsonify({
        'id': todolist.id,
        'name': todolist.name,
        'date_created': todolist.date_created,
        'date_modified': todolist.date_modified
      })
      response.status_code = 200
      return response

  @app.route('/api/todoitems/', methods=['POST', 'GET'])
  def todoitem():
    if request.method == 'POST':
      items = str(request.data.get('items', ' '))
      todolist_id =str(request.data.get('todolist_id', ' '))

      if items:
        todoitem = TodoItem(items=items, todolist_id=todolist_id)
        todoitem.save()
        response = jsonify({
          'id': todoitem.id,
          'items': todoitem.items,
          'todolist_id': todoitem.todolist_id,
          'date_created': todoitem.date_created,
          'date_modified': todoitem.date_modified
        })
        response.status_code = 201
        return response

    else:
      todoitems = TodoItem.get_all()
      todos = []
      for todoitem in todoitems:
        new_obj = {
          'id': todoitem.id,
          'item': todoitem.items,
          'todolist_id': todoitem.todolist_id,
          'date_created': todoitem.date_created,
          'date_modified': todoitem.date_modified
        }
        todos.append(new_obj)
        response = jsonify(todos)
        response.status_code = 200

      return response

  @app.route('/api/todoitems/<int:id>', methods=['GET', 'PUT', 'DELETE'])
  def todoitems_manipulation(id, **kwargs):
    todoitem = TodoItem.query.filter_by(id=id).first()
    if not todoitem:
      abort(404)

    if request.method == 'GET':
      response = jsonify({
        'id': todoitem.id,
        'items': todoitem.items,
        'todolist_id': todoitem.todolist_id,
        'date_created': todoitem.date_created,
        'date_modified': todoitem.date_modified
      })
      response.status_code = 200
      return response

    elif request.method == 'DELETE':
      todolist.delete()
      return {
        "message": "todoitem {} deleted successfully" .format(todoitem.id)
      }, 200

    elif request.method == 'PUT':
      name = str(request.data.get('name', ' '))
      todolist.name = name
      todolist.save()
      response = jsonify({
        'id': todoitem.id,
        'items': todoitem.items,
        'todolist_id': todoitem.todolist_id,
        'date_created': todoitem.date_created,
        'date_modified': todoitem.date_modified
      })
      response.status_code = 200
      return response

  @app.route('/api/todolists/<int:id>/todoitems', methods=['GET'])
  def todolist_items_manipulation(id, **kwargs):
    todolist = TodoList.query.filter_by(id=id).first()
    if not todolist:
      abort(404)

    if request.method == 'GET':
      todolist_items = TodoItem.query.filter_by(todolist_id=todolist.id)
      todoitems = []

      for todolist_item in todolist_items:
        new_obj = {
        'id': todolist_item.id,
        'item': todolist_item.items,
        'todolist_id': todolist_item.todolist_id,
        'date_created': todolist_item.date_created,
        'date_modified': todolist_item.date_modified
        }
        todoitems.append(new_obj)
        response = jsonify(todoitems)
        response.status_code = 200
      return response

  return app


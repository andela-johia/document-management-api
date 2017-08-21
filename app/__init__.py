from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local imports
from instance.config import app_config

#initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
  from app.models import TodoList
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

  return app


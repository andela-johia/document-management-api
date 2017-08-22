from app import db

class TodoList(db.Model):
    """This class represents the TodoList table."""

    __tablename__ = 'todolists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    todoitems = db.relationship('TodoItem', backref='todolist', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
      """intitialize with name"""
      self.name =  name

    def save(self):
      db.session.add(self)
      db.session.commit()

    @staticmethod
    def get_all():
      return TodoList.query.all()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def __repr__(self):
      return "<TodoList: {}>".format(self.name)


class TodoItem(db.Model):
  """This class represents the Todoitems table."""

  __tablename__ = 'todoitems'

  id = db.Column(db.Integer, primary_key=True)
  items = db.Column(db.Text())
  todolist_id = db.Column(db.Integer, db.ForeignKey('todolists.id'))
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

  def __init__(self, items, todolist_id):
    """initialize with name"""
    self.items = items
    self.todolist_id = todolist_id

  def save(self):
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def get_all():
    return TodoItem.query.all()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def __repr__(self):
    return "<TodoItem: {}>".format(self.name)


from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cywang@localhost:5432/todoapp'
db=SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__='todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean,  nullable = False, default = False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.description
  })

@app.route('/todos/<todo_id>/set-completed', methods = ['POST']) #grab todo_id from itself so it can show

def set_completed_todo(todo_id): # how does it retreive todo_id
    completed = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all()) # render_template allows you to pass in data to html file
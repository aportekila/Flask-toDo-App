from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/abdul/Desktop/Flask ToDo App/todo.db'

db = SQLAlchemy(app)
@app.route('/')
def index():
    todos = ToDo.query.all()

    return render_template('index.html', todos = todos)
@app.route('/add', methods = ['POST'])
def add():
    title = request.form.get("title")
    content = request.form.get("content")
    newToDo = ToDo(title = title, content = content, coplete = False)
    db.session.add(newToDo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/complete/<string:id>')
def complete(id):
    todo=ToDo.query.filter_by(id=id).first_or_404()
    todo
    if(todo.coplete==False):
        todo.coplete=True
    else:
        todo.coplete=False
    db.session.commit()
    return redirect(url_for("index"))
@app.route('/delete/<string:id>')
def delete(id):
    todo=ToDo.query.filter_by(id=id).first_or_404()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

def page_not_found(e):
    return render_template('404.html'), 404
app.register_error_handler(404, page_not_found)

class ToDo(db.Model):
    id  = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    coplete = db.Column(db.Boolean)

if __name__ == "__main__":
    app.run(debug=True)
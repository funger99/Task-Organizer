from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
# telling our app where out database is located

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initializing database
# binding the instance to a specific flask app
db = SQLAlchemy(app)

# db contains all the functions and helpers from sqlalchemy and sqlalchemy.orm
# db also provides a class called model


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime)
    color = db.Column(db.String(7), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def hello2():
    # request.method returns the method used in the current request
    if request.method == 'POST':
        my_content = request.form['content']
        my_subject = request.form['subject']
        my_dd = datetime.date(int(request.form['year_dd']), int(request.form['month_dd']), int(request.form['day_dd']))
        my_color = '#000000'
        item = Todo(subject=my_subject, content=my_content, due_date=my_dd, color=my_color)

        db.session.add(item)
        db.session.commit()
        return redirect('/')

    else:
        tasks = Todo.query.order_by(Todo.due_date).all()
        return render_template('index.html', tasks=tasks)


@app.route('/<int:item_to_delete>')
def delete(item_to_delete):
    delete_item = Todo.query.get(item_to_delete)
    db.session.delete(delete_item)
    db.session.commit()
    return redirect('/')


@app.route('/done/<int:checkoff>')
def done(checkoff):
    item_to_checkoff = Todo.query.get(checkoff)
    item_to_checkoff.color = "#D3D3D3"
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:item_to_update>', methods=['GET', 'POST'])
def update(item_to_update):
    if request.method == 'POST':
        ud_content = request.form['content']
        ud_subject = request.form['subject']
        ud_dd = datetime.date(int(request.form['year_dd']), int(request.form['month_dd']), int(request.form['day_dd']))
        update_task = Todo.query.get(item_to_update)
        update_task.content = ud_content
        update_task.subject = ud_subject
        update_task.due_date = ud_dd
        db.session.commit()
        return redirect('/')
    else:
        change = Todo.query.get(item_to_update)
        return render_template('index2.html', change=change)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])

def index():
    if(request.method == 'POST'):
        task_content = request.form['content']
        task = Todo(content=task_content)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "did not add."
    else:
        task = Todo.query.all()
        return render_template('index.html',tasks = task)

@app.route('/delete/<int:id>')

def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "can not delete"



@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task =Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "errror while updating"

    else:
        return render_template('update.html',task = task)

if __name__ == "__main__":
    app.run(debug=True)
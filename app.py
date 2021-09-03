from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import current_user, login_user, logout_user, login_required
from models.db_worker import UserHandler, TaskHandler
from datetime import datetime
from forms import LoginForm

task_tracker = Flask(__name__)
task_tracker.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/tasktracker.db'
task_tracker.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(task_tracker)
task_tracker.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

login = LoginManager(task_tracker)
login.login_view = 'login'


@login.user_loader
def load_user(user):
    user_obj = UserHandler()
    user_obj.get_by_id(user)
    return user_obj


@task_tracker.route('/')
@task_tracker.route('/index')
def index():
    return render_template("index.html")


@task_tracker.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_tasks():
    if request.method == 'POST':
        description = request.form.get('description')
        values_task = {
            'description': description
        }
        values_lifecycle = {
            'user': current_user.id,
            'status': 'Новая'
        }
        task = TaskHandler().create(values_task, values_lifecycle)
        return redirect(url_for('task', task_id=task))
    return render_template("create_task.html")


@task_tracker.route('/tasks')
@login_required
def tasks():
    statuses = ['Новыя', 'В работе', 'Выполнено', 'Отменено']
    status = request.args.get('status')
    all_tasks = TaskHandler().get_all(status)
    return render_template("tasks.html", tasks=all_tasks, statuses=statuses)


@task_tracker.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    statuses = ['Новыя', 'В работе', 'Выполнено', 'Отменено']
    if request.method == 'POST':
        status = request.args.get('status')
        values_task = {
            'current_status': status,
            'user_id': current_user.id
        }
        values_lifecycle = {'user': current_user.id,
                            'task': task_id,
                            'status': status,
                            'date': datetime.now()
                            }

        TaskHandler().update(task_id, values_task, values_lifecycle)
        return redirect(url_for('tasks'))
    else:
        task_obj = TaskHandler().get(task_id)
        lifecycle = TaskHandler().get_lifecycle(task_id)
        content = {
            'task': task_obj,
            'lifecycle': lifecycle
        }
    return render_template("task.html", data=content, statuses=statuses)


@task_tracker.route('/my_tasks')
@login_required
def my_tasks():
    status = request.args.get('status')
    print(current_user.id)
    tasks = TaskHandler().get_user_task(user_id=current_user.id, task_status=status)
    return render_template("tasks.html", tasks=tasks)


@task_tracker.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserHandler()
        user_obj = user.get(login=form.login.data)
        if user_obj is None or not user.check_password(form.password.data, form.login.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)


@task_tracker.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    task_tracker.run(debug=True)

from flask import Flask, render_template, request, redirect
from loguru import logger

app = Flask(__name__)

logger.add("todo_app.log", rotation="500 KB")


todos = []
task_id = 1

@app.route('/')
def index():
    logger.info("Loaded home page with {} tasks", len(todos))
    return render_template('todo.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    global task_id
    task = request.form['task']
    if task:
        todos.append({'id': task_id, 'task': task, 'done': False})
        logger.success("Added task: [{}] {}", task_id, task)
        task_id += 1
    else:
        logger.warning("Attempted to add empty task")
    return redirect('/')

@app.route('/toggle/<int:id>')
def toggle(id):
    for todo in todos:
        if todo['id'] == id:
            todo['done'] = not todo['done']
            logger.info("Toggled task {} to {}", id, "done" if todo['done'] else "not done")
            break
    else:
        logger.error("Toggle failed: Task ID {} not found", id)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo['id'] != id]
    if len(todos) < initial_length:
        logger.warning("Deleted task with ID {}", id)
    else:
        logger.error("Delete failed: Task ID {} not found", id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['task_content']
    
    if task_content:
        tasks.append(task_content)
        
    return redirect(url_for('index'))

def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    return delete_task(task_id)


@app.route('/delete_last', methods=['POST'])
def delete_last():
    if tasks:
        tasks.pop()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
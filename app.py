from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'data/tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

tasks = load_tasks()

@app.route('/')
def index():
    selected_category = request.args.get('category')
    keyword = request.args.get('keyword', '').lower()

    filtered_tasks = tasks

    if selected_category:
        filtered_tasks = [t for t in filtered_tasks if t.get('category') == selected_category]

    if keyword:
        filtered_tasks = [
            t for t in filtered_tasks if
            keyword in t.get('title', '').lower() or
            keyword in t.get('description', '').lower() or
            keyword in t.get('category', '').lower()
        ]

    categories = sorted(set(t.get('category', '未分類') for t in tasks if t.get('category')))
    
    return render_template(
        'index.html',
        tasks=filtered_tasks,
        categories=categories,
        selected_category=selected_category,
        keyword=request.args.get('keyword', '')
    )

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    if title:
        tasks.append({
            'id': len(tasks) + 1,
            'title': title,
            'description': description,
            'category': category,
            'completed': False
        })
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def toggle_complete(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

from flask import Flask, request, jsonify
from models import Task # Import the Task class from models

app = Flask(__name__) # create application

API_KEY = 'live_oGxvWh0u3mWmMNetq6hSWWWpuxke5PIRehczw2PUWasyi2lKrJV84JbN5XPCu947'

def authenticate(api_key):
    return api_key == API_KEY

tasks = [
    Task(id=1, title='Task 1', description='Description 1', completed=False),
    Task(id=2, title='Task 2', description='Description 2', completed=True),
]

@app.route('/tasks', methods=['POST']) # decorator, api endpoint
def create_task():
    api_key = request.headers.get('Authorization') # api verification logic

    if not authenticate(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    new_task = Task(len(tasks) + 1, data['title'], data['description'], False)
    tasks.append(new_task)
    return jsonify(new_task.__dict__), 201

@app.route('/tasks', methods=['GET']) # path parameter dynamic value
def get_all_tasks(): #passing path parameter
    api_key = request.headers.get('Authorization') # api verification logic

    if not authenticate(api_key):
        return jsonify({'error': 'Unauthorized'}), 401 

    return jsonify({'tasks': [task__dict__ for task in tasks]})
    
@app.route('/tasks/<int:task_id>', methods=["GET"])
def get_task(task_id):
    api_key = request.headers.get('Authorization') # api verification logic

    if not authenticate(api_key):
        return jsonify({'error': 'Unauthorized'}), 401
    ''' 
    next() function gets first item from the generator expression, 
    which generates tasks 1 by 1 based on the condition 'task.id == task_id'
    '''
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        return jsonify(task.__dict__)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    api_key = request.headers.get('Authorization') # api verification logic

    if not authenticate(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    found_task = None
    for task in tasks:
        if task.id == task_id:
            found_task = task
            break

        if found_task:
            data = request.get_json()
            found_task.title = data['title']
            found_task.description = data['description']
            found_task.completed = data['completed']
            return jsonify(found_task.__dict__)
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    api_key = request.headers.get('Authorization') # api verification logic

    if not authenticate(api_key):
        return jsonify({'error': 'Unauthorized'}), 401
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return jsonify({'result': 'Task deleted'})

# run flask server
if __name__ == "__main__":
    app.run(debug=True)



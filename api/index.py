from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    data = {
        'message': 'Hello, Ashgan!'
    }
    return jsonify(data)


@app.route('/about')
def about():
    return 'About'


@app.route('/post', methods=['POST'])
def handle_post():
    data = request.get_json()  # Get the JSON data from the request

    # Process the data or perform any desired operations
    # For example, let's assume the JSON data contains a 'name' field
    name = data.get('name')
    if name:
        return f"Hello, {name}! This is a POST request."
    else:
        return "No name provided in the request."

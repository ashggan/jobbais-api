from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    data = {
        'message': 'Hello, Ashgan!'
    }
    return jsonify(data)


@app.route('/about', methods=['POST'])
def about():
    if request.method == 'POST':
        # Retrieve data from the request
        data = request.get_json()

        # Process the data
        # ...

        # Create a JSON response
        response = {'message': 'Received POST request', 'data': data}

        # Return the JSON response
        return jsonify(response)

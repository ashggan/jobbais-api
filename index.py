from flask import Flask, jsonify, request
# from pydantic import BaseModel
# from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
# from happytransformer import HappyTextToText, TTSettings


# tokenizer = AutoTokenizer.from_pretrained("saurabhg2083/model_bert")
# model = AutoModelForSequenceClassification.from_pretrained(
#     "saurabhg2083/model_bert")
# happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
# args = TTSettings(num_beams=5, min_length=1)


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
    text = data.get('text')
    if text:
        return f"Hello, {text}! This is a POST request."
    else:
        return "No text provided in the request."

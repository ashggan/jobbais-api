from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from happytransformer import HappyTextToText, TTSettings


app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("saurabhg2083/model_bert")
model = AutoModelForSequenceClassification.from_pretrained(
    "saurabhg2083/model_bert")
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)


# Create a Pydantic model for the request body


class Item(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"message": "Ashgan"}


# Define a route that handles POST requests
@app.post("/classify/")
async def check_bais(item: Item):
    # Access the data from the request body
    text = item.text

    # Perform some logic with the data
    # ...

    # Return a response as per your requirements
    return {"message": "text ayalzed successfully", "name": text}

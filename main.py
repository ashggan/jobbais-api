from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


app = FastAPI()

# Create a Pydantic model for the request body

tokenizer = AutoTokenizer.from_pretrained("saurabhg2083/model_bert")
model = AutoModelForSequenceClassification.from_pretrained(
    "saurabhg2083/model_bert")


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

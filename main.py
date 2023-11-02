from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

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
    return {"message": "text ayalzed successfully", "result": text}

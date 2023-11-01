from typing import Optional

from fastapi import FastAPI


app = FastAPI()

name = "Ashgan"


@app.get("/")
async def root():
    return {"message": name}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

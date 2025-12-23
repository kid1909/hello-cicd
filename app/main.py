from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="item_id must be > 0")
    return {"item_id": item_id, "name": f"Item-{item_id}"}

from fastapi import APIRouter

book1 = APIRouter()

@book1.get("/")
def index():
    print("k")
    return {"message": "book"}
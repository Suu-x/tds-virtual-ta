from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from app.qa_engine import answer_question

app = FastAPI()

class Query(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image if present

@app.post("/")
async def get_answer(query: Query):
    result = answer_question(query.question)
    return result

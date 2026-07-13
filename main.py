import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# HTML fayllarni o'qish uchun
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=BASE_DIR)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("app.html", {"request": request, "view": "home"})

@app.get("/test/{section}/{part}")
async def serve_test_app(request: Request, section: str, part: str):
    mock_data = {
        "text": "The history of computers dates back to the 1800s. Charles Babbage is considered to be the father of computing after his invention of the Analytical Engine...",
        "questions": [
            {"id": 1, "q": "When did computer history begin?", "options": ["1700s", "1800s", "1900s"]},
            {"id": 2, "q": "Who is known as the father of computers?", "options": ["Charles Babbage", "Alan Turing", "Steve Jobs"]}
        ]
    }
    return templates.TemplateResponse("app.html", {
        "request": request, 
        "view": "test", 
        "section": section, 
        "part": part, 
        "data": mock_data
    })

# Foydalanuvchidan keladigan javoblar qolipi
class TestSubmit(BaseModel):
    section: str
    part: str
    answers: dict

@app.post("/api/submit_test")
async def submit_test(data: TestSubmit):
    # To'g'ri javoblar bazasi (Buni keyinchalik ma'lumotlar bazasidan olasiz)
    correct_answers = {"1": "1800s", "2": "Charles Babbage"}
    score = 0
    
    for q_id, ans in data.answers.items():
        if correct_answers.get(q_id) == ans:
            score += 1
            
    total = len(correct_answers)
    percentage = int((score / total) * 100)
    
    # Natijani to'g'ridan-to'g'ri saytga (frontend'ga) qaytaramiz
    return {
        "status": "success", 
        "score": score, 
        "total": total, 
        "percentage": percentage
    }

import os
import logging
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.INFO)

# Vercel Environment Variables dan tokenni olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Vercel sozlamalariga kiriting.")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
app = FastAPI()

# Barcha HTML fayllarni to'g'ridan-to'g'ri asosiy joydan o'qiydi (templates papkasi kerak emas)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=BASE_DIR)

@app.get("/test/{section}/{part}")
async def serve_test_app(request: Request, section: str, part: str):
    mock_data = {
        "text": "The history of computers dates back to the 1800s...",
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

@app.get("/admin")
async def serve_admin_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request, "view": "admin"})

class TestSubmit(BaseModel):
    user_id: int
    section: str
    part: str
    answers: dict

@app.post("/api/submit_test")
async def submit_test(data: TestSubmit):
    correct_answers = {"1": "1800s", "2": "Charles Babbage"}
    score = 0
    
    for q_id, ans in data.answers.items():
        if correct_answers.get(q_id) == ans:
            score += 1
            
    total = len(correct_answers)
    result_text = (
        f"📊 <b>Test natijangiz:</b>\n\n"
        f"Bo'lim: {data.section.capitalize()} | Part {data.part}\n"
        f"To'g'ri javoblar: {score} / {total}\n"
    )
    
    try:
        await bot.send_message(chat_id=data.user_id, text=result_text)
    except Exception as e:
        print(f"Xabar yuborishda xatolik: {e}")
        
    return {"status": "success", "score": score}

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from openai import OpenAI
from retrieval import load_bm25_corpus, search_word
from dotenv import load_dotenv
from pathlib import Path
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

import openai 
load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

    
#Create OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def build_rag_answer(query: str, k:int=3):
    retrieved = search_word(query, k=k)

    if not retrieved:
        context_text = "No dictionary entries were retrieved."
    else:
        chunks = []
        for r in retrieved:
            chunks.append(
                f"Word: {r['word']}\nSource: {r['source']}\nText: {r['definition']}\n"
            )
        context_text = "\n---\n".join(chunks)

    prompt = f"""
You are helping a learner understand Greek vocabulary.

User query: {query}

Below are dictionary entries and context texts (definitions, example sentences, short encyclopedia paragraphs). Use only this information plus general Greek knowledge, and stay brief.

Context:
{context_text}

Task:
- Explain what the query word/phrase means.
- If there are multiple senses, list them briefly.
- Optionally give 1–2 short example sentences in Greek.
- Keep the explanation in Greek, but offer to help with English translation next.
"""

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",  # or your chosen cheap model
        messages=[
            {"role": "system", "content": "You are a concise Greek vocabulary teacher."},
            {"role": "user", "content": prompt},
        ],
    )
    answer = completion.choices[0].message.content
    return answer, retrieved

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "chat.html",           # template filename
        {"request": request}   # context (must include request)
    )

@app.post("/chat", response_class=JSONResponse)
async def chat(query: str = Form(...)):
    """Chat endpoint that returns JSON response for the chatbot interface."""
    answer, retrieved = build_rag_answer(query, k=5)
    
    # Return JSON response - you can modify this structure as needed
    return JSONResponse({
        "answer": answer,
        "retrieved": retrieved,
        "query": query
    })

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    answer, retrieved = build_rag_answer(query, k=5)
    
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "query": query,
            "answer": answer,
            "retrieved": retrieved
        }
    )



    


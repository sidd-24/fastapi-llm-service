from fastapi import FastAPI, Header, HTTPException
from app.models import (
    SummarizeRequest,
    SummarizeResponse,
    ClassifyRequest,
    ClassifyResponse,
)
from app.services import summarize_text, classify_text


app = FastAPI(
    title="LLM Microservice",
    description="A REST API for text summarization and classification powered by Groq.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"status": "ok", "message": "LLM Microservice is running."}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest, x_api_key: str = Header(...)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key is required.")
    result = summarize_text(request.text, request.max_words, x_api_key)
    return result


@app.post("/classify", response_model=ClassifyResponse)
def classify(request: ClassifyRequest, x_api_key: str = Header(...)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key is required.")
    result = classify_text(request.text, request.labels, x_api_key)
    return result
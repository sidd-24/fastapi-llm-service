![CI](https://github.com/sidd-24/fastapi-llm-service/actions/workflows/ci.yml/badge.svg)

# ⚡ FastAPI LLM Microservice

A production-ready REST API that wraps Groq LLM for text summarization and classification. Built to show how AI can be integrated into real systems as a callable service rather than a standalone app.

## Stack

| Layer | Tool |
|---|---|
| API Framework | FastAPI |
| LLM | Groq (Llama 3.3 70B) |
| Orchestration | LangChain |
| Validation | Pydantic v2 |
| Testing | pytest + httpx |
| Server | Uvicorn |

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/summarize` | Summarize any text |
| POST | `/classify` | Classify text into custom labels |

## Project Structure

```
fastapi-llm-service/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app and route definitions
│   ├── models.py      # Pydantic request/response models
│   └── services.py    # LLM logic with LangChain + Groq
├── tests/
│   ├── __init__.py
│   └── test_endpoints.py   # pytest test suite
├── requirements.txt
└── .env.example
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/sidd-24/fastapi-llm-service
cd fastapi-llm-service
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Get a free Groq API key**

Sign up at [console.groq.com](https://console.groq.com) and create an API key.

**5. Run the server**
```bash
uvicorn app.main:app --reload
```

API will be live at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## Usage

### Summarize text

```bash
curl -X POST http://localhost:8000/summarize \
  -H "x-api-key: your_groq_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "max_words": 50
  }'
```

**Response:**
```json
{
  "summary": "A concise summary of the text.",
  "word_count": 9
}
```

### Classify text

```bash
curl -X POST http://localhost:8000/classify \
  -H "x-api-key: your_groq_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The product broke after one day of use.",
    "labels": ["positive", "negative", "neutral"]
  }'
```

**Response:**
```json
{
  "label": "negative",
  "reason": "The text describes a product defect which indicates a negative experience."
}
```

## Running Tests

```bash
pytest tests/ -v
```

All tests use mocking so no real API key is needed to run them.

## How it works

```
Client → POST /summarize → FastAPI → LangChain PromptTemplate → Groq LLM → Response
Client → POST /classify  → FastAPI → LangChain PromptTemplate → Groq LLM → Response
```

The API key is passed per request via the `x-api-key` header so the service is stateless and each caller can use their own key.

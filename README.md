# Northstar Culinary Technologies — Knowledge Agent

A FastAPI-based AI agent that answers questions about Northstar Culinary Technologies
using a curated knowledge base. Questions outside the domain are gracefully declined.

## Quick start (local)

### Prerequisites
- Python 3.12
- An Gemini API key

### 1. Clone and install

```bash
git clone https://github.com/FKjaeren/pfa_case_frederik.git
cd pfa_case_frederik
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment
Edit .env and set GEMINI_API_KEY=your-key
 
### 3. Run
 
```bash
uvicorn app.main:app --reload
```
 
The API is now live at **http://localhost:8000**.
Interactive Swagger docs: **http://localhost:8000/docs**
 
---
 
## Quick start (Docker)
 
```bash
docker build -t pfa_case_frederik .
docker run -p 8000:8000 -e GEMINI_API_KEY=your-key pfa_case_frederik
```
 
---
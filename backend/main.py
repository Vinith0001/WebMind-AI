from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .rag import RAGProcessor
import os
from dotenv import load_dotenv

from typing import Optional

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG processor
try:
    rag_processor = RAGProcessor()
    print("Enhanced RAG processor initialized successfully")
except Exception as e:
    print(f"Error initializing RAG processor: {e}")
    rag_processor = None

@app.get("/")
def read_root():
    return {
        "message": "WebMind AI API", 
        "endpoints": ["/chat", "/languages"],
        "features": ["Multi-language", "Text processing"]
    }

@app.get("/languages")
def get_supported_languages():
    """Get list of supported languages"""
    if not rag_processor:
        raise HTTPException(status_code=500, detail="RAG processor not initialized")
    return {"languages": rag_processor.supported_languages}

class EnhancedRAGRequest(BaseModel):
    text: str
    query: str
    target_language: Optional[str] = 'en'

@app.post("/chat")
def get_answer(payload: EnhancedRAGRequest):
    try:
        if not rag_processor:
            raise HTTPException(status_code=500, detail="RAG processor not initialized")
        
        if not payload.text or not payload.query:
            raise HTTPException(status_code=400, detail="Both text and query are required")

        result = rag_processor.process_query(
            text=payload.text,
            query=payload.query,
            target_lang=payload.target_language
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
# main.py
from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main  import get_datasets_response  # adapte selon ton arborescence

# 1) Création de l'app
app = FastAPI(title="API OpenData Bénin")

# 2) Configuration CORS
origins = [
    "http://127.0.0.1:5500",  # ton front local
    "https://chat-by-ghi.onrender.com",  # si tu as un front hébergé
    # "*"  # décommente si tu veux autoriser toutes les origines
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # tu peux aussi mettre ["*"]
    allow_headers=["*"],  # autorise tous les en-têtes (Accept, Content-Type…)
)

# 3) Modèles Pydantic
class Dataset(BaseModel):
    title: str
    description: str
    url: str

class SearchResponse(BaseModel):
    status: Literal["ok", "hors_sujet"]
    keywords: Optional[List[str]] = None
    datasets: Optional[List[Dataset]] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str

# 4) Route POST /search
@app.post(
    "/search",
    response_model=SearchResponse,
    responses={400: {"model": ErrorResponse}}
)
async def search_endpoint(
    query: str = Query(..., description="Terme de recherche")
):
    """
    Recherche de datasets à partir d'une query utilisateur.
    """
    resp = get_datasets_response(query)

    if resp["status"] == "error":
        # devient HTTP 400
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": resp["message"]}
        )

    # status ok ou hors_sujet → HTTP 200
    return resp

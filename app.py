# api.py

from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import get_datasets_response

app = FastAPI(title="API OpenData Bénin")

class Dataset(BaseModel):
    title: str
    description: str
    url: str

class SearchResponse(BaseModel):
    status: Literal["ok", "hors_sujet"]
    keywords: Optional[List[str]] = None
    datasets: Optional[List[Dataset]] = None
    message: Optional[str] = None  # contient le recadrage si hors_sujet

class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str

@app.post(
    "/search",
    response_model=SearchResponse,
    responses={400: {"model": ErrorResponse}}
)
async def search_endpoint(query: str):
    """
    Recherche de datasets à partir d'une query utilisateur.
    - status == "ok"       => on a des mots-clés et des datasets
    - status == "hors_sujet" => le LLM a recadré, on renvoie son message (HTTP 200)
    - status == "error"     => problème technique (on renvoie HTTP 400)
    """
    resp = get_datasets_response(query)

    if resp["status"] == "error":
        # Seul le statut "error" devient une vraie erreur HTTP 400
        raise HTTPException(status_code=400, detail={"status": "error", "message": resp["message"]})

    # ok ou hors_sujet retournés en HTTP 200 avec le même modèle SearchResponse
    return resp

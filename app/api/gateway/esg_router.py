"""
ESG 라우터
- ESG 엔드포인트

"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

router = APIRouter(
    prefix="/esg",
    tags=["esg"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root() -> Dict[str, Any]:
    """
    ESG 서비스 루트 엔드포인트
    """
    return {"message": "ESG Service"} 
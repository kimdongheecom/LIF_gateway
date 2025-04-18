"""
Finance 라우터
- Finance 엔드포인트

"""

from fastapi import APIRouter, Request
import httpx
import os
from typing import Dict, Any

router = APIRouter(  
    tags=["finance"],
)

FINANCE_SERVICE_URL = os.getenv("FINANCE_SERVICE_URL")

@router.get("/ratios/{company_name}")
async def get_financial_ratios(company_name: str) -> Dict[str, Any]:
    """
    회사명으로 재무비율을 조회합니다.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FINANCE_SERVICE_URL}/ratios/{company_name}")
        return response.json()

@router.get("/financial")
async def get_financial() -> Dict[str, Any]:
    """
    기본 회사의 재무제표를 조회합니다.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FINANCE_SERVICE_URL}/financial")
        return response.json()

@router.post("/financial")
async def get_financial_by_name(company_name: str) -> Dict[str, Any]:
    """
    회사명으로 재무제표를 조회합니다.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FINANCE_SERVICE_URL}/financial",
            json={"company_name": company_name}
        )
        return response.json()

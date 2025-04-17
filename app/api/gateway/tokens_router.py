"""
Tokens 라우터
- Tokens 엔드포인트
- 토큰 관리
- 사용자 인증 처리
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Body
from typing import Dict, Any, Optional

from app.domain.gateway.controllers.token_controller import TokenController
from app.domain.gateway.schemas.token_schema import TokenSchema, TokenResponseSchema, TokenVerifyResponseSchema

router = APIRouter(
    prefix="/tokens",
    tags=["tokens"],
    responses={404: {"description": "Not found"}},
)

controller = TokenController()

@router.post("/")
async def root() -> Dict[str, Any]:
    """
    Tokens 서비스 루트 엔드포인트
    """
    return {"message": "Tokens Service"}

@router.post("/create", response_model=TokenResponseSchema)
async def create_token(user_id: str) -> TokenResponseSchema:
    """
    사용자 ID로 새 토큰 생성
    
    Args:
        user_id: 사용자 ID
        
    Returns:
        생성된 토큰 정보
    """
    return await controller.create_token(user_id)

@router.post("/verify", response_model=TokenVerifyResponseSchema)
async def verify_token(token_data: TokenSchema) -> TokenVerifyResponseSchema:
    """
    토큰 검증
    
    Args:
        token_data: 검증할 토큰 정보
        
    Returns:
        토큰 검증 결과
    """
    return await controller.verify_token(token_data)

@router.post("/revoke")
async def revoke_token(token_data: TokenSchema) -> Dict[str, Any]:
    """
    토큰 폐기
    
    Args:
        token_data: 폐기할 토큰 정보
        
    Returns:
        폐기 결과 메시지
    """
    return await controller.revoke_token(token_data.token)

@router.post("/dummy")
async def test_dummy_token(data: str = Body(..., description="아무 값이나 입력해보세요")):
    """
    테스트용 더미 토큰 생성 (Body 파라미터)
    
    Swagger에서 입력한 문자열을 그대로 토큰으로 사용합니다.
    
    Args:
        data: 입력 값 (필수, Body 파라미터)
        
    Returns:
        메시지와 입력 데이터
    """
    print(f"✅ Swagger에서 받은 값:", data)
    
    # 사용자가 입력한 값을 토큰으로 사용
    return {
        "message": "✅ 콘솔에 출력 완료!",
        "received": data,
        "token_info": {
            "access_token": data,  # 사용자 입력 값을 토큰으로 사용
            "token_type": "bearer",
            "expires_in": 1800
        }
    }
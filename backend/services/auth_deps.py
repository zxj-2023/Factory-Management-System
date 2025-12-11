"""
Supabase JWT 校验与权限依赖（供 FastAPI 路由使用），基于 PyJWT + PyJWKClient 验证 JWKS。
"""

import os
from functools import lru_cache
from typing import Dict, List

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# 加载 .env 变量
load_dotenv()

SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL", "")
SUPABASE_ISS = os.getenv("SUPABASE_ISS", "")
SUPABASE_AUD = os.getenv("SUPABASE_AUD", "authenticated")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")

bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache()
def get_jwks_client():
    if not SUPABASE_JWKS_URL:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWKS URL not configured")
    return jwt.PyJWKClient(SUPABASE_JWKS_URL)


def _verify_token(token: str) -> Dict:
    try:
        unverified_header = jwt.get_unverified_header(token)
        alg = unverified_header.get("alg", "RS256")

        options = {"require_exp": True}
        if not SUPABASE_AUD:
            options["verify_aud"] = False

        # 如果是 HS 系列并配置共享密钥，先尝试 HS 验证
        if alg.upper().startswith("HS") and SUPABASE_JWT_SECRET:
            payload = jwt.decode(
                token,
                SUPABASE_JWT_SECRET,
                algorithms=[alg],
                issuer=SUPABASE_ISS or None,
                audience=SUPABASE_AUD or None,
                options=options,
            )
            return payload

        # 其余（ES/RS 等）通过 JWKS 验证
        signing_key = get_jwks_client().get_signing_key_from_jwt(token).key
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=[alg],
            issuer=SUPABASE_ISS or None,
            audience=SUPABASE_AUD or None,
            options=options,
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    payload = _verify_token(token)
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role") or payload.get("app_metadata", {}).get("role"),
        "raw": payload,
    }


def require_roles(*allowed: str):
    def checker(user=Depends(get_current_user)):
        roles = user.get("role")
        roles_list: List[str] = []
        if isinstance(roles, str):
            roles_list = [roles]
        elif isinstance(roles, list):
            roles_list = roles
        if not set(roles_list) & set(allowed):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
        return user

    return checker

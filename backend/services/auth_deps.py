"""
Supabase JWT 校验与权限依赖（供 FastAPI 路由使用），基于 PyJWT 验证 JWKS。
"""

import json
import os
import time
from typing import Dict, List
from urllib.request import urlopen

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL", "")
SUPABASE_ISS = os.getenv("SUPABASE_ISS", "")
SUPABASE_AUD = os.getenv("SUPABASE_AUD", "authenticated")

_jwks_cache: Dict[str, object] = {}
_jwks_expires_at: float = 0
_jwks_ttl_seconds = 600

bearer_scheme = HTTPBearer(auto_error=False)


def _load_jwks() -> Dict:
    global _jwks_cache, _jwks_expires_at
    now = time.time()
    if _jwks_cache and now < _jwks_expires_at:
        return _jwks_cache
    if not SUPABASE_JWKS_URL:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWKS URL not configured")
    with urlopen(SUPABASE_JWKS_URL) as resp:
        data = json.load(resp)
        _jwks_cache = data
        _jwks_expires_at = now + _jwks_ttl_seconds
        return data


def _verify_token(token: str) -> Dict:
    jwks = _load_jwks()
    unverified = jwt.get_unverified_header(token)
    kid = unverified.get("kid")
    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token kid")
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=[unverified.get("alg", "RS256")],
            audience=SUPABASE_AUD,
            issuer=SUPABASE_ISS or None,
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

"""
Módulo de autenticación (preparado para JWT/Supabase)
Por ahora está inactivo, pero la estructura está lista para activarse
"""
from fastapi import Header, HTTPException, status
from typing import Optional
import os


class AuthService:
    """Servicio de autenticación (preparado para futuro)"""
    
    def __init__(self):
        self.enabled = os.getenv("AUTH_ENABLED", "false").lower() == "true"
        self.jwt_secret = os.getenv("JWT_SECRET", None)
        self.supabase_url = os.getenv("SUPABASE_URL", None)
        self.supabase_key = os.getenv("SUPABASE_KEY", None)
    
    async def verify_token(self, authorization: Optional[str] = Header(None)) -> Optional[dict]:
        """
        Verifica el token JWT (inactivo por ahora)
        
        Cuando se active, validará:
        - Bearer token en header Authorization
        - Firma JWT con JWT_SECRET o Supabase public key
        - Expiración del token
        
        Returns:
            dict: Payload del token decodificado (user_id, email, etc.)
        """
        if not self.enabled:
            # Auth deshabilitado - permitir acceso
            return None
        
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se proporcionó token de autenticación",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # TODO: Implementar validación real cuando se active
        # try:
        #     scheme, token = authorization.split()
        #     if scheme.lower() != "bearer":
        #         raise HTTPException(...)
        #     
        #     # Validar con JWT o Supabase
        #     payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
        #     return payload
        # except Exception as e:
        #     raise HTTPException(...)
        
        return None
    
    def require_auth(self):
        """
        Dependency para rutas que requieren autenticación
        Uso: @router.get("/protected", dependencies=[Depends(auth.require_auth())])
        """
        return self.verify_token


# Instancia global
auth_service = AuthService()










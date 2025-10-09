"""
Utilidades y helpers para el backend
"""
import logging
import sys
from typing import Any
import json


def setup_logging(level: str = "INFO"):
    """
    Configura el sistema de logging
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def log_calculation(expression: str, mode: str, success: bool, error: str = None):
    """
    Log estructurado de cálculos (preparado para métricas futuras)
    """
    logger = logging.getLogger("educalc.calculations")
    log_data = {
        "expression": expression,
        "mode": mode,
        "success": success,
        "error": error
    }
    logger.info(json.dumps(log_data))


def sanitize_expression(expression: str) -> str:
    """
    Sanitiza la expresión antes de procesarla
    Elimina caracteres peligrosos y normaliza
    """
    # Eliminar espacios extra
    expression = expression.strip()
    
    # Lista de caracteres/palabras prohibidas para evitar eval malicioso
    forbidden = [
        "__", "import", "exec", "eval", "compile", "open", "file",
        "input", "raw_input", "execfile", "reload", "globals", "locals"
    ]
    
    expression_lower = expression.lower()
    for forbidden_word in forbidden:
        if forbidden_word in expression_lower:
            raise ValueError(f"Expresión contiene término prohibido: {forbidden_word}")
    
    return expression


def format_latex(expression: str) -> str:
    """
    Convierte una expresión de SymPy a formato LaTeX (preparado para futuro)
    """
    try:
        from sympy import latex, sympify
        expr = sympify(expression)
        return latex(expr)
    except Exception:
        return expression


class RateLimiter:
    """
    Rate limiter simple (preparado para Redis en producción)
    Por ahora es un placeholder
    """
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.enabled = False  # Deshabilitado por ahora
    
    async def check_rate_limit(self, identifier: str) -> bool:
        """
        Verifica si el usuario/IP está dentro del rate limit
        """
        if not self.enabled:
            return True
        
        # TODO: Implementar con Redis
        # INCR identifier
        # EXPIRE identifier window_seconds
        # if count > max_requests: return False
        
        return True


# Instancia global
rate_limiter = RateLimiter()





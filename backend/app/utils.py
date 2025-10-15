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
    
    # Detectar comas (múltiples expresiones)
    if ',' in expression:
        # Sugerir separar las expresiones
        parts = [p.strip() for p in expression.split(',') if p.strip()]
        if len(parts) > 1:
            if len(parts) == 2:
                raise ValueError(
                    f"❌ La coma (,) NO es un operador matemático válido.\n\n"
                    f"📚 Explicación:\n"
                    f"La coma se usa en programación para separar elementos de una lista, pero en matemáticas no es una operación.\n\n"
                    f"✅ Solución: Calcula cada expresión por separado:\n\n"
                    f"   1) {parts[0]}\n"
                    f"   2) {parts[1]}"
                )
            else:
                suggestions = '\n'.join([f"   {i+1}) {part}" for i, part in enumerate(parts)])
                raise ValueError(
                    f"❌ La coma (,) NO es un operador matemático válido.\n\n"
                    f"📚 Explicación:\n"
                    f"La coma se usa en programación para separar elementos, pero en matemáticas no existe como operación.\n\n"
                    f"✅ Solución: Calcula cada expresión por separado:\n\n{suggestions}"
                )
    
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










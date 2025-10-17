"""
Endpoint de validación de expresiones
"""
from fastapi import APIRouter, HTTPException, status
from app.models import ValidationRequest, ValidationResponse
from app.calculator_engine import CalculatorEngine
from app.utils import sanitize_expression
import logging

router = APIRouter()
calculator = CalculatorEngine()
logger = logging.getLogger(__name__)


@router.post("/validate", response_model=ValidationResponse, tags=["validate"])
async def validate_expression(request: ValidationRequest):
    """
    Valida una expresión matemática sin resolverla
    
    - Verifica que la expresión sea parseable
    - Comprueba que no contenga código malicioso
    - Detecta el modo apropiado si no se especifica
    """
    try:
        # Sanitizar expresión
        clean_expression = sanitize_expression(request.expression)
        
        # Detectar modo si es auto
        mode = request.mode
        if mode == "auto":
            mode = calculator._detect_mode(clean_expression)
        
        # Validar con el engine
        is_valid = calculator.validate_expression(clean_expression, mode)
        
        if is_valid:
            return ValidationResponse(
                valid=True,
                expression=clean_expression,
                mode=mode,
                error=None
            )
        else:
            return ValidationResponse(
                valid=False,
                expression=request.expression,
                mode=mode,
                error="La expresión no es válida o no se puede parsear"
            )
    
    except ValueError as e:
        # Error de validación conocido
        logger.warning(f"Validación fallida: {str(e)}")
        return ValidationResponse(
            valid=False,
            expression=request.expression,
            mode=request.mode,
            error=str(e)
        )
    
    except Exception as e:
        # Error inesperado
        logger.error(f"Error en validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno en validación: {str(e)}"
        )











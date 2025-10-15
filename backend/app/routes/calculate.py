"""
Endpoint principal de cálculo
"""
from fastapi import APIRouter, HTTPException, status, Depends
from app.models import CalculationRequest, CalculationResponse
from app.calculator_engine import CalculatorEngine
from app.utils import sanitize_expression, log_calculation
from app.auth import auth_service
import logging

router = APIRouter()
calculator = CalculatorEngine()
logger = logging.getLogger(__name__)


@router.post(
    "/calculate",
    response_model=CalculationResponse,
    tags=["calculate"],
    # dependencies=[Depends(auth_service.require_auth())]  # Descomentrar cuando se active auth
)
async def calculate(request: CalculationRequest):
    """
    Endpoint principal para resolver expresiones matemáticas con explicaciones paso a paso
    
    **Modos soportados:**
    - `auto`: Detecta automáticamente el tipo de operación
    - `arithmetic`: Operaciones aritméticas básicas
    - `algebra`: Simplificación y expansión algebraica
    - `solve`: Resolver ecuaciones
    - `derivative`: Calcular derivadas
    - `integral`: Calcular integrales
    
    **Parámetros:**
    - `expression`: La expresión matemática a resolver
    - `mode`: El modo de cálculo (opcional, por defecto 'auto')
    - `variables`: Diccionario de variables para sustituir (opcional)
    
    **Retorna:**
    - `original`: Expresión original
    - `result`: Resultado final
    - `steps`: Lista de pasos explicativos
    - `mode`: Modo utilizado
    - `error`: Mensaje de error si aplica
    """
    try:
        # Sanitizar expresión
        clean_expression = sanitize_expression(request.expression)
        
        # Calcular con el engine
        result_data = calculator.calculate(
            expression=clean_expression,
            mode=request.mode,
            variables=request.variables
        )
        
        # Log de la operación
        log_calculation(
            expression=clean_expression,
            mode=result_data["mode"],
            success=True
        )
        
        # Construir respuesta
        response = CalculationResponse(
            original=request.expression,
            result=result_data["result"],
            steps=result_data["steps"],
            mode=result_data["mode"],
            error=None
        )
        
        return response
    
    except ValueError as e:
        # Error de validación o cálculo conocido
        logger.warning(f"Error en cálculo: {str(e)}")
        log_calculation(
            expression=request.expression,
            mode=request.mode,
            success=False,
            error=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Error en la expresión o cálculo",
                "message": str(e),
                "expression": request.expression
            }
        )
    
    except Exception as e:
        # Error inesperado
        logger.error(f"Error interno en cálculo: {str(e)}", exc_info=True)
        log_calculation(
            expression=request.expression,
            mode=request.mode,
            success=False,
            error=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Error interno del servidor",
                "message": "Ocurrió un error inesperado al procesar la solicitud"
            }
        )










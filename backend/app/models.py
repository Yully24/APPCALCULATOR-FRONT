from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Step(BaseModel):
    """Modelo para un paso individual de la solución"""
    step: int = Field(..., description="Número del paso")
    description: str = Field(..., description="Descripción breve del paso")
    expression: Optional[str] = Field(None, description="Expresión matemática en este paso")
    detail: Optional[str] = Field(None, description="Explicación detallada del paso")

    class Config:
        json_schema_extra = {
            "example": {
                "step": 1,
                "description": "Expandir la expresión",
                "expression": "2x + 6",
                "detail": "Aplicamos la propiedad distributiva: 2(x+3) = 2*x + 2*3"
            }
        }


class CalculationRequest(BaseModel):
    """Modelo de solicitud para cálculos"""
    expression: str = Field(..., description="Expresión matemática a resolver")
    mode: Optional[str] = Field(
        "auto",
        description="Modo de cálculo: 'auto', 'arithmetic', 'algebra', 'solve', 'derivative', 'integral'"
    )
    variables: Optional[Dict[str, Any]] = Field(
        None,
        description="Variables y sus valores para sustituir"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "expression": "2*(x+3) - 4",
                "mode": "algebra",
                "variables": None
            }
        }


class CalculationResponse(BaseModel):
    """Modelo de respuesta para cálculos"""
    original: str = Field(..., description="Expresión original")
    result: str = Field(..., description="Resultado final")
    steps: List[Step] = Field(..., description="Pasos de la solución")
    mode: str = Field(..., description="Modo de cálculo utilizado")
    error: Optional[str] = Field(None, description="Mensaje de error si aplica")

    class Config:
        json_schema_extra = {
            "example": {
                "original": "2*(x+3) - 4",
                "result": "2*x + 2",
                "steps": [
                    {
                        "step": 1,
                        "description": "Expandir expresión",
                        "expression": "2*x + 6 - 4",
                        "detail": "Aplicar propiedad distributiva"
                    },
                    {
                        "step": 2,
                        "description": "Combinar términos semejantes",
                        "expression": "2*x + 2",
                        "detail": "Sumar 6 - 4 = 2"
                    }
                ],
                "mode": "algebra",
                "error": None
            }
        }


class ValidationRequest(BaseModel):
    """Modelo para validar expresiones"""
    expression: str = Field(..., description="Expresión a validar")
    mode: Optional[str] = Field("auto", description="Modo esperado")


class ValidationResponse(BaseModel):
    """Respuesta de validación"""
    valid: bool = Field(..., description="Si la expresión es válida")
    expression: str = Field(..., description="Expresión validada")
    mode: str = Field(..., description="Modo detectado/validado")
    error: Optional[str] = Field(None, description="Mensaje de error si no es válida")


class OperationInfo(BaseModel):
    """Información de una operación soportada"""
    type: str
    name: str
    description: str
    examples: List[str]


class HealthResponse(BaseModel):
    """Respuesta del health check"""
    status: str
    version: str
    environment: str






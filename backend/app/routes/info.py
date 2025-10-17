"""
Endpoints de información: health, operations
"""
from fastapi import APIRouter
from app.models import HealthResponse, OperationInfo
from typing import List
import os

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["info"])
async def health_check():
    """
    Health check endpoint - verifica que el servicio esté funcionando
    """
    return HealthResponse(
        status="ok",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )


@router.get("/operations", response_model=List[OperationInfo], tags=["info"])
async def get_operations():
    """
    Lista todas las operaciones matemáticas soportadas
    """
    operations = [
        OperationInfo(
            type="arithmetic",
            name="Aritmética Básica",
            description="Operaciones numéricas: suma, resta, multiplicación, división, potencias",
            examples=["2 + 3 * 4", "(10 - 5) / 2", "2**8"]
        ),
        OperationInfo(
            type="algebra",
            name="Álgebra",
            description="Simplificación y expansión de expresiones algebraicas",
            examples=["2*(x + 3) - 4", "(x + 2)**2", "x**2 - 4"]
        ),
        OperationInfo(
            type="solve",
            name="Resolver Ecuaciones",
            description="Resolución de ecuaciones lineales y cuadráticas",
            examples=["2*x + 5 = 15", "x**2 - 4 = 0", "3*x - 7 = 2*x + 3"]
        ),
        OperationInfo(
            type="derivative",
            name="Derivadas",
            description="Cálculo de derivadas de funciones",
            examples=["x**2 + 3*x", "sin(x)", "x**3 - 2*x + 1"]
        ),
        OperationInfo(
            type="integral",
            name="Integrales",
            description="Cálculo de integrales indefinidas",
            examples=["x**2", "2*x + 1", "sin(x)"]
        )
    ]
    
    return operations


@router.get("/", tags=["info"])
async def root():
    """
    Endpoint raíz - información básica de la API
    """
    return {
        "app": "EduCalc Backend API",
        "version": "1.0.0",
        "description": "Backend para calculadora educativa con explicaciones paso a paso",
        "docs": "/docs",
        "health": "/health",
        "operations": "/operations"
    }











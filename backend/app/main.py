"""
EduCalc Backend - FastAPI Application
Calculadora educativa con explicaciones paso a paso
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routes import calculate, validate, info
from app.utils import setup_logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))

# Crear aplicación FastAPI
app = FastAPI(
    title="EduCalc Backend API",
    description="Backend para calculadora educativa con explicaciones paso a paso. "
                "Soporta aritmética, álgebra, ecuaciones, derivadas e integrales.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8081")

# Si es "*" permitir todos los orígenes (solo para fase de feedback)
if cors_origins_env == "*":
    origins = ["*"]
else:
    origins = cors_origins_env.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True if origins != ["*"] else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(info.router, prefix="", tags=["info"])
app.include_router(calculate.router, prefix="", tags=["calculate"])
app.include_router(validate.router, prefix="", tags=["validate"])


# Event handlers
@app.on_event("startup")
async def startup_event():
    """
    Ejecutar al iniciar la aplicación
    """
    print("=" * 60)
    print("🚀 EduCalc Backend iniciando...")
    print(f"📝 Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔐 Auth habilitado: {os.getenv('AUTH_ENABLED', 'false')}")
    print(f"📚 Documentación: http://localhost:{os.getenv('API_PORT', '8000')}/docs")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Ejecutar al cerrar la aplicación
    """
    print("🛑 EduCalc Backend cerrando...")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )


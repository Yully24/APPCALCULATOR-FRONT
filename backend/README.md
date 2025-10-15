# EduCalc Backend API

Backend para calculadora educativa con explicaciones paso a paso. Desarrollado con FastAPI y SymPy.

## 🚀 Características

- **Aritmética básica**: Operaciones numéricas con orden de precedencia
- **Álgebra**: Simplificación y expansión de expresiones
- **Ecuaciones**: Resolución de ecuaciones lineales y cuadráticas
- **Cálculo**: Derivadas e integrales
- **Explicaciones paso a paso**: Cada cálculo incluye pasos detallados
- **API REST**: Endpoints bien documentados con FastAPI
- **Docker**: Containerizado para fácil despliegue

## 📋 Requisitos

- Python 3.11+
- Docker (opcional)
- pip

## 🛠️ Instalación

### Opción 1: Instalación local

```bash
# Clonar el repositorio
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Ejecutar servidor
python -m app.main
# O con uvicorn directamente:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opción 2: Con Docker

```bash
# Construir y ejecutar con docker-compose
docker-compose up --build

# O solo construir la imagen
docker build -t educalc-backend .

# Ejecutar contenedor
docker run -p 8000:8000 educalc-backend
```

## 📖 Uso

### Acceder a la documentación

Una vez iniciado el servidor:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Ejemplos de uso

#### 1. Aritmética básica

```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "2 + 3 * 4",
    "mode": "arithmetic"
  }'
```

#### 2. Álgebra

```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "2*(x + 3) - 4",
    "mode": "algebra"
  }'
```

#### 3. Resolver ecuaciones

```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "2*x + 5 = 15",
    "mode": "solve"
  }'
```

#### 4. Derivadas

```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "x**2 + 3*x",
    "mode": "derivative"
  }'
```

#### 5. Integrales

```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "x**2",
    "mode": "integral"
  }'
```

## 🔌 Endpoints

### POST `/calculate`
Resuelve expresiones matemáticas con pasos explicativos.

**Request Body:**
```json
{
  "expression": "2*(x+3) - 4",
  "mode": "algebra",
  "variables": null
}
```

**Response:**
```json
{
  "original": "2*(x+3) - 4",
  "result": "2*x + 2",
  "steps": [
    {
      "step": 1,
      "description": "Expresión original",
      "expression": "2*(x+3) - 4",
      "detail": "Simplificaremos esta expresión algebraica"
    },
    {
      "step": 2,
      "description": "Expandir expresión",
      "expression": "2*x + 6 - 4",
      "detail": "Aplicar propiedad distributiva"
    }
  ],
  "mode": "algebra",
  "error": null
}
```

### POST `/validate`
Valida una expresión sin resolverla.

### GET `/operations`
Lista todas las operaciones soportadas.

### GET `/health`
Health check del servicio.

## 🏗️ Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app principal
│   ├── models.py              # Modelos Pydantic
│   ├── calculator_engine.py   # Motor de cálculo
│   ├── auth.py                # Autenticación (preparada)
│   ├── utils.py               # Utilidades
│   └── routes/
│       ├── calculate.py       # Endpoint de cálculo
│       ├── validate.py        # Endpoint de validación
│       └── info.py            # Endpoints de información
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest httpx

# Ejecutar tests (cuando se implementen)
pytest app/tests/
```

## 🔒 Seguridad

- **Sin eval()**: Usa SymPy para parseo seguro
- **Sanitización**: Valida y limpia expresiones
- **CORS**: Configurado para orígenes específicos
- **Auth preparada**: Estructura lista para JWT/Supabase

## 🔧 Configuración

Variables de entorno en `.env`:

```bash
# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8081

# Auth (para activar en futuro)
AUTH_ENABLED=false
# SUPABASE_URL=your-url
# SUPABASE_KEY=your-key

# Environment
ENVIRONMENT=development
```

## 📝 Modos de Cálculo

| Modo | Descripción | Ejemplo |
|------|-------------|---------|
| `auto` | Detecta automáticamente | Cualquier expresión |
| `arithmetic` | Aritmética básica | `2 + 3 * 4` |
| `algebra` | Álgebra simbólica | `2*(x+3)` |
| `solve` | Resolver ecuaciones | `2*x + 5 = 15` |
| `derivative` | Derivadas | `x**2 + 3*x` |
| `integral` | Integrales | `x**2` |

## 🚧 Roadmap

- [ ] Tests unitarios completos
- [ ] Integración con base de datos
- [ ] Sistema de auth con JWT
- [ ] Rate limiting
- [ ] Más tipos de operaciones (límites, matrices)
- [ ] Gráficas de funciones
- [ ] CI/CD con GitHub Actions

## 📄 Licencia

Este proyecto es parte de EduCalc.

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias sobre el backend de EduCalc.

---

**Versión**: 1.0.0  
**Fase**: MVP (Producto Mínimo Viable)










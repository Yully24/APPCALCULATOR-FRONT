#!/bin/bash
# Script de despliegue rápido para Google Cloud Run
# Uso: ./deploy-gcloud.sh [PROJECT_ID]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 EduCalc Backend - Deploy to Cloud Run${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Verificar si se proporcionó PROJECT_ID
if [ -z "$1" ]; then
    echo -e "${YELLOW}⚠️  No se proporcionó PROJECT_ID${NC}"
    echo -e "Uso: ./deploy-gcloud.sh PROJECT_ID\n"
    
    # Intentar obtener el proyecto actual de gcloud
    CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
    
    if [ -z "$CURRENT_PROJECT" ]; then
        echo -e "${RED}❌ No hay proyecto configurado en gcloud${NC}"
        echo -e "Por favor ejecuta: ${GREEN}gcloud config set project TU_PROJECT_ID${NC}"
        exit 1
    else
        echo -e "${BLUE}Usando proyecto actual: ${GREEN}$CURRENT_PROJECT${NC}"
        PROJECT_ID=$CURRENT_PROJECT
    fi
else
    PROJECT_ID=$1
    echo -e "${BLUE}Usando proyecto: ${GREEN}$PROJECT_ID${NC}\n"
fi

# Verificar autenticación
echo -e "${YELLOW}🔐 Verificando autenticación...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo -e "${RED}❌ No estás autenticado en gcloud${NC}"
    echo -e "Por favor ejecuta: ${GREEN}gcloud auth login${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Autenticado${NC}\n"

# Configurar proyecto
echo -e "${YELLOW}📋 Configurando proyecto...${NC}"
gcloud config set project $PROJECT_ID
echo -e "${GREEN}✓ Proyecto configurado${NC}\n"

# Habilitar APIs necesarias
echo -e "${YELLOW}🔧 Habilitando APIs necesarias...${NC}"
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet
echo -e "${GREEN}✓ APIs habilitadas${NC}\n"

# Preguntar si desea actualizar variables de entorno
echo -e "${YELLOW}🌍 Variables de entorno:${NC}"
echo -e "  ENVIRONMENT=production"
echo -e "  CORS_ORIGINS=*"
echo -e "  AUTH_ENABLED=false"
echo ""

# Desplegar
echo -e "${BLUE}🚀 Desplegando en Cloud Run...${NC}\n"

gcloud run deploy educalc-backend \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production,CORS_ORIGINS=*,AUTH_ENABLED=false" \
  --max-instances=10 \
  --memory=512Mi \
  --cpu=1 \
  --port=8000

# Obtener URL del servicio
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Despliegue completado exitosamente!${NC}"
echo -e "${GREEN}========================================${NC}\n"

SERVICE_URL=$(gcloud run services describe educalc-backend --region=us-central1 --format='value(status.url)')

echo -e "${BLUE}🌐 URL del servicio:${NC}"
echo -e "${GREEN}$SERVICE_URL${NC}\n"

echo -e "${BLUE}📝 Verificar endpoints:${NC}"
echo -e "Health:  ${GREEN}$SERVICE_URL/health${NC}"
echo -e "Docs:    ${GREEN}$SERVICE_URL/docs${NC}"
echo -e "Redoc:   ${GREEN}$SERVICE_URL/redoc${NC}\n"

echo -e "${BLUE}📊 Ver logs:${NC}"
echo -e "${GREEN}gcloud run services logs read educalc-backend --region=us-central1 --follow${NC}\n"

echo -e "${YELLOW}💡 Tip: Guarda la URL del servicio para configurar tu frontend${NC}"









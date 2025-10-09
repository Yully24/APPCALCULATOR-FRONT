# 🚀 Guía de Despliegue - EduCalc Backend en Google Cloud Run

Esta guía te llevará paso a paso para desplegar tu backend de FastAPI en Google Cloud Run de forma gratuita.

---

## 📋 Prerequisitos

- Cuenta de Google Cloud (incluye $300 de créditos gratis por 90 días)
- Google Cloud CLI (`gcloud`) instalado
- Docker instalado (opcional, Cloud Build lo hará por ti)

---

## 🌐 PASO 1: Configurar Google Cloud

### 1.1 Crear Cuenta y Proyecto

1. Ve a: **https://console.cloud.google.com**
2. Inicia sesión con tu cuenta de Google
3. Acepta los términos y activa los créditos gratuitos ($300)
4. Crea un nuevo proyecto:
   - Click en el selector de proyectos (arriba)
   - Click en **"Nuevo proyecto"**
   - Nombre: `educalc` (o el que prefieras)
   - Click en **"Crear"**

### 1.2 Instalar Google Cloud CLI

**En macOS (con Homebrew):**
```bash
brew install google-cloud-sdk
```

**En Linux/Windows:**
Descarga desde: https://cloud.google.com/sdk/docs/install

### 1.3 Inicializar gcloud

```bash
# Autenticarte
gcloud auth login

# Configurar tu proyecto (reemplaza PROJECT_ID con el ID de tu proyecto)
gcloud config set project PROJECT_ID

# Habilitar APIs necesarias
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

---

## 🔧 PASO 2: Preparar el Backend

### 2.1 Navegar al directorio del backend

```bash
cd /Users/ub-col-tec-t2q/Documents/ProjectsYP/APP/backend
```

### 2.2 Crear archivo .gcloudignore (opcional)

Esto evita subir archivos innecesarios:

```bash
cat > .gcloudignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.log
.git/
.gitignore
*.md
image/
EOF
```

---

## 🐳 PASO 3: Desplegar en Cloud Run

### Opción A: Despliegue Automático (Recomendado)

Cloud Run puede construir tu Docker image automáticamente:

```bash
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
```

### Opción B: Despliegue Manual con Docker

Si prefieres construir la imagen localmente:

```bash
# 1. Configurar Docker para usar GCR
gcloud auth configure-docker

# 2. Construir la imagen
docker build -t gcr.io/PROJECT_ID/educalc-backend:latest .

# 3. Subir la imagen
docker push gcr.io/PROJECT_ID/educalc-backend:latest

# 4. Desplegar en Cloud Run
gcloud run deploy educalc-backend \
  --image=gcr.io/PROJECT_ID/educalc-backend:latest \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production,CORS_ORIGINS=*,AUTH_ENABLED=false" \
  --max-instances=10 \
  --memory=512Mi \
  --cpu=1 \
  --port=8000
```

**Nota:** Reemplaza `PROJECT_ID` con el ID de tu proyecto de Google Cloud.

---

## ⏳ PASO 4: Esperar el Deploy (3-5 minutos)

Verás algo como:

```
Building using Dockerfile and deploying container to Cloud Run service [educalc-backend]...
✓ Building and deploying... Done.
✓ Uploading sources...
✓ Building Container... Logs are available at [...]
✓ Creating Revision...
✓ Routing traffic...
✓ Setting IAM Policy...
Done.
Service [educalc-backend] revision [educalc-backend-00001] has been deployed.
Service URL: https://educalc-backend-xxxxx-uc.a.run.app
```

---

## 🎉 PASO 5: Obtener tu URL

Al final del deploy verás:

```
Service URL: https://educalc-backend-xxxxx-uc.a.run.app
```

Esta es tu URL pública del backend.

También puedes obtenerla con:
```bash
gcloud run services describe educalc-backend --region=us-central1 --format='value(status.url)'
```

---

## ✅ PASO 6: Verificar que Funciona

### Prueba 1: Health Check

```bash
curl https://TU-URL.run.app/health
```

Deberías ver:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "production"
}
```

### Prueba 2: Documentación

Abre en tu navegador:
```
https://TU-URL.run.app/docs
```

### Prueba 3: Hacer un Cálculo

```bash
curl -X POST "https://TU-URL.run.app/calculate" \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 + 3 * 4", "mode": "arithmetic"}'
```

---

## 🔄 PASO 7: Configurar CI/CD (Opcional)

Para despliegues automáticos cuando hagas cambios:

### Crear archivo cloudbuild.yaml

```yaml
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/educalc-backend:$COMMIT_SHA', '.']
  
  # Push the container image to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/educalc-backend:$COMMIT_SHA']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'educalc-backend'
      - '--image=gcr.io/$PROJECT_ID/educalc-backend:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'

images:
  - 'gcr.io/$PROJECT_ID/educalc-backend:$COMMIT_SHA'
```

---

## 💰 Costos (Plan Gratuito)

Cloud Run tiene un tier gratuito generoso:

- **2 millones de peticiones/mes** - GRATIS
- **360,000 GB-segundos/mes** - GRATIS
- **180,000 vCPU-segundos/mes** - GRATIS
- **Sin sleep/cold start** forzado como Render

Ideal para desarrollo, feedback y producción pequeña.

---

## 🔧 Comandos Útiles

### Ver logs en tiempo real
```bash
gcloud run services logs read educalc-backend --region=us-central1 --follow
```

### Actualizar variables de entorno
```bash
gcloud run services update educalc-backend \
  --region=us-central1 \
  --set-env-vars="NUEVA_VAR=valor"
```

### Actualizar CORS origins (cuando tengas frontend)
```bash
gcloud run services update educalc-backend \
  --region=us-central1 \
  --set-env-vars="CORS_ORIGINS=https://tu-frontend.web.app"
```

### Eliminar el servicio
```bash
gcloud run services delete educalc-backend --region=us-central1
```

---

## 🐛 Solución de Problemas

### Error: "Permission denied"
**Solución:** 
```bash
gcloud auth login
gcloud config set project PROJECT_ID
```

### Error: "API not enabled"
**Solución:**
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Error: "Container failed to start"
**Solución:** Revisa los logs:
```bash
gcloud run services logs read educalc-backend --region=us-central1 --limit=50
```

### El servicio no responde en el puerto
**Causa:** Cloud Run espera que la app escuche en el puerto que define la variable `$PORT`
**Solución:** El Dockerfile ya lo configura correctamente en el puerto 8000

---

## 🎯 Siguiente Paso

Una vez que tengas tu URL de Cloud Run funcionando:
1. Guarda la URL: `https://educalc-backend-xxxxx-uc.a.run.app`
2. Ve a la carpeta `frontend-pwa/` para desplegar el frontend en Firebase Hosting o GitHub Pages
3. Actualiza la variable `CORS_ORIGINS` con la URL de tu frontend

---

## 📊 Monitoreo

Puedes ver métricas en:
https://console.cloud.google.com/run

Verás:
- Peticiones por segundo
- Latencia
- Uso de memoria
- Errores
- Logs en tiempo real

---

**¡Listo! Tu backend está en Google Cloud 🎉**



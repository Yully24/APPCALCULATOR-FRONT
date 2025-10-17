#!/bin/bash

# Script de despliegue con cache busting automático
echo "🚀 Iniciando despliegue de EduCalc..."

# 1. Actualizar versión automáticamente
echo "📝 Actualizando versión..."
node update-version.js

# 2. Verificar que no hay errores
echo "🔍 Verificando archivos..."
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html no encontrado"
    exit 1
fi

if [ ! -f "app.js" ]; then
    echo "❌ Error: app.js no encontrado"
    exit 1
fi

echo "✅ Archivos verificados"

# 3. Desplegar frontend (ejemplo para Vercel)
echo "🌐 Desplegando frontend..."
if command -v vercel &> /dev/null; then
    vercel --prod
    echo "✅ Frontend desplegado en Vercel"
else
    echo "⚠️  Vercel CLI no encontrado. Despliega manualmente:"
    echo "   - Sube los archivos a tu plataforma de hosting"
    echo "   - O usa: npm install -g vercel && vercel --prod"
fi

# 4. Desplegar backend (ejemplo para Google Cloud Run)
echo "🔧 Desplegando backend..."
if [ -d "backend" ]; then
    cd backend
    if [ -f "deploy-gcloud.sh" ]; then
        chmod +x deploy-gcloud.sh
        ./deploy-gcloud.sh
        echo "✅ Backend desplegado en Google Cloud Run"
    else
        echo "⚠️  Script de despliegue del backend no encontrado"
        echo "   Despliega manualmente el backend"
    fi
    cd ..
else
    echo "⚠️  Directorio backend no encontrado"
fi

echo ""
echo "🎉 ¡Despliegue completado!"
echo "💡 Los usuarios verán los cambios automáticamente sin borrar caché"
echo "📱 La versión actual es: $(grep 'meta name="version"' index.html | sed 's/.*content="\([^"]*\)".*/\1/')"

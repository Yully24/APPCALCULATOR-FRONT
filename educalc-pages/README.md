# EduCalc PWA - Frontend

Progressive Web App para EduCalc - Calculadora educativa con explicaciones paso a paso.

## 🎯 Características

- ✅ **PWA**: Se instala como app nativa
- ✅ **Responsive**: Funciona en móvil, tablet y desktop
- ✅ **Offline-ready**: Cache de archivos estáticos
- ✅ **Rápida**: Diseño optimizado y ligero
- ✅ **Moderna**: UI limpia y profesional

## 🚀 Inicio Rápido

### Configuración Inicial

**IMPORTANTE**: Antes de desplegar, actualiza la URL del backend en `app.js`:

```javascript
// Línea 7 en app.js
const API_URL = 'https://TU-BACKEND.onrender.com';
```

Reemplaza `TU-BACKEND.onrender.com` con la URL real de tu backend desplegado en Render.

### Desarrollo Local

Para probar localmente con tu backend local:

1. Asegúrate que el backend esté corriendo en `http://localhost:8000`
2. Abre `index.html` en un servidor local:

```bash
# Opción 1: Python
python -m http.server 8080

# Opción 2: Node.js (npx)
npx serve .

# Opción 3: PHP
php -S localhost:8080
```

3. Abre tu navegador en: `http://localhost:8080`

## 📱 Instalación como App

### En Android/Chrome:

1. Abre la PWA en Chrome
2. Toca el menú (⋮)
3. Selecciona "Instalar app" o "Agregar a pantalla de inicio"
4. ¡Listo! La app aparecerá en tu cajón de apps

### En iOS/Safari:

1. Abre la PWA en Safari
2. Toca el botón de compartir (🔼)
3. Selecciona "Agregar a pantalla de inicio"
4. Toca "Añadir"

## 🌐 Despliegue en Producción

Sigue las instrucciones en `DEPLOY.md` para desplegar en:
- Vercel (recomendado)
- Netlify
- GitHub Pages

## 📁 Estructura de Archivos

```
frontend-pwa/
├── index.html           # Página principal
├── styles.css           # Estilos
├── app.js              # Lógica JavaScript
├── manifest.json       # Configuración PWA
├── service-worker.js   # Service Worker (offline)
├── icon-192.png        # Ícono 192x192
├── icon-512.png        # Ícono 512x512
├── README.md           # Este archivo
└── DEPLOY.md           # Guía de despliegue
```

## 🎨 Personalización

### Cambiar Colores

Edita las variables CSS en `styles.css` (líneas 18-28):

```css
:root {
    --primary: #2563eb;      /* Color principal */
    --secondary: #10b981;    /* Color secundario */
    --accent: #8b5cf6;       /* Color de acento */
}
```

### Cambiar Nombre/Logo

Edita `manifest.json`:

```json
{
  "name": "Tu App",
  "short_name": "TuApp"
}
```

Y el header en `index.html` (línea 35):

```html
<h1 class="logo">
    <span class="logo-icon">🎓</span>
    Tu App
</h1>
```

## 🧪 Pruebas

### Probar Funcionalidad

1. Ingresa una expresión: `2 + 3 * 4`
2. Selecciona modo o deja en "Auto"
3. Presiona "Calcular"
4. Deberías ver el resultado y los pasos

### Verificar PWA

Abre Chrome DevTools:
1. Pestaña "Application"
2. Sección "Manifest" - Verifica que se cargue
3. Sección "Service Workers" - Verifica que esté activo

## 🔧 Solución de Problemas

### "No se pudo conectar con el servidor"

**Causa:** El backend no está accesible
**Solución:**
1. Verifica que la URL en `app.js` sea correcta
2. Verifica que el backend esté desplegado y funcionando
3. Abre `https://TU-BACKEND.onrender.com/health` en el navegador

### "Expresión inválida"

**Causa:** Sintaxis incorrecta
**Solución:** Usa los ejemplos como referencia:
- Multiplicación: `*` (no `x`)
- Potencia: `**` (no `^`)
- Variables: `x`, `y`, etc.

### La app no se instala

**Causa:** Requiere HTTPS o localhost
**Solución:** Despliega en Vercel/Netlify (automáticamente tienen HTTPS)

## 📊 Compatibilidad

| Navegador | Versión | Soporte |
|-----------|---------|---------|
| Chrome | 90+ | ✅ Completo |
| Edge | 90+ | ✅ Completo |
| Safari | 14+ | ✅ Completo |
| Firefox | 88+ | ✅ Completo |
| Samsung Internet | 14+ | ✅ Completo |

## 🚀 Próximas Mejoras

- [ ] Historial de cálculos
- [ ] Modo oscuro
- [ ] Exportar resultados como PDF
- [ ] Compartir resultados
- [ ] Gráficas de funciones
- [ ] Más tipos de operaciones

## 📄 Licencia

Parte del proyecto EduCalc.

---

**Versión**: 1.0.0  
**Última actualización**: 2025


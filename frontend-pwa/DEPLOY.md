# 🚀 Guía de Despliegue - EduCalc PWA Frontend

Esta guía te ayudará a desplegar tu PWA en la nube para que puedas compartirla con un link.

---

## ⚠️ IMPORTANTE: Antes de Desplegar

**Debes actualizar la URL del backend en `app.js`:**

Abre `app.js` y en la línea 7 cambia:

```javascript
// ANTES (desarrollo local)
const API_URL = 'http://localhost:8000';

// DESPUÉS (producción)
const API_URL = 'https://TU-BACKEND.onrender.com';
```

Reemplaza `TU-BACKEND.onrender.com` con la URL real que obtuviste al desplegar el backend.

---

## 🌐 Opción 1: Vercel (Recomendada)

Vercel es **gratis**, **rápido** y **fácil**.

### Paso 1: Crear Cuenta

1. Ve a: **https://vercel.com**
2. Click en "Sign Up"
3. Regístrate con GitHub (recomendado)

### Paso 2: Preparar el Proyecto

Si NO tienes el código en GitHub:

```bash
cd /Users/ub-col-tec-t2q/Documents/ProjectsYP/APP
git add frontend-pwa/
git commit -m "Add PWA frontend"
git push
```

### Paso 3: Importar en Vercel

1. En el dashboard de Vercel, click **"Add New..."** → **"Project"**
2. Click **"Import Git Repository"**
3. Selecciona tu repositorio
4. En "Root Directory" click **"Edit"** y pon: `frontend-pwa`
5. Framework Preset: **"Other"**
6. Click **"Deploy"**

### Paso 4: Esperar (30 segundos)

Vercel construirá y desplegará automáticamente.

### Paso 5: Obtener URL

Una vez completado, verás:

```
✅ Your project is ready!
https://educalc-xxxx.vercel.app
```

¡Esa es tu URL! Cópiala y compártela. 🎉

---

## 🌐 Opción 2: Netlify

Muy similar a Vercel, también gratis.

### Paso 1: Crear Cuenta

1. Ve a: **https://netlify.com**
2. Click "Sign Up"
3. Regístrate con GitHub

### Paso 2: Deploy

**Método A: Desde Git**
1. Click **"Add new site"** → **"Import an existing project"**
2. Conecta con GitHub
3. Selecciona tu repositorio
4. Base directory: `frontend-pwa`
5. Build command: (dejar vacío)
6. Publish directory: `.` (punto)
7. Click **"Deploy"**

**Método B: Drag & Drop (más rápido)**
1. Click **"Add new site"** → **"Deploy manually"**
2. Arrastra la carpeta `frontend-pwa` directamente
3. ¡Listo!

### Paso 3: Obtener URL

```
https://educalc-xxxx.netlify.app
```

---

## 🌐 Opción 3: GitHub Pages

Gratis si tu repositorio es público.

### Paso 1: Preparar

1. Asegúrate que tu código esté en GitHub
2. La carpeta `frontend-pwa` debe estar en la raíz

### Paso 2: Configurar

1. Ve a tu repositorio en GitHub
2. Click en **"Settings"**
3. En el menú lateral, click **"Pages"**
4. Source: **"Deploy from a branch"**
5. Branch: **"main"** → Carpeta: **"/ (root)"** o **"/frontend-pwa"**
6. Click **"Save"**

### Paso 3: Acceder

```
https://TU-USUARIO.github.io/TU-REPO/frontend-pwa/
```

**Nota:** GitHub Pages puede tardar 5-10 minutos en activarse.

---

## 🧪 Verificar que Funciona

Una vez desplegado, abre tu URL y:

### 1. Health Check del Backend

Abre la consola del navegador (F12) y verifica:

```
✅ Conectado al backend correctamente
```

Si ves error:
- Verifica que la URL en `app.js` sea correcta
- Verifica que el backend esté funcionando
- Prueba abrir `https://TU-BACKEND.onrender.com/health`

### 2. Probar Cálculo

1. Ingresa: `2 + 3 * 4`
2. Click "Calcular"
3. Deberías ver el resultado: `14`

### 3. Probar Instalación

En el navegador móvil:
- Debería aparecer el botón "📱 Instalar App"
- O en el menú: "Instalar app"

---

## 📱 Compartir para Feedback

### Opción A: Link Directo

Simplemente comparte tu URL:
```
https://educalc-xxxx.vercel.app
```

Cualquiera con el link puede abrirlo en su navegador.

### Opción B: QR Code

Genera un QR code con tu URL:
- https://qr-code-generator.com
- Pega tu URL
- Descarga el QR
- Compártelo en redes sociales, WhatsApp, etc.

### Opción C: Mensaje de WhatsApp

```
🎓 ¡Prueba EduCalc!

Calculadora educativa que te enseña paso a paso.

👉 https://educalc-xxxx.vercel.app

📱 Puedes instalarla como app desde el navegador
```

---

## 🔄 Actualizar la App

### En Vercel/Netlify (con Git):

```bash
# Hacer cambios en frontend-pwa/
git add frontend-pwa/
git commit -m "Update frontend"
git push
```

Vercel/Netlify detectarán el cambio y desplegarán automáticamente.

### En GitHub Pages:

Igual, solo haz push y espera 5 minutos.

---

## 🎨 Personalizar Dominio (Opcional)

Si tienes un dominio propio (ej: `educalc.com`):

### En Vercel:
1. Settings → Domains
2. Add Domain
3. Sigue las instrucciones de DNS

### En Netlify:
1. Domain settings → Add custom domain
2. Configura DNS según instrucciones

---

## ⚠️ Limitaciones del Plan Gratuito

| Servicio | Límites |
|----------|---------|
| **Vercel** | 100GB bandwidth/mes, ilimitados deployments |
| **Netlify** | 100GB bandwidth/mes, 300 build minutes/mes |
| **GitHub Pages** | 100GB/mes, repositorios públicos solo (o pro) |

Para una app de feedback, estos límites son **más que suficientes**.

---

## 🐛 Solución de Problemas

### "Failed to fetch" en la app

**Causa:** Backend no accesible
**Solución:**
1. Verifica URL en `app.js`
2. Asegúrate que el backend permite CORS (ya configurado)
3. Prueba el backend directamente: `https://TU-BACKEND.onrender.com/health`

### La app no se actualiza

**Causa:** Cache del navegador
**Solución:**
1. Limpia cache (Ctrl+Shift+R o Cmd+Shift+R)
2. O abre en ventana incógnita

### El service worker no funciona

**Causa:** Requiere HTTPS
**Solución:** Vercel/Netlify automáticamente usan HTTPS ✅

---

## 📊 Analytics (Opcional)

Para ver cuántas personas usan tu app:

### Google Analytics:

Agrega en `index.html` antes de `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Obtén tu ID en: https://analytics.google.com

---

## 🎯 Checklist Final

Antes de compartir para feedback:

- [ ] Backend desplegado y funcionando
- [ ] URL del backend actualizada en `app.js`
- [ ] Frontend desplegado (Vercel/Netlify)
- [ ] Probado: hacer un cálculo funciona
- [ ] Probado: se puede instalar como app
- [ ] URL lista para compartir
- [ ] (Opcional) QR code generado

---

## 🎉 ¡Listo!

Tu app está en la nube y lista para recibir feedback.

**Tu URL:**
```
https://educalc-xxxx.vercel.app
```

**Siguiente paso:** Compártela y recopila feedback para mejorarla antes de crear la versión nativa (React Native).

---

**¿Problemas?** Revisa los logs en el dashboard de Vercel/Netlify o abre la consola del navegador (F12).





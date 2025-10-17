#!/usr/bin/env node

/**
 * Script para actualizar automáticamente la versión y evitar problemas de caché
 * Se ejecuta antes de cada despliegue
 */

const fs = require('fs');
const path = require('path');

// Generar versión basada en timestamp
const version = `2025-01-25-v${Date.now().toString().slice(-4)}`;

// Archivos a actualizar
const files = [
    'index.html',
    'app.js',
    'styles.css',
    'manifest.json'
];

console.log(`🔄 Actualizando versión a: ${version}`);

// Actualizar index.html
const indexPath = path.join(__dirname, 'index.html');
let indexContent = fs.readFileSync(indexPath, 'utf8');

// Actualizar meta version
indexContent = indexContent.replace(
    /<meta name="version" content="[^"]*">/,
    `<meta name="version" content="${version}">`
);

// Actualizar versiones en enlaces CSS y JS
indexContent = indexContent.replace(
    /href="styles\.css\?v=[^"]*"/,
    `href="styles.css?v=${version}"`
);

indexContent = indexContent.replace(
    /src="app\.js\?v=[^"]*"/,
    `src="app.js?v=${version}"`
);

fs.writeFileSync(indexPath, indexContent);
console.log('✅ index.html actualizado');

// Actualizar manifest.json
const manifestPath = path.join(__dirname, 'manifest.json');
let manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
manifest.version = version;
manifest.version_name = version;
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
console.log('✅ manifest.json actualizado');

// Actualizar service worker para cache busting
const swPath = path.join(__dirname, 'service-worker.js');
if (fs.existsSync(swPath)) {
    let swContent = fs.readFileSync(swPath, 'utf8');
    
    // Agregar o actualizar versión en service worker
    const versionComment = `// Version: ${version}`;
    if (!swContent.includes('// Version:')) {
        swContent = versionComment + '\n' + swContent;
    } else {
        swContent = swContent.replace(/\/\/ Version:.*/, versionComment);
    }
    
    fs.writeFileSync(swPath, swContent);
    console.log('✅ service-worker.js actualizado');
}

console.log(`🎉 Versión ${version} aplicada exitosamente`);
console.log('💡 Los cambios se verán sin necesidad de borrar caché manualmente');

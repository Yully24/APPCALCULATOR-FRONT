// =============================================
// EduCalc - JavaScript Principal
// =============================================

// CONFIGURACIÓN - IMPORTANTE: Cambiar esta URL después de desplegar el backend
const API_URL = 'https://appcalculator.onrender.com';
//'http://localhost:8000'; // Cambiar a tu URL de Render después del deploy
// Ejemplo: const API_URL = 'https://educalc-backend-xxxx.onrender.com';

// =============================================
// Estado de la aplicación
// =============================================
let currentResult = null;
let stepsVisible = false;

// =============================================
// Elementos del DOM
// =============================================
const elements = {
    form: document.getElementById('calculatorForm'),
    expressionInput: document.getElementById('expression'),
    modeSelect: document.getElementById('mode'),
    calculateBtn: document.getElementById('calculateBtn'),
    btnText: document.querySelector('.btn-text'),
    btnLoader: document.querySelector('.btn-loader'),
    
    resultCard: document.getElementById('resultCard'),
    originalExpression: document.getElementById('originalExpression'),
    finalResult: document.getElementById('finalResult'),
    stepsList: document.getElementById('stepsList'),
    toggleStepsBtn: document.getElementById('toggleSteps'),
    toggleStepsText: document.getElementById('toggleStepsText'),
    toggleStepsIcon: document.getElementById('toggleStepsIcon'),
    closeResultBtn: document.getElementById('closeResult'),
    
    errorCard: document.getElementById('errorCard'),
    errorMessage: document.getElementById('errorMessage'),
    closeErrorBtn: document.getElementById('closeError'),
    
    exampleBtns: document.querySelectorAll('.example-btn'),
    installBtn: document.getElementById('installBtn')
};

// =============================================
// Event Listeners
// =============================================

// Form submit
elements.form.addEventListener('submit', handleCalculate);

// Close buttons
elements.closeResultBtn.addEventListener('click', hideResult);
elements.closeErrorBtn.addEventListener('click', hideError);

// Toggle steps
elements.toggleStepsBtn.addEventListener('click', toggleSteps);

// Example buttons
elements.exampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const expr = btn.getAttribute('data-expr');
        const mode = btn.getAttribute('data-mode');
        elements.expressionInput.value = expr;
        elements.modeSelect.value = mode;
        elements.expressionInput.focus();
    });
});

// =============================================
// Funciones principales
// =============================================

async function handleCalculate(e) {
    e.preventDefault();
    
    const expression = elements.expressionInput.value.trim();
    const mode = elements.modeSelect.value;
    
    if (!expression) {
        showError('Por favor, ingresa una expresión matemática');
        return;
    }
    
    // Ocultar resultados previos
    hideResult();
    hideError();
    
    // Mostrar loading
    setLoading(true);
    
    try {
        const result = await calculate(expression, mode);
        showResult(result);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

async function calculate(expression, mode) {
    try {
        const response = await fetch(`${API_URL}/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                expression: expression,
                mode: mode,
                variables: null
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail?.message || errorData.detail || 'Error al calcular');
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        // Manejo de errores de red
        if (error.message.includes('Failed to fetch')) {
            throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté corriendo.');
        }
        throw error;
    }
}

// =============================================
// UI Functions
// =============================================

function showResult(result) {
    currentResult = result;
    stepsVisible = false;
    
    // Llenar datos
    elements.originalExpression.textContent = result.original;
    elements.finalResult.textContent = result.result;
    
    // Renderizar pasos
    renderSteps(result.steps);
    
    // Mostrar card
    elements.resultCard.style.display = 'block';
    elements.stepsList.style.display = 'none';
    elements.toggleStepsText.textContent = 'Ver pasos detallados';
    elements.toggleStepsIcon.textContent = '▼';
    
    // Scroll to result
    setTimeout(() => {
        elements.resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function renderSteps(steps) {
    elements.stepsList.innerHTML = '';
    
    if (!steps || steps.length === 0) {
        elements.stepsList.innerHTML = '<p style="color: var(--gray-600);">No hay pasos disponibles.</p>';
        return;
    }
    
    steps.forEach(step => {
        const stepCard = document.createElement('div');
        stepCard.className = 'step-card';
        
        stepCard.innerHTML = `
            <div class="step-header">
                <div class="step-number">${step.step}</div>
                <div class="step-description">${escapeHtml(step.description)}</div>
            </div>
            ${step.expression ? `<div class="step-expression">${escapeHtml(step.expression)}</div>` : ''}
            ${step.detail ? `<div class="step-detail">${escapeHtml(step.detail)}</div>` : ''}
        `;
        
        elements.stepsList.appendChild(stepCard);
    });
}

function toggleSteps() {
    stepsVisible = !stepsVisible;
    
    if (stepsVisible) {
        elements.stepsList.style.display = 'block';
        elements.toggleStepsText.textContent = 'Ocultar pasos';
        elements.toggleStepsIcon.textContent = '▲';
    } else {
        elements.stepsList.style.display = 'none';
        elements.toggleStepsText.textContent = 'Ver pasos detallados';
        elements.toggleStepsIcon.textContent = '▼';
    }
}

function hideResult() {
    elements.resultCard.style.display = 'none';
    currentResult = null;
    stepsVisible = false;
}

function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorCard.style.display = 'block';
    
    // Scroll to error
    setTimeout(() => {
        elements.errorCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function hideError() {
    elements.errorCard.style.display = 'none';
}

function setLoading(loading) {
    if (loading) {
        elements.calculateBtn.disabled = true;
        elements.btnText.style.display = 'none';
        elements.btnLoader.style.display = 'flex';
    } else {
        elements.calculateBtn.disabled = false;
        elements.btnText.style.display = 'block';
        elements.btnLoader.style.display = 'none';
    }
}

// =============================================
// Utilidades
// =============================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// =============================================
// PWA - Install prompt
// =============================================

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevenir que Chrome muestre el prompt automáticamente
    e.preventDefault();
    // Guardar el evento para usarlo después
    deferredPrompt = e;
    // Mostrar botón de instalación
    elements.installBtn.style.display = 'block';
});

elements.installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) {
        return;
    }
    
    // Mostrar el prompt de instalación
    deferredPrompt.prompt();
    
    // Esperar a que el usuario responda
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response: ${outcome}`);
    
    // Limpiar el prompt
    deferredPrompt = null;
    elements.installBtn.style.display = 'none';
});

// Ocultar botón si ya está instalada
window.addEventListener('appinstalled', () => {
    console.log('PWA instalada');
    elements.installBtn.style.display = 'none';
});

// =============================================
// Detección de conexión (útil para debugging)
// =============================================

window.addEventListener('load', async () => {
    // Test de conexión con el backend
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('✅ Conectado al backend correctamente');
        } else {
            console.warn('⚠️ Backend respondió pero con error');
        }
    } catch (error) {
        console.error('❌ No se pudo conectar al backend:', error);
        console.log('📝 Asegúrate de que el backend esté corriendo en:', API_URL);
    }
});

// =============================================
// Atajos de teclado
// =============================================

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter para calcular
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        elements.form.dispatchEvent(new Event('submit'));
    }
    
    // Escape para cerrar resultados/errores
    if (e.key === 'Escape') {
        hideResult();
        hideError();
    }
});

// =============================================
// Auto-focus en el input al cargar
// =============================================

window.addEventListener('load', () => {
    elements.expressionInput.focus();
});

console.log('EduCalc PWA cargado ✅');
console.log('API URL:', API_URL);


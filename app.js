// =============================================
// EduCalc - JavaScript Principal
// =============================================

// CONFIGURACIÓN - IMPORTANTE: Cambiar esta URL después de desplegar el backend
const API_URL = 'https://educalc-backend-ntw33zfv2a-uc.a.run.app/';
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
    previewContent: document.getElementById('previewContent'),
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
        updateExpressionPreview(); // Actualizar preview
        elements.expressionInput.focus();
    });
});

// Preview en tiempo real
elements.expressionInput.addEventListener('input', updateExpressionPreview);

// =============================================
// Funciones principales
// =============================================

function cleanExpression(expr) {
    // Limpiar y normalizar la expresión antes de enviarla al backend
    let cleaned = expr.trim();
    
    // Remover símbolos matemáticos que no son válidos para SymPy
    cleaned = cleaned.replace(/∫/g, '');  // Remover símbolo de integral
    cleaned = cleaned.replace(/∂/g, 'd'); // Derivada parcial a 'd'
    cleaned = cleaned.replace(/÷/g, '/'); // División
    cleaned = cleaned.replace(/×/g, '*'); // Multiplicación
    
    // Remover espacios extras
    cleaned = cleaned.replace(/\s+/g, ' ').trim();
    
    // Si contiene "dx=" o "d/dx=" es probablemente un resultado, no entrada
    if (cleaned.includes('dx=') || cleaned.includes('d/dx=')) {
        // Extraer solo la parte de la expresión antes del =
        const parts = cleaned.split('=');
        if (parts.length > 1) {
            // Buscar la expresión original (usualmente entre [] o después de dx)
            const match = cleaned.match(/dx\[(.*?)\]/);
            if (match) {
                cleaned = match[1];
            }
        }
    }
    
    // Si contiene "+ C" al final (resultado de integral), removerlo
    cleaned = cleaned.replace(/\s*\+\s*C\s*$/i, '');
    
    return cleaned;
}

async function handleCalculate(e) {
    e.preventDefault();
    
    let expression = elements.expressionInput.value.trim();
    const mode = elements.modeSelect.value;
    
    if (!expression) {
        showError('Por favor, ingresa una expresión matemática');
        return;
    }
    
    // Limpiar y normalizar la expresión
    expression = cleanExpression(expression);
    
    if (!expression) {
        showError('La expresión no es válida después de limpiarla');
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
    
    // Llenar datos - Renderizar expresión original con LaTeX si está disponible
    if (result.steps && result.steps[0] && result.steps[0].expression_latex) {
        try {
            katex.render(result.steps[0].expression_latex, elements.originalExpression, {
                throwOnError: false,
                displayMode: false,
                output: 'html'
            });
        } catch (e) {
            elements.originalExpression.textContent = result.original;
        }
    } else {
        elements.originalExpression.textContent = result.original;
    }
    
    // Renderizar pasos
    renderSteps(result.steps);
    
    // Mostrar card
    elements.resultCard.style.display = 'block';
    elements.stepsList.style.display = 'none';
    elements.toggleStepsText.textContent = 'Ver pasos detallados';
    elements.toggleStepsIcon.textContent = '▼';
    
    // Animar el resultado con conteo
    animateResult(result.result);
    
    // Crear efecto de celebración
    createCelebrationEffect();
    
    // Scroll to result
    setTimeout(() => {
        elements.resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function animateResult(finalValue) {
    // Determinar longitud para ajustar tamaño
    const length = finalValue.toString().length;
    let sizeClass = 'short';
    
    if (length > 15) {
        sizeClass = 'long';
    } else if (length > 8) {
        sizeClass = 'medium';
    }
    
    elements.finalResult.setAttribute('data-length', sizeClass);
    
    // Intentar convertir a número para animar
    const numValue = parseFloat(finalValue);
    
    if (!isNaN(numValue) && isFinite(numValue)) {
        // Es un número, animar con conteo
        const duration = 1000; // 1 segundo
        const steps = 30;
        const increment = numValue / steps;
        let current = 0;
        let step = 0;
        
        const interval = setInterval(() => {
            step++;
            current += increment;
            
            if (step >= steps) {
                current = numValue;
                clearInterval(interval);
            }
            
            // Formatear el número (entero o decimal)
            if (numValue === Math.floor(numValue)) {
                elements.finalResult.textContent = Math.round(current);
            } else {
                elements.finalResult.textContent = current.toFixed(6).replace(/\.?0+$/, '');
            }
        }, duration / steps);
    } else {
        // No es un número simple, mostrar directamente
        elements.finalResult.textContent = finalValue;
    }
}

function createCelebrationEffect() {
    // Agregar clase de celebración
    elements.resultCard.classList.add('celebrating');
    
    // Crear partículas de celebración
    const resultFinal = document.querySelector('.result-final');
    
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'celebration-particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 0.5 + 's';
        particle.innerHTML = ['✨', '⭐', '🌟', '💫', '✓'][Math.floor(Math.random() * 5)];
        resultFinal.appendChild(particle);
        
        // Eliminar después de la animación
        setTimeout(() => particle.remove(), 2000);
    }
    
    // Remover clase después de la animación
    setTimeout(() => {
        elements.resultCard.classList.remove('celebrating');
    }, 2000);
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
        
        // Formatear descripción y detalle preservando saltos de línea
        const formattedDescription = formatTextWithLineBreaks(step.description);
        const formattedDetail = step.detail ? formatTextWithLineBreaks(step.detail) : '';
        
        stepCard.innerHTML = `
            <div class="step-header">
                <div class="step-number">${step.step}</div>
                <div class="step-description">${formattedDescription}</div>
            </div>
            ${step.expression ? `<div class="step-expression math-expression" data-latex="${step.expression_latex || ''}">${escapeHtml(step.expression)}</div>` : ''}
            ${step.detail ? `<div class="step-detail">${formattedDetail}</div>` : ''}
        `;
        
        elements.stepsList.appendChild(stepCard);
    });
    
    // Renderizar todas las expresiones LaTeX
    renderMathExpressions();
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
    // Convertir saltos de línea a <br> y escapar HTML
    const formattedMessage = formatTextWithLineBreaks(message);
    elements.errorMessage.innerHTML = formattedMessage;
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

function formatTextWithLineBreaks(text) {
    // Escapar HTML primero para seguridad
    const escaped = escapeHtml(text);
    
    // Convertir saltos de línea a <br>
    let formatted = escaped.replace(/\n/g, '<br>');
    
    // Convertir listas con viñetas (•) a formato HTML más legible
    formatted = formatted.replace(/•\s*/g, '<br>• ');
    
    // Añadir espaciado a flechas
    formatted = formatted.replace(/👉/g, '<strong>👉</strong>');
    
    return formatted;
}

function renderMathExpressions() {
    // Renderizar todas las expresiones matemáticas con KaTeX
    const mathElements = document.querySelectorAll('.math-expression');
    
    mathElements.forEach(element => {
        const latex = element.getAttribute('data-latex');
        if (latex && latex.trim() !== '') {
            try {
                // Renderizar LaTeX con KaTeX
                katex.render(latex, element, {
                    throwOnError: false,
                    displayMode: true,  // Display mode para mejor visualización
                    output: 'html'
                });
            } catch (error) {
                console.warn('Error renderizando LaTeX:', latex, error);
                // Si falla, mantener el texto original
            }
        }
    });
}

function convertToLaTeX(expression) {
    /**
     * Convierte expresión de texto plano a LaTeX
     * Ejemplos:
     * - 2/3 → \frac{2}{3}
     * - x^2 o x**2 → x^{2}
     * - 2*x → 2x
     * - sqrt(16) → \sqrt{16}
     */
    
    if (!expression || expression.trim() === '') {
        return '';
    }
    
    let latex = expression.trim();
    
    // Funciones matemáticas PRIMERO (antes de modificar paréntesis)
    // Raíz cuadrada: sqrt(x) → \sqrt{x}
    latex = latex.replace(/sqrt\(([^)]+)\)/gi, '\\sqrt{$1}');
    
    // Otras funciones trigonométricas
    latex = latex.replace(/sin\(/gi, '\\sin(');
    latex = latex.replace(/cos\(/gi, '\\cos(');
    latex = latex.replace(/tan\(/gi, '\\tan(');
    latex = latex.replace(/log\(/gi, '\\log(');
    latex = latex.replace(/ln\(/gi, '\\ln(');
    
    // Convertir ** y ^ a exponentes (antes de tocar *)
    // Exponentes con paréntesis: x**(2+1) → x^{2+1}
    latex = latex.replace(/\*\*\(([^)]+)\)/g, '^{$1}');
    latex = latex.replace(/\^\(([^)]+)\)/g, '^{$1}');
    
    // Exponentes simples: x**2 o x^2 → x^{2}
    latex = latex.replace(/\*\*([a-zA-Z0-9]+)/g, '^{$1}');
    latex = latex.replace(/\^([a-zA-Z0-9]+)/g, '^{$1}');
    
    // Detectar y convertir fracciones ANTES de modificar *
    // Fracciones con paréntesis en ambos lados: (a+b)/(c+d)
    latex = latex.replace(/\(([^()]+)\)\s*\/\s*\(([^()]+)\)/g, '\\frac{$1}{$2}');
    
    // Fracciones con paréntesis en numerador: (a+b)/c
    latex = latex.replace(/\(([^()]+)\)\s*\/\s*([^\s()+-/]+)/g, '\\frac{$1}{$2}');
    
    // Fracciones con paréntesis en denominador: a/(b+c)
    latex = latex.replace(/([^\s()+-/]+)\s*\/\s*\(([^()]+)\)/g, '\\frac{$1}{$2}');
    
    // Fracciones simples: 2/3, x/y, 450/3
    latex = latex.replace(/([a-zA-Z0-9.]+)\s*\/\s*([a-zA-Z0-9.]+)/g, '\\frac{$1}{$2}');
    
    // Ahora reemplazar operadores comunes
    // Multiplicación implícita número*variable: 2*x → 2x
    latex = latex.replace(/(\d+)\s*\*\s*([a-zA-Z])/g, '$1$2');
    
    // Resto de multiplicaciones con símbolo ×
    latex = latex.replace(/\*/g, ' \\times ');
    
    // División como símbolo
    latex = latex.replace(/÷/g, ' \\div ');
    
    // Limpiar múltiples espacios
    latex = latex.replace(/\s+/g, ' ').trim();
    
    // Eliminar \\times innecesarios cerca de paréntesis
    latex = latex.replace(/\\times\s*\(/g, '(');
    latex = latex.replace(/\)\s*\\times\s*\(/g, ')(');
    
    return latex;
}

function updateExpressionPreview() {
    const expression = elements.expressionInput.value.trim();
    
    if (!expression) {
        elements.previewContent.innerHTML = '<span class="preview-placeholder">Escribe una expresión...</span>';
        return;
    }
    
    try {
        // Convertir a LaTeX
        const latexExpr = convertToLaTeX(expression);
        
        // Renderizar con KaTeX
        katex.render(latexExpr, elements.previewContent, {
            throwOnError: false,
            displayMode: true,
            output: 'html'
        });
    } catch (error) {
        console.warn('Error en preview:', error);
        // Si falla, mostrar la expresión tal cual
        elements.previewContent.textContent = expression;
    }
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
    // Inicializar preview si hay valor
    if (elements.expressionInput.value.trim()) {
        updateExpressionPreview();
    }
});

// =============================================
// Acordeón para secciones de info
// =============================================

function toggleAccordion(contentId) {
    const content = document.getElementById(contentId);
    const icon = document.getElementById(contentId + 'Icon');
    
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        icon.textContent = '▲';
    } else {
        content.style.display = 'none';
        icon.textContent = '▼';
    }
}

console.log('EduCalc PWA cargado ✅');
console.log('API URL:', API_URL);


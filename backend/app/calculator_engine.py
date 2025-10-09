"""
Motor de cálculo matemático con generación de pasos explicativos
Utiliza SymPy para el procesamiento simbólico
"""
from sympy import (
    sympify, simplify, expand, factor, solve, diff, integrate,
    Eq, symbols, latex, preorder_traversal, Add, Mul, Pow
)
from typing import List, Dict, Any, Optional
from app.models import Step
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


def format_number(value) -> str:
    """
    Formatea un número de manera inteligente:
    - Enteros sin decimales: 14 en lugar de 14.0000000
    - Decimales con máximo 6 cifras significativas: 3.141593
    - Elimina ceros innecesarios: 2.5 en lugar de 2.500000
    """
    try:
        # Convertir a float
        num = float(value)
        
        # Verificar si es un número entero
        if num == int(num):
            return str(int(num))
        
        # Para decimales, usar 6 cifras significativas y eliminar ceros finales
        formatted = f"{num:.10g}"  # 10 cifras significativas máximo
        
        # Si tiene más de 6 decimales, redondear a 6
        if '.' in formatted:
            parts = formatted.split('.')
            if len(parts[1]) > 6:
                formatted = f"{num:.6f}".rstrip('0').rstrip('.')
        
        return formatted
    except:
        # Si falla el formateo, devolver el string original
        return str(value)


class CalculatorEngine:
    """
    Motor principal de cálculo con explicaciones paso a paso
    """
    
    def __init__(self):
        self.supported_modes = [
            "auto", "arithmetic", "algebra", "solve", "derivative", "integral"
        ]
    
    def calculate(self, expression: str, mode: str = "auto", variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Método principal que rutea a los calculadores específicos
        
        Args:
            expression: Expresión matemática
            mode: Modo de cálculo
            variables: Variables para sustituir
        
        Returns:
            Dict con result y steps
        """
        try:
            # Detectar modo automáticamente si es necesario
            if mode == "auto":
                mode = self._detect_mode(expression)
            
            # Validar modo
            if mode not in self.supported_modes:
                raise ValueError(f"Modo no soportado: {mode}")
            
            # Rutear al método apropiado
            if mode == "arithmetic":
                return self._arithmetic(expression)
            elif mode == "algebra":
                return self._algebra(expression)
            elif mode == "solve":
                return self._solve_equation(expression)
            elif mode == "derivative":
                return self._derivative(expression, variables)
            elif mode == "integral":
                return self._integral(expression, variables)
            else:
                raise ValueError(f"Modo no implementado: {mode}")
        
        except Exception as e:
            logger.error(f"Error en cálculo: {str(e)}")
            raise
    
    def _detect_mode(self, expression: str) -> str:
        """
        Detecta automáticamente el tipo de operación
        """
        expr_lower = expression.lower()
        
        # Detectar ecuaciones (contiene =)
        if "=" in expression:
            return "solve"
        
        # Detectar derivadas
        if any(word in expr_lower for word in ["d/dx", "derivative", "diff"]):
            return "derivative"
        
        # Detectar integrales
        if any(word in expr_lower for word in ["integral", "integrate"]):
            return "integral"
        
        # Detectar si hay variables (álgebra)
        try:
            expr = sympify(expression)
            if expr.free_symbols:
                return "algebra"
        except:
            pass
        
        # Por defecto, aritmética
        return "arithmetic"
    
    def _arithmetic(self, expression: str) -> Dict[str, Any]:
        """
        Resuelve operaciones aritméticas básicas
        """
        steps = []
        
        # Paso 1: Expresión original
        steps.append(Step(
            step=1,
            description="Expresión original",
            expression=expression,
            detail="Evaluaremos esta expresión numérica paso a paso"
        ))
        
        try:
            # Parsear expresión
            expr = sympify(expression)
            
            # Paso 2: Identificar operaciones
            operations = self._identify_operations(expr)
            if operations:
                steps.append(Step(
                    step=2,
                    description="Identificar operaciones",
                    expression=str(expr),
                    detail=f"Operaciones presentes: {', '.join(operations)}"
                ))
            
            # Paso 3: Evaluar
            result = expr.evalf()
            result_formatted = format_number(result)
            steps.append(Step(
                step=len(steps) + 1,
                description="Evaluar expresión",
                expression=result_formatted,
                detail="Realizar los cálculos siguiendo el orden de operaciones (PEMDAS)"
            ))
            
            return {
                "result": result_formatted,
                "steps": [s.model_dump() for s in steps],
                "mode": "arithmetic"
            }
        
        except Exception as e:
            raise ValueError(f"Error en aritmética: {str(e)}")
    
    def _algebra(self, expression: str) -> Dict[str, Any]:
        """
        Simplifica y expande expresiones algebraicas
        """
        steps = []
        
        # Paso 1: Expresión original
        steps.append(Step(
            step=1,
            description="Expresión original",
            expression=expression,
            detail="Simplificaremos esta expresión algebraica"
        ))
        
        try:
            expr = sympify(expression)
            
            # Paso 2: Expandir
            expanded = expand(expr)
            if expanded != expr:
                steps.append(Step(
                    step=2,
                    description="Expandir expresión",
                    expression=str(expanded),
                    detail="Aplicar propiedad distributiva y expandir productos"
                ))
                expr = expanded
            
            # Paso 3: Simplificar
            simplified = simplify(expr)
            if simplified != expr:
                steps.append(Step(
                    step=len(steps) + 1,
                    description="Simplificar",
                    expression=str(simplified),
                    detail="Combinar términos semejantes y simplificar"
                ))
                expr = simplified
            
            # Paso final: Resultado
            if len(steps) == 1:
                steps.append(Step(
                    step=2,
                    description="Expresión ya simplificada",
                    expression=str(expr),
                    detail="La expresión no requiere más simplificación"
                ))
            
            return {
                "result": str(expr),
                "steps": [s.model_dump() for s in steps],
                "mode": "algebra"
            }
        
        except Exception as e:
            raise ValueError(f"Error en álgebra: {str(e)}")
    
    def _solve_equation(self, expression: str) -> Dict[str, Any]:
        """
        Resuelve ecuaciones lineales y cuadráticas
        """
        steps = []
        
        # Paso 1: Expresión original
        steps.append(Step(
            step=1,
            description="Ecuación original",
            expression=expression,
            detail="Resolveremos esta ecuación para encontrar el valor de la variable"
        ))
        
        try:
            # Separar por el signo =
            if "=" not in expression:
                raise ValueError("La expresión debe contener un signo '='")
            
            left, right = expression.split("=")
            left_expr = sympify(left.strip())
            right_expr = sympify(right.strip())
            
            # Paso 2: Crear ecuación
            equation = Eq(left_expr, right_expr)
            steps.append(Step(
                step=2,
                description="Expresar como ecuación",
                expression=f"{left_expr} = {right_expr}",
                detail="Identificar los lados de la ecuación"
            ))
            
            # Paso 3: Identificar variable
            free_vars = equation.free_symbols
            if not free_vars:
                raise ValueError("No se encontró ninguna variable en la ecuación")
            
            var = list(free_vars)[0]  # Tomar la primera variable
            steps.append(Step(
                step=3,
                description=f"Variable a resolver: {var}",
                expression=str(equation),
                detail=f"Resolveremos para la variable '{var}'"
            ))
            
            # Paso 4: Resolver
            solutions = solve(equation, var)
            
            # Paso 5: Presentar solución
            if not solutions:
                result_str = "Sin solución"
                detail = "La ecuación no tiene soluciones reales"
            elif len(solutions) == 1:
                sol_formatted = format_number(solutions[0])
                result_str = f"{var} = {sol_formatted}"
                detail = f"La solución única es {var} = {sol_formatted}"
            else:
                sols_formatted = [format_number(s) for s in solutions]
                result_str = f"{var} = {{{', '.join(sols_formatted)}}}"
                detail = f"Las soluciones son: {', '.join(sols_formatted)}"
            
            steps.append(Step(
                step=4,
                description="Solución",
                expression=result_str,
                detail=detail
            ))
            
            return {
                "result": result_str,
                "steps": [s.model_dump() for s in steps],
                "mode": "solve"
            }
        
        except Exception as e:
            raise ValueError(f"Error resolviendo ecuación: {str(e)}")
    
    def _derivative(self, expression: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Calcula derivadas
        """
        steps = []
        
        # Paso 1: Expresión original
        steps.append(Step(
            step=1,
            description="Función original",
            expression=expression,
            detail="Calcularemos la derivada de esta función"
        ))
        
        try:
            expr = sympify(expression)
            
            # Determinar variable
            var = symbols('x')  # Por defecto x
            if variables and 'var' in variables:
                var = symbols(variables['var'])
            elif expr.free_symbols:
                var = list(expr.free_symbols)[0]
            
            steps.append(Step(
                step=2,
                description=f"Variable de derivación: {var}",
                expression=str(expr),
                detail=f"Derivaremos con respecto a '{var}'"
            ))
            
            # Calcular derivada
            derivative = diff(expr, var)
            
            steps.append(Step(
                step=3,
                description="Aplicar reglas de derivación",
                expression=str(derivative),
                detail=self._explain_derivative_rule(expr, var)
            ))
            
            # Simplificar si es posible
            simplified = simplify(derivative)
            if simplified != derivative:
                steps.append(Step(
                    step=4,
                    description="Simplificar resultado",
                    expression=str(simplified),
                    detail="Simplificar la expresión derivada"
                ))
                derivative = simplified
            
            return {
                "result": f"d/d{var}[{expr}] = {derivative}",
                "steps": [s.model_dump() for s in steps],
                "mode": "derivative"
            }
        
        except Exception as e:
            raise ValueError(f"Error calculando derivada: {str(e)}")
    
    def _integral(self, expression: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Calcula integrales indefinidas
        """
        steps = []
        
        # Paso 1: Expresión original
        steps.append(Step(
            step=1,
            description="Función a integrar",
            expression=expression,
            detail="Calcularemos la integral indefinida de esta función"
        ))
        
        try:
            expr = sympify(expression)
            
            # Determinar variable
            var = symbols('x')
            if variables and 'var' in variables:
                var = symbols(variables['var'])
            elif expr.free_symbols:
                var = list(expr.free_symbols)[0]
            
            steps.append(Step(
                step=2,
                description=f"Variable de integración: {var}",
                expression=str(expr),
                detail=f"Integraremos con respecto a '{var}'"
            ))
            
            # Calcular integral
            integral_result = integrate(expr, var)
            
            steps.append(Step(
                step=3,
                description="Aplicar reglas de integración",
                expression=str(integral_result),
                detail="Aplicar las reglas de integración apropiadas"
            ))
            
            # Añadir constante
            result_str = f"{integral_result} + C"
            steps.append(Step(
                step=4,
                description="Añadir constante de integración",
                expression=result_str,
                detail="Las integrales indefinidas incluyen una constante arbitraria C"
            ))
            
            return {
                "result": f"∫{expr} d{var} = {result_str}",
                "steps": [s.model_dump() for s in steps],
                "mode": "integral"
            }
        
        except Exception as e:
            raise ValueError(f"Error calculando integral: {str(e)}")
    
    def _identify_operations(self, expr) -> List[str]:
        """
        Identifica las operaciones presentes en una expresión
        """
        operations = set()
        
        for arg in preorder_traversal(expr):
            if isinstance(arg, Add):
                operations.add("suma/resta")
            elif isinstance(arg, Mul):
                operations.add("multiplicación/división")
            elif isinstance(arg, Pow):
                operations.add("potencia")
        
        return list(operations)
    
    def _explain_derivative_rule(self, expr, var) -> str:
        """
        Genera explicación de la regla de derivación aplicada
        """
        if expr.is_polynomial(var):
            return "Aplicar regla de la potencia: d/dx[x^n] = n*x^(n-1)"
        elif expr.has(sympify('sin'), sympify('cos'), sympify('tan')):
            return "Aplicar reglas de derivación trigonométricas"
        else:
            return "Aplicar reglas de derivación correspondientes"
    
    def validate_expression(self, expression: str, mode: str = "auto") -> bool:
        """
        Valida que una expresión sea parseable y segura
        """
        try:
            # Intentar parsear
            expr = sympify(expression, evaluate=False)
            return True
        except Exception as e:
            logger.warning(f"Expresión inválida: {expression}, error: {str(e)}")
            return False




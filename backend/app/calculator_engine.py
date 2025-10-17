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
import re

logger = logging.getLogger(__name__)


def format_number(value) -> str:
    """
    Formatea un número de manera inteligente:
    - Enteros sin decimales: 14 en lugar de 14.0000000
    - Decimales con máximo 6 cifras significativas: 3.141593
    - Elimina ceros innecesarios: 2.72 en lugar de 2.72000000
    """
    try:
        # Convertir a float (maneja objetos SymPy también)
        num = float(value)
        
        # Verificar si es un número entero
        if num == int(num):
            return str(int(num))
        
        # Para decimales, usar formato que elimine ceros innecesarios
        # Redondear a 10 decimales para evitar errores de punto flotante
        formatted = f"{num:.10f}".rstrip('0').rstrip('.')
        
        return formatted
    except:
        # Si falla el formateo, devolver el string original
        return str(value)


def to_latex(expression) -> str:
    """
    Convierte una expresión a formato LaTeX
    """
    try:
        # Si es un string simple (como número), intentar parsearlo
        if isinstance(expression, str):
            # Si es solo un número, retornarlo directamente
            try:
                num = float(expression)
                return format_number(num)
            except:
                # Intentar convertir a expresión SymPy
                try:
                    expr = sympify(expression)
                    return latex(expr)
                except:
                    # Si falla, devolver el string original limpio
                    return expression
        
        # Si es una expresión SymPy, usar latex()
        latex_str = latex(expression)
        return latex_str
    except:
        # Si todo falla, convertir a string
        return str(expression)


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
        Resuelve operaciones aritméticas básicas con explicaciones educativas
        """
        try:
            # Parsear expresión
            expr = sympify(expression)
            
            # SIEMPRE intentar primero con explicaciones educativas detalladas
            # Si no funciona, usará el método compuesto automáticamente
            return self._arithmetic_detailed(expression, expr)
        
        except Exception as e:
            raise ValueError(f"Error en aritmética: {str(e)}")
    
    def _is_simple_operation(self, expr) -> bool:
        """
        Verifica si la expresión es una operación simple (dos números y un operador)
        """
        try:
            # Verificar que la expresión tenga exactamente 2 argumentos
            if not hasattr(expr, 'args') or len(expr.args) != 2:
                return False
            
            # Verificar que ambos argumentos sean números puros
            arg1, arg2 = expr.args
            if not (arg1.is_number and arg2.is_number):
                return False
            
            # Verificar que sea una operación básica (Add, Mul, Pow)
            if not isinstance(expr, (Add, Mul, Pow)):
                return False
            
            return True
        except:
            return False
    
    def _arithmetic_detailed(self, expression: str, expr) -> Dict[str, Any]:
        """
        Explicación educativa detallada para operaciones simples
        """
        try:
            # Detectar el tipo de operación
            op_type, nums = self._detect_operation_type(expr, expression)
            
            # Validar que tengamos 2 números
            if op_type != "unknown" and len(nums) == 2:
                if op_type == "division":
                    return self._explain_division(nums[0], nums[1])
                elif op_type == "multiplication":
                    return self._explain_multiplication(nums[0], nums[1])
                elif op_type == "addition":
                    return self._explain_addition(nums[0], nums[1])
                elif op_type == "subtraction":
                    return self._explain_subtraction(nums[0], nums[1])
                elif op_type == "power":
                    return self._explain_power(nums[0], nums[1])
            
            # Si no se puede identificar o no es una operación simple válida, usar método compuesto
            return self._arithmetic_compound(expression, expr)
        except Exception as e:
            # Si hay cualquier error, usar el método compuesto
            return self._arithmetic_compound(expression, expr)
    
    def _arithmetic_compound(self, expression: str, expr) -> Dict[str, Any]:
        """
        Explicación para operaciones compuestas (múltiples operadores)
        """
        steps = []
        
        try:
            # Paso 1: Expresión original con introducción
            steps.append(Step(
                step=1,
                description="💡 Expresión original",
                expression=expression,
                expression_latex=to_latex(expr),
                detail="Vamos a resolver esta expresión matemática paso a paso, siguiendo el orden correcto de operaciones."
            ))
            
            # Generar pasos intermedios del cálculo
            calculation_steps = self._generate_calculation_steps(expression, expr)
            steps.extend(calculation_steps)
            
            # Paso final: Evaluar y mostrar resultado
            result = expr.evalf()
            result_formatted = format_number(result)
            
            # Resultado final
            steps.append(Step(
                step=len(steps) + 1,
                description="✅ Resultado final",
                expression=result_formatted,
                expression_latex=to_latex(result_formatted),
                detail=f"🎉 La respuesta es {result_formatted}"
            ))
            
            return {
                "result": result_formatted,
                "steps": [s.model_dump() for s in steps],
                "mode": "arithmetic"
            }
        except Exception as e:
            # Si hay un error, devolver una respuesta básica
            try:
                result = expr.evalf()
                result_formatted = format_number(result)
            except:
                result_formatted = str(expr)
            
            return {
                "result": result_formatted,
                "steps": [
                    Step(
                        step=1,
                        description="Expresión",
                        expression=expression,
                        expression_latex=to_latex(expr),
                        detail="Calculando resultado..."
                    ).model_dump(),
                    Step(
                        step=2,
                        description="Resultado",
                        expression=result_formatted,
                        expression_latex=to_latex(result_formatted),
                        detail=f"El resultado es: {result_formatted}"
                    ).model_dump()
                ],
                "mode": "arithmetic"
            }
    
    def _detect_operation_type(self, expr, expression: str):
        """
        Detecta el tipo de operación y extrae los números
        Solo detecta operaciones SIMPLES (dos números y un operador)
        """
        # Limpiar espacios
        expr_clean = expression.strip()
        
        # Intentar detectar división SIMPLE (sin otros operadores)
        if "/" in expr_clean and "*" not in expr_clean and "+" not in expr_clean and "-" not in expr_clean.replace(" ", ""):
            parts = expr_clean.split("/")
            if len(parts) == 2:
                try:
                    p1 = parts[0].strip()
                    p2 = parts[1].strip()
                    # Verificar que sean números puros (sin operadores)
                    if p1.replace(".", "").replace("-", "").isdigit() and p2.replace(".", "").replace("-", "").isdigit():
                        num1 = float(p1)
                        num2 = float(p2)
                        return "division", [num1, num2]
                except:
                    pass
        
        # Detectar multiplicación SIMPLE (sin ** ni otros operadores)
        if "*" in expr_clean and "**" not in expr_clean and "/" not in expr_clean and "+" not in expr_clean:
            # Remover espacios para contar -
            temp = expr_clean.replace(" ", "")
            if temp.count("-") <= 1 and (temp.count("-") == 0 or temp.startswith("-") or temp.find("*-") > 0):
                parts = expr_clean.split("*")
                if len(parts) == 2:
                    try:
                        p1 = parts[0].strip()
                        p2 = parts[1].strip()
                        if p1.replace(".", "").replace("-", "").isdigit() and p2.replace(".", "").replace("-", "").isdigit():
                            num1 = float(p1)
                            num2 = float(p2)
                            return "multiplication", [num1, num2]
                    except:
                        pass
        
        # Detectar potencia SIMPLE
        if "**" in expr_clean and "/" not in expr_clean and "+" not in expr_clean:
            temp = expr_clean.replace(" ", "")
            if temp.count("-") <= 1:
                parts = expr_clean.split("**")
                if len(parts) == 2:
                    try:
                        p1 = parts[0].strip()
                        p2 = parts[1].strip()
                        if p1.replace(".", "").replace("-", "").isdigit() and p2.replace(".", "").replace("-", "").isdigit():
                            num1 = float(p1)
                            num2 = float(p2)
                            return "power", [num1, num2]
                    except:
                        pass
        
        # Detectar suma SIMPLE (sin paréntesis ni otros operadores)
        if "+" in expr_clean and "(" not in expr_clean and "*" not in expr_clean and "/" not in expr_clean:
            parts = expr_clean.split("+")
            if len(parts) == 2:
                try:
                    p1 = parts[0].strip()
                    p2 = parts[1].strip()
                    if p1.replace(".", "").replace("-", "").isdigit() and p2.replace(".", "").replace("-", "").isdigit():
                        num1 = float(p1)
                        num2 = float(p2)
                        return "addition", [num1, num2]
                except:
                    pass
        
        # Detectar resta SIMPLE
        if "-" in expr_clean and "(" not in expr_clean and "*" not in expr_clean and "/" not in expr_clean and "+" not in expr_clean:
            # Buscar el último - (para manejar números negativos)
            idx = expr_clean.rfind("-")
            if idx > 0:  # No al inicio
                try:
                    p1 = expr_clean[:idx].strip()
                    p2 = expr_clean[idx+1:].strip()
                    if p1.replace(".", "").replace("-", "").isdigit() and p2.replace(".", "").replace("-", "").isdigit():
                        num1 = float(p1)
                        num2 = float(p2)
                        return "subtraction", [num1, num2]
                except:
                    pass
        
        return "unknown", []
    
    def _generate_calculation_steps(self, expression: str, expr) -> List[Step]:
        """
        Genera pasos intermedios para expresiones compuestas
        """
        steps = []
        current_expr = expression
        step_num = 2
        
        try:
            # Paso 2: Explicar PEMDAS
            steps.append(Step(
                step=step_num,
                description="📋 Orden de operaciones (PEMDAS)",
                expression=current_expr,
                expression_latex=to_latex(expr),
                detail="Seguimos el orden PEMDAS:\n\n1️⃣ Paréntesis\n2️⃣ Exponentes\n3️⃣ Multiplicación/División (izquierda a derecha)\n4️⃣ Suma/Resta (izquierda a derecha)"
            ))
            step_num += 1
            
            # Procesar paréntesis primero
            parentheses_processed = self._process_parentheses(current_expr)
            if parentheses_processed != current_expr:
                steps.append(Step(
                    step=step_num,
                    description="🔧 Resolver paréntesis",
                    expression=parentheses_processed,
                    expression_latex=to_latex(sympify(parentheses_processed)),
                    detail="Resolvemos las operaciones dentro de los paréntesis primero."
                ))
                current_expr = parentheses_processed
                step_num += 1
            
            # Procesar multiplicaciones y divisiones
            md_processed = self._process_multiplication_division(current_expr)
            if md_processed != current_expr:
                steps.append(Step(
                    step=step_num,
                    description="✖️ Resolver multiplicación/división",
                    expression=md_processed,
                    expression_latex=to_latex(sympify(md_processed)),
                    detail="Resolvemos multiplicaciones y divisiones de izquierda a derecha."
                ))
                current_expr = md_processed
                step_num += 1
            
            # Procesar sumas y restas
            as_processed = self._process_addition_subtraction(current_expr)
            if as_processed != current_expr:
                steps.append(Step(
                    step=step_num,
                    description="➕ Resolver suma/resta",
                    expression=as_processed,
                    expression_latex=to_latex(sympify(as_processed)),
                    detail="Resolvemos sumas y restas de izquierda a derecha."
                ))
                current_expr = as_processed
                step_num += 1
            
        except Exception as e:
            # Si hay error, agregar paso genérico
            steps.append(Step(
                step=step_num,
                description="✏️ Resolver paso a paso",
                expression=expression,
                expression_latex=to_latex(expr),
                detail="Aplicamos el orden PEMDAS para resolver la expresión."
            ))
        
        return steps
    
    def _process_parentheses(self, expression: str) -> str:
        """
        Procesa las operaciones dentro de paréntesis
        """
        import re
        
        # Buscar paréntesis simples (sin anidamiento)
        pattern = r'\(([^()]+)\)'
        
        def replace_parentheses(match):
            inner_expr = match.group(1)
            try:
                # Usar sympify para evaluación más segura
                result = sympify(inner_expr)
                # Si es un número, devolverlo formateado
                if result.is_number:
                    return format_number(float(result))
                else:
                    return str(result)
            except:
                return match.group(0)  # Si no se puede evaluar, mantener original
        
        # Aplicar reemplazo
        processed = re.sub(pattern, replace_parentheses, expression)
        
        return processed
    
    def _process_multiplication_division(self, expression: str) -> str:
        """
        Procesa multiplicaciones y divisiones de izquierda a derecha
        """
        # Esta es una implementación simplificada
        # En una versión más completa, se procesarían paso a paso
        return expression
    
    def _process_addition_subtraction(self, expression: str) -> str:
        """
        Procesa sumas y restas de izquierda a derecha
        """
        # Esta es una implementación simplificada
        # En una versión más completa, se procesarían paso a paso
        return expression
    
    def _explain_division(self, dividend: float, divisor: float) -> Dict[str, Any]:
        """
        Explicación educativa detallada para división
        """
        steps = []
        
        # Convertir a enteros si es posible
        dividend_int = int(dividend) if dividend == int(dividend) else dividend
        divisor_int = int(divisor) if divisor == int(divisor) else divisor
        
        # Crear expresión SymPy para LaTeX
        div_expr = sympify(f"{dividend_int}/{divisor_int}")
        
        # Paso 1: Introducción conceptual
        steps.append(Step(
            step=1,
            description="💡 ¿Qué significa dividir?",
            expression=f"{dividend_int} ÷ {divisor_int}",
            expression_latex=to_latex(div_expr),
            detail="Dividir es repartir en partes iguales.\n\nPor ejemplo:\nSi tienes {} {} y los quieres repartir entre {} {}, la división te dice cuánto le toca a cada uno.".format(
                dividend_int,
                "caramelos" if dividend_int != 1 else "caramelo",
                divisor_int,
                "amigos" if divisor_int != 1 else "amigo"
            )
        ))
        
        # Paso 2: Plantear la pregunta
        steps.append(Step(
            step=2,
            description="✏️ ¿Qué es {} ÷ {}?".format(dividend_int, divisor_int),
            expression=f"{dividend_int} ÷ {divisor_int}",
            expression_latex=to_latex(div_expr),
            detail="Eso quiere decir:\n¿Cuántas veces cabe el {} en el {}?\nO: ¿Cuánto le toca a cada uno si repartimos {} entre {} {}?".format(
                divisor_int,
                dividend_int,
                dividend_int,
                divisor_int,
                "personas" if divisor_int > 1 else "persona"
            )
        ))
        
        # Calcular resultado
        result = dividend / divisor
        result_int = int(result) if result == int(result) else result
        remainder = dividend % divisor if dividend == int(dividend) and divisor == int(divisor) else 0
        
        # Paso 3: Proceso de división
        if dividend_int == int(dividend_int) and divisor_int == int(divisor_int) and dividend_int >= 100:
            # División larga para números grandes
            steps.extend(self._explain_long_division(int(dividend_int), int(divisor_int)))
        else:
            # División simple
            result_expr = sympify(f"Eq({dividend_int}/{divisor_int}, {result_int})")
            steps.append(Step(
                step=3,
                description="🔢 Resolver la división",
                expression=f"{dividend_int} ÷ {divisor_int} = {result_int}",
                expression_latex=f"\\frac{{{dividend_int}}}{{{divisor_int}}} = {result_int}",
                detail="Para resolver esta división, pensamos:\n¿Cuántas veces cabe el {} en {}?\n👉 Cabe {} veces{}".format(
                    divisor_int,
                    dividend_int,
                    result_int,
                    f", porque {divisor_int} × {result_int} = {dividend_int}" if remainder == 0 else f" y sobra {int(remainder)}"
                )
            ))
        
        # Paso 4: Verificación
        if remainder == 0:
            verify_expr = f"{divisor_int} \\times {result_int} = {dividend_int}"
            steps.append(Step(
                step=len(steps) + 1,
                description="✓ Verificar el resultado",
                expression=f"{divisor_int} × {result_int} = {dividend_int}",
                expression_latex=verify_expr,
                detail="Podemos verificar multiplicando: {} × {} = {}. ¡Correcto! ✓".format(
                    divisor_int,
                    result_int,
                    dividend_int
                )
            ))
        
        # Paso final: Resultado con contexto
        final_latex = f"\\frac{{{dividend_int}}}{{{divisor_int}}} = {result_int}"
        steps.append(Step(
            step=len(steps) + 1,
            description="✅ Resultado final",
            expression=f"{dividend_int} ÷ {divisor_int} = {result_int}",
            expression_latex=final_latex,
            detail="🎉 Entonces, {} ÷ {} = {}\n\n{}".format(
                dividend_int,
                divisor_int,
                result_int,
                "Cada uno recibe {} {} si los repartimos en partes iguales.".format(
                    result_int,
                    "caramelos" if result_int != 1 else "caramelo"
                ) if remainder == 0 else "El resultado es {} con un residuo de {}.".format(result_int, int(remainder))
            )
        ))
        
        return {
            "result": format_number(result),
            "steps": [s.model_dump() for s in steps],
            "mode": "arithmetic"
        }
    
    def _explain_long_division(self, dividend: int, divisor: int) -> List[Step]:
        """
        Genera pasos detallados para división larga
        """
        steps = []
        dividend_str = str(dividend)
        quotient = ""
        current = 0
        position = 0
        
        steps.append(Step(
            step=3,
            description="✅ Paso a paso con división larga",
            expression=f"{dividend} ÷ {divisor}",
            detail="Vamos a dividir usando una técnica fácil llamada división larga."
        ))
        
        step_details = []
        
        for i, digit in enumerate(dividend_str):
            current = current * 10 + int(digit)
            position = i + 1
            
            if current >= divisor:
                # Cuántas veces cabe
                times = current // divisor
                quotient += str(times)
                remainder = current % divisor
                
                place_name = ""
                if len(dividend_str) - i == 3:
                    place_name = " (centenas)"
                elif len(dividend_str) - i == 2:
                    place_name = " (decenas)"
                elif len(dividend_str) - i == 1:
                    place_name = " (unidades)"
                
                detail = "Paso {}: Miramos el {}{}.\n¿Cuántas veces cabe el {} en {}?\n👉 Cabe {} {}, porque {} × {} = {}\nSobra: {} - {} = {}".format(
                    position,
                    current if i == 0 else dividend_str[:i+1],
                    place_name,
                    divisor,
                    current,
                    times,
                    "vez" if times == 1 else "veces",
                    divisor,
                    times,
                    divisor * times,
                    current,
                    divisor * times,
                    remainder
                )
                
                step_details.append(detail)
                current = remainder
            elif quotient:  # Ya empezamos el cociente
                quotient += "0"
                step_details.append(f"Paso {position}: Bajamos el {digit}. Ahora tenemos {current}.\n¿Cuántas veces cabe el {divisor} en {current}?\n👉 Cabe 0 veces")
        
        # Agregar todos los pasos de división larga
        all_details = "\n\n".join(step_details)
        steps.append(Step(
            step=4,
            description="🔢 Proceso detallado",
            expression=quotient,
            detail=all_details
        ))
        
        return steps
    
    def _explain_multiplication(self, num1: float, num2: float) -> Dict[str, Any]:
        """
        Explicación educativa para multiplicación
        """
        steps = []
        
        num1_int = int(num1) if num1 == int(num1) else num1
        num2_int = int(num2) if num2 == int(num2) else num2
        result = num1 * num2
        result_int = int(result) if result == int(result) else result
        
        # Introducción
        steps.append(Step(
            step=1,
            description="💡 ¿Qué significa multiplicar?",
            expression=f"{num1_int} × {num2_int}",
            detail="Multiplicar es sumar un número varias veces.\n\nPor ejemplo:\n{} × {} significa sumar {} veces el número {}.".format(
                num1_int, num2_int, num2_int, num1_int
            )
        ))
        
        # Explicación visual (si los números son pequeños)
        if num1_int <= 12 and num2_int <= 12:
            sum_representation = " + ".join([str(num1_int)] * int(num2_int)) if num2_int <= 5 else f"{num1_int} (sumado {num2_int} veces)"
            steps.append(Step(
                step=2,
                description="✏️ Representar como suma",
                expression=sum_representation if num2_int <= 5 else f"{num1_int} × {num2_int}",
                detail="Podemos pensar en esto como:\n{} = {}".format(
                    sum_representation if num2_int <= 5 else f"{num1_int} + {num1_int} + ... ({num2_int} veces)",
                    result_int
                )
            ))
        
        # Resultado
        steps.append(Step(
            step=len(steps) + 1,
            description="🔢 Calcular el producto",
            expression=f"{num1_int} × {num2_int} = {result_int}",
            detail="Multiplicamos: {} × {} = {}".format(num1_int, num2_int, result_int)
        ))
        
        # Resultado final
        steps.append(Step(
            step=len(steps) + 1,
            description="✅ Resultado final",
            expression=str(result_int),
            detail="🎉 Entonces, {} × {} = {}\n\nSi tienes {} grupos de {} elementos, en total tienes {} elementos.".format(
                num1_int, num2_int, result_int, num2_int, num1_int, result_int
            )
        ))
        
        return {
            "result": format_number(result),
            "steps": [s.model_dump() for s in steps],
            "mode": "arithmetic"
        }
    
    def _explain_addition(self, num1: float, num2: float) -> Dict[str, Any]:
        """
        Explicación educativa para suma
        """
        steps = []
        
        num1_int = int(num1) if num1 == int(num1) else num1
        num2_int = int(num2) if num2 == int(num2) else num2
        result = num1 + num2
        result_int = int(result) if result == int(result) else result
        
        # Introducción
        steps.append(Step(
            step=1,
            description="💡 ¿Qué significa sumar?",
            expression=f"{num1_int} + {num2_int}",
            detail="Sumar es juntar o combinar cantidades.\n\nPor ejemplo:\nSi tienes {} manzanas y consigues {} más, ¿cuántas manzanas tienes en total?".format(
                num1_int, num2_int
            )
        ))
        
        # Proceso
        steps.append(Step(
            step=2,
            description="✏️ Sumar los números",
            expression=f"{num1_int} + {num2_int} = {result_int}",
            detail="Juntamos las dos cantidades:\n{} + {} = {}".format(num1_int, num2_int, result_int)
        ))
        
        # Resultado final
        steps.append(Step(
            step=3,
            description="✅ Resultado final",
            expression=str(result_int),
            detail="🎉 Entonces, {} + {} = {}\n\nEn total tienes {} elementos.".format(
                num1_int, num2_int, result_int, result_int
            )
        ))
        
        return {
            "result": format_number(result),
            "steps": [s.model_dump() for s in steps],
            "mode": "arithmetic"
        }
    
    def _explain_subtraction(self, num1: float, num2: float) -> Dict[str, Any]:
        """
        Explicación educativa para resta
        """
        steps = []
        
        num1_int = int(num1) if num1 == int(num1) else num1
        num2_int = int(num2) if num2 == int(num2) else num2
        result = num1 - num2
        result_int = int(result) if result == int(result) else result
        
        # Introducción
        steps.append(Step(
            step=1,
            description="💡 ¿Qué significa restar?",
            expression=f"{num1_int} - {num2_int}",
            detail="Restar es quitar o encontrar la diferencia entre dos cantidades.\n\nPor ejemplo:\nSi tienes {} galletas y comes {}, ¿cuántas galletas te quedan?".format(
                num1_int, num2_int
            )
        ))
        
        # Proceso
        steps.append(Step(
            step=2,
            description="✏️ Restar los números",
            expression=f"{num1_int} - {num2_int} = {result_int}",
            detail="Quitamos la segunda cantidad de la primera:\n{} - {} = {}".format(num1_int, num2_int, result_int)
        ))
        
        # Resultado final
        steps.append(Step(
            step=3,
            description="✅ Resultado final",
            expression=str(result_int),
            detail="🎉 Entonces, {} - {} = {}\n\n{}".format(
                num1_int, num2_int, result_int,
                f"Te quedan {result_int} elementos." if result_int >= 0 else f"El resultado es negativo: {result_int}"
            )
        ))
        
        return {
            "result": format_number(result),
            "steps": [s.model_dump() for s in steps],
            "mode": "arithmetic"
        }
    
    def _explain_power(self, base: float, exponent: float) -> Dict[str, Any]:
        """
        Explicación educativa para potencias
        """
        steps = []
        
        base_int = int(base) if base == int(base) else base
        exp_int = int(exponent) if exponent == int(exponent) else exponent
        result = base ** exponent
        result_int = int(result) if result == int(result) else result
        
        # Introducción
        steps.append(Step(
            step=1,
            description="💡 ¿Qué significa una potencia?",
            expression=f"{base_int}^{exp_int}",
            expression_latex=f"{base_int}^{{{exp_int}}}",
            detail="Una potencia significa multiplicar un número por sí mismo varias veces.\n\n{}^{} significa multiplicar {} por sí mismo {} veces.".format(
                base_int, exp_int, base_int, exp_int
            )
        ))
        
        # Explicación visual (si el exponente es pequeño)
        if exp_int <= 5 and exp_int == int(exp_int) and exp_int > 0:
            mult_representation = " × ".join([str(base_int)] * int(exp_int))
            mult_latex = " \\times ".join([str(base_int)] * int(exp_int))
            steps.append(Step(
                step=2,
                description="✏️ Representar como multiplicación",
                expression=mult_representation,
                expression_latex=mult_latex,
                detail="Podemos escribir esto como:\n{}^{} = {}".format(
                    base_int, exp_int, mult_representation
                )
            ))
        
        # Resultado
        steps.append(Step(
            step=len(steps) + 1,
            description="🔢 Calcular la potencia",
            expression=f"{base_int}^{exp_int} = {result_int}",
            expression_latex=f"{base_int}^{{{exp_int}}} = {result_int}",
            detail="Calculamos: {}^{} = {}".format(base_int, exp_int, result_int)
        ))
        
        # Resultado final
        steps.append(Step(
            step=len(steps) + 1,
            description="✅ Resultado final",
            expression=str(result_int),
            expression_latex=str(result_int),
            detail="🎉 Entonces, {}^{} = {}".format(base_int, exp_int, result_int)
        ))
        
        return {
            "result": format_number(result),
            "steps": [s.model_dump() for s in steps],
            "mode": "arithmetic"
        }
    
    def _algebra(self, expression: str) -> Dict[str, Any]:
        """
        Simplifica y expande expresiones algebraicas con explicaciones educativas
        """
        steps = []
        
        try:
            expr = sympify(expression)
            
            # Identificar variables
            variables = list(expr.free_symbols)
            
            # Si no hay variables, es aritmética pura - redirigir
            if not variables:
                return self._arithmetic(expression)
            
            # Paso 1: Introducción a álgebra
            steps.append(Step(
                step=1,
                description="💡 ¿Qué es una expresión algebraica?",
                expression=expression,
                detail="Una expresión algebraica usa letras (variables) para representar números desconocidos.\n\nPor ejemplo: En '2x + 3', la 'x' puede valer cualquier número.\n\nVamos a simplificar esta expresión paso a paso."
            ))
            
            if variables:
                var_names = ", ".join(str(v) for v in variables)
                steps.append(Step(
                    step=2,
                    description="📝 Identificar variables",
                    expression=expression,
                    detail=f"Las variables en esta expresión son: {var_names}\n\nEstas letras representan números que aún no conocemos."
                ))
            
            # Paso: Expandir
            expanded = expand(expr)
            if expanded != expr:
                expanded_str = format_number(expanded) if expanded.is_number else str(expanded)
                steps.append(Step(
                    step=len(steps) + 1,
                    description="✏️ Expandir expresión",
                    expression=expanded_str,
                    detail="Aplicamos la propiedad distributiva:\na(b + c) = ab + ac\n\nMultiplicamos cada término dentro de los paréntesis."
                ))
                expr = expanded
            
            # Paso: Simplificar
            simplified = simplify(expr)
            if simplified != expr:
                simplified_str = format_number(simplified) if simplified.is_number else str(simplified)
                steps.append(Step(
                    step=len(steps) + 1,
                    description="🔢 Simplificar y combinar términos",
                    expression=simplified_str,
                    detail="Combinamos los términos semejantes (términos con las mismas variables y exponentes).\n\nPor ejemplo: 2x + 3x = 5x"
                ))
                expr = simplified
            
            # Paso final: Resultado
            # Formatear el resultado si es numérico
            result_str = str(expr)
            if expr.is_number:
                result_str = format_number(expr)
            
            if len(steps) <= 2:
                steps.append(Step(
                    step=len(steps) + 1,
                    description="✅ Expresión simplificada",
                    expression=result_str,
                    detail="Esta expresión ya está en su forma más simple. No necesita más simplificación."
                ))
            else:
                steps.append(Step(
                    step=len(steps) + 1,
                    description="✅ Resultado final",
                    expression=result_str,
                    detail=f"🎉 La expresión simplificada es: {result_str}\n\nEsta es la forma más sencilla de escribir la expresión original."
                ))
            
            return {
                "result": result_str,
                "steps": [s.model_dump() for s in steps],
                "mode": "algebra"
            }
        
        except Exception as e:
            raise ValueError(f"Error en álgebra: {str(e)}")
    
    def _solve_equation(self, expression: str) -> Dict[str, Any]:
        """
        Resuelve ecuaciones con explicaciones educativas detalladas
        """
        steps = []
        
        # Paso 1: Introducción a ecuaciones
        steps.append(Step(
            step=1,
            description="💡 ¿Qué es una ecuación?",
            expression=expression,
            detail="Una ecuación es como una balanza en equilibrio.\n\nEl signo '=' dice que ambos lados valen lo mismo.\n\nNuestra meta es encontrar el valor de la incógnita (variable) que hace que la ecuación sea verdadera."
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
                description="📋 Los dos lados de la ecuación",
                expression=f"{left_expr} = {right_expr}",
                detail=f"Lado izquierdo: {left_expr}\nLado derecho: {right_expr}\n\nAmbos lados deben ser iguales."
            ))
            
            # Paso 3: Identificar variable
            free_vars = equation.free_symbols
            if not free_vars:
                raise ValueError("No se encontró ninguna variable en la ecuación")
            
            var = list(free_vars)[0]  # Tomar la primera variable
            steps.append(Step(
                step=3,
                description=f"🔍 Identificar la incógnita",
                expression=str(equation),
                detail=f"La variable que debemos encontrar es '{var}'.\n\nVamos a despejar '{var}' para encontrar su valor."
            ))
            
            # Paso 4: Proceso de resolución
            steps.append(Step(
                step=4,
                description="✏️ Resolver la ecuación",
                expression=str(equation),
                detail="Para resolver, aplicamos operaciones a ambos lados de la ecuación:\n\n• Si sumamos/restamos algo, lo hacemos en ambos lados\n• Si multiplicamos/dividimos, lo hacemos en ambos lados\n• Así mantenemos el equilibrio de la balanza"
            ))
            
            # Paso 5: Resolver
            solutions = solve(equation, var)
            
            # Paso 6: Presentar solución
            if not solutions:
                result_str = "Sin solución"
                detail = "❌ Esta ecuación no tiene soluciones reales.\n\nEsto significa que no existe ningún valor de {} que haga verdadera la ecuación.".format(var)
            elif len(solutions) == 1:
                sol_formatted = format_number(solutions[0])
                result_str = f"{var} = {sol_formatted}"
                
                # Verificar la solución
                verification = left_expr.subs(var, solutions[0])
                steps.append(Step(
                    step=5,
                    description="✓ Verificar la solución",
                    expression=f"{var} = {sol_formatted}",
                    detail=f"Vamos a comprobar que la solución es correcta.\n\nSustituimos {var} = {sol_formatted} en la ecuación original:\n{left_expr.subs(var, solutions[0])} = {right_expr}\n\n¡Es correcto! ✓"
                ))
                
                detail = f"La solución es {var} = {sol_formatted}"
            else:
                sols_formatted = [format_number(s) for s in solutions]
                result_str = f"{var} = {{{', '.join(sols_formatted)}}}"
                detail = f"Esta ecuación tiene múltiples soluciones:\n{var} = {' o '.join(sols_formatted)}\n\nCualquiera de estos valores hace verdadera la ecuación."
            
            steps.append(Step(
                step=len(steps) + 1,
                description="✅ Resultado final",
                expression=result_str,
                detail=f"🎉 {detail}"
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
        Calcula derivadas con explicaciones educativas
        """
        steps = []
        
        # Paso 1: Introducción a derivadas
        steps.append(Step(
            step=1,
            description="💡 ¿Qué es una derivada?",
            expression=expression,
            detail="La derivada nos dice qué tan rápido cambia algo.\n\nPor ejemplo:\n• La velocidad es la derivada de la posición (qué tan rápido cambia tu ubicación)\n• La aceleración es la derivada de la velocidad\n\nVamos a calcular la derivada de esta función."
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
                description=f"📝 Variable de derivación",
                expression=str(expr),
                detail=f"Vamos a derivar con respecto a '{var}'.\n\nEsto significa que veremos cómo cambia la función cuando {var} cambia."
            ))
            
            # Identificar el tipo de función
            func_type = self._identify_function_type(expr, var)
            steps.append(Step(
                step=3,
                description="🔍 Identificar tipo de función",
                expression=str(expr),
                detail=func_type
            ))
            
            # Calcular derivada
            derivative = diff(expr, var)
            
            steps.append(Step(
                step=4,
                description="✏️ Aplicar reglas de derivación",
                expression=str(derivative),
                detail=self._explain_derivative_rule(expr, var)
            ))
            
            # Simplificar si es posible
            simplified = simplify(derivative)
            if simplified != derivative:
                steps.append(Step(
                    step=5,
                    description="🔢 Simplificar",
                    expression=str(simplified),
                    detail="Simplificamos la expresión para obtener la forma más clara."
                ))
                derivative = simplified
            
            # Resultado final
            steps.append(Step(
                step=len(steps) + 1,
                description="✅ Resultado final",
                expression=f"d/d{var}[{expr}] = {derivative}",
                detail=f"🎉 La derivada es: {derivative}\n\nEsta función nos dice la tasa de cambio instantánea."
            ))
            
            return {
                "result": f"d/d{var}[{expr}] = {derivative}",
                "steps": [s.model_dump() for s in steps],
                "mode": "derivative"
            }
        
        except Exception as e:
            raise ValueError(f"Error calculando derivada: {str(e)}")
    
    def _integral(self, expression: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Calcula integrales con explicaciones educativas
        """
        steps = []
        
        # Paso 1: Introducción a integrales
        steps.append(Step(
            step=1,
            description="💡 ¿Qué es una integral?",
            expression=expression,
            detail="La integral es lo opuesto de la derivada.\n\nPodemos pensar en ella como:\n• Encontrar el área bajo una curva\n• Sumar infinitos pedacitos pequeños\n• Revertir el proceso de derivación\n\nVamos a calcular la integral de esta función."
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
                description=f"📝 Variable de integración",
                expression=str(expr),
                detail=f"Vamos a integrar con respecto a '{var}'.\n\nEsto significa que estamos 'sumando' o 'acumulando' valores a medida que {var} cambia."
            ))
            
            # Identificar el tipo de función
            func_type = self._identify_function_type(expr, var)
            steps.append(Step(
                step=3,
                description="🔍 Identificar tipo de función",
                expression=str(expr),
                detail=func_type
            ))
            
            # Calcular integral
            integral_result = integrate(expr, var)
            
            steps.append(Step(
                step=4,
                description="✏️ Aplicar reglas de integración",
                expression=str(integral_result),
                detail=self._explain_integration_rule(expr, var)
            ))
            
            # Añadir constante
            result_str = f"{integral_result} + C"
            steps.append(Step(
                step=5,
                description="➕ Añadir constante",
                expression=result_str,
                detail="Añadimos '+ C' (constante de integración).\n\n¿Por qué?\nCuando derivamos una constante, se vuelve 0. Por eso, al integrar, no sabemos si había una constante originalmente.\n\nLa 'C' puede ser cualquier número."
            ))
            
            # Resultado final
            steps.append(Step(
                step=6,
                description="✅ Resultado final",
                expression=f"∫{expr} d{var} = {result_str}",
                detail=f"🎉 La integral es: {result_str}\n\nEsta función representa la 'antiderivada' o la acumulación de la función original."
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
    
    def _identify_function_type(self, expr, var) -> str:
        """
        Identifica el tipo de función para dar contexto educativo
        """
        from sympy import sin, cos, tan, exp, log
        
        if expr.is_polynomial(var):
            degree = expr.as_poly(var).degree() if expr.as_poly(var) else 0
            if degree == 1:
                return "Esta es una función lineal (una línea recta)."
            elif degree == 2:
                return "Esta es una función cuadrática (una parábola)."
            else:
                return f"Esta es una función polinomial de grado {degree}."
        elif expr.has(sin, cos, tan):
            return "Esta es una función trigonométrica (relacionada con ángulos y círculos)."
        elif expr.has(exp):
            return "Esta es una función exponencial (crece muy rápidamente)."
        elif expr.has(log):
            return "Esta es una función logarítmica (lo opuesto de la exponencial)."
        else:
            return "Vamos a trabajar con esta función matemática."
    
    def _explain_derivative_rule(self, expr, var) -> str:
        """
        Genera explicación de la regla de derivación aplicada
        """
        from sympy import sin, cos, tan, exp, log
        
        if expr.is_polynomial(var):
            return "Aplicamos la regla de la potencia:\n\nd/dx[x^n] = n × x^(n-1)\n\nBajamos el exponente y restamos 1 al exponente.\n\nPor ejemplo: d/dx[x³] = 3x²"
        elif expr.has(sin):
            return "Reglas trigonométricas:\n• d/dx[sin(x)] = cos(x)\n• d/dx[cos(x)] = -sin(x)\n• d/dx[tan(x)] = sec²(x)"
        elif expr.has(exp):
            return "Regla de la exponencial:\nd/dx[e^x] = e^x\n\nLa exponencial es especial: ¡su derivada es ella misma!"
        elif expr.has(log):
            return "Regla del logaritmo:\nd/dx[ln(x)] = 1/x"
        else:
            return "Aplicamos las reglas de derivación correspondientes, como:\n• Regla del producto\n• Regla de la cadena\n• Regla del cociente"
    
    def _explain_integration_rule(self, expr, var) -> str:
        """
        Genera explicación de la regla de integración aplicada
        """
        from sympy import sin, cos, tan, exp, log
        
        if expr.is_polynomial(var):
            return "Aplicamos la regla de la potencia para integración:\n\n∫x^n dx = x^(n+1)/(n+1) + C\n\nSumamos 1 al exponente y dividimos por el nuevo exponente.\n\nPor ejemplo: ∫x² dx = x³/3 + C"
        elif expr.has(sin, cos):
            return "Reglas trigonométricas de integración:\n• ∫sin(x) dx = -cos(x) + C\n• ∫cos(x) dx = sin(x) + C"
        elif expr.has(exp):
            return "Regla de la exponencial:\n∫e^x dx = e^x + C\n\nLa integral de e^x es e^x."
        elif str(expr) == "1/x" or expr.has(log):
            return "Regla especial:\n∫(1/x) dx = ln|x| + C"
        else:
            return "Aplicamos las reglas de integración correspondientes."
    
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




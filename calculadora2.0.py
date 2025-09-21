import tkinter as tk
import math
import random

# Variables globales para los modos
modo_f1_activo = False
modo_f2_activo = False
modo_f3_activo = False

# Diccionario para mapear botones a sus dígitos originales
botones_originales = {}

# Función factorial personalizada
def factorial(n):
    if n < 0:
        raise ValueError("Factorial no definido para números negativos")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, int(n) + 1):
        result *= i
    return result

def on_click(event):
    global modo_f1_activo, modo_f2_activo, modo_f3_activo, ultimo_resultado
    
    current_text = entry.get()
    button = event.widget
    button_text = button.cget("text")
    
    # Obtener el dígito original del botón
    digito_original = botones_originales.get(button, button_text)
    
    # Manejo de botones F1, F2 y F3 (toggle)
    if button_text == "F1":
        modo_f1_activo = not modo_f1_activo
        modo_f2_activo = False
        modo_f3_activo = False
        actualizar_estado_modos()
        actualizar_texto_botones()
        return
        
    if button_text == "F2":
        modo_f2_activo = not modo_f2_activo
        modo_f1_activo = False
        modo_f3_activo = False
        actualizar_estado_modos()
        actualizar_texto_botones()
        return
        
    if button_text == "F3":
        modo_f3_activo = not modo_f3_activo
        modo_f1_activo = False
        modo_f2_activo = False
        actualizar_estado_modos()
        actualizar_texto_botones()
        return
    
    if button_text == "=":
        try:
            # Preprocesar la expresión antes de evaluar
            expresion_procesada = preprocesar_expresion(current_text)
            result = eval(expresion_procesada, {"math": math, "factorial": factorial})
            entry.delete(0, tk.END)
            # Formatear el resultado para números muy grandes o muy pequeños
            if isinstance(result, float) and (abs(result) > 1e10 or abs(result) < 1e-10):
                entry.insert(tk.END, f"{result:.10e}")
            else:
                entry.insert(tk.END, str(result))
            ultimo_resultado = result  # Guardar el último resultado
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    
    elif button_text == "C":
        entry.delete(0, tk.END)  # Borra todo
        # Si estaba en modo especial, volver a mostrar números
        if modo_f1_activo or modo_f2_activo or modo_f3_activo:
            modo_f1_activo = False
            modo_f2_activo = False
            modo_f3_activo = False
            actualizar_estado_modos()
            actualizar_texto_botones()
    
    elif button_text == "CE":
        # Borra solo el último carácter
        if current_text:
            entry.delete(len(current_text) - 1, tk.END)
    
    else:
        # Determinar qué texto insertar según el modo activo
        texto_a_insertar = button_text
        
        if modo_f1_activo and digito_original in obtener_funcion_f1_keys():
            texto_a_insertar = obtener_funcion_f1(digito_original)
        elif modo_f2_activo and digito_original in obtener_funcion_f2_keys():
            texto_a_insertar = obtener_funcion_f2(digito_original)
        elif modo_f3_activo and digito_original in obtener_funcion_f3_keys():
            texto_a_insertar = obtener_funcion_f3(digito_original)
        
        # Insertar el texto y desactivar modos especiales
        entry.insert(tk.END, texto_a_insertar)
        
        # Después de insertar una función, volver al modo normal (números)
        if modo_f1_activo or modo_f2_activo or modo_f3_activo:
            modo_f1_activo = False
            modo_f2_activo = False
            modo_f3_activo = False
            actualizar_estado_modos()
            actualizar_texto_botones()

def obtener_funcion_f1(digito):
    funciones_f1 = {
        "7": "(",
        "8": ")",
        "9": "^2",
        "4": "1/",
        "5": "10^",
        "6": "(-)",
        "1": "π",
        "2": "e",
        "3": "rand()",
        "0": "ANS"
    }
    return funciones_f1.get(digito, digito)

def obtener_funcion_f2(digito):
    funciones_f2 = {
        "7": "sin(",
        "8": "cos(",
        "9": "tan(",
        "4": "asin(",
        "5": "acos(",
        "6": "atan(",
        "1": "log(",
        "2": "ln(",
        "3": "√(",
        "0": "∛("
    }
    return funciones_f2.get(digito, digito)

def obtener_funcion_f3(digito):
    funciones_f3 = {
        "7": "!(",
        "8": "abs(",
        "9": "round(",
        "4": "mod(",
        "5": "rad(",
        "6": "deg(",
        "1": "sinh(",
        "2": "cosh(",
        "3": "tanh(",
        "0": "e^("
    }
    return funciones_f3.get(digito, digito)

def obtener_nombre_funcion_f1(digito):
    nombres_f1 = {
        "7": "(",
        "8": ")",
        "9": "x²",
        "4": "1/x",
        "5": "10ˣ",
        "6": "±",
        "1": "π",
        "2": "e",
        "3": "rand",
        "0": "ANS"
    }
    return nombres_f1.get(digito, digito)

def obtener_nombre_funcion_f2(digito):
    nombres_f2 = {
        "7": "sin",
        "8": "cos",
        "9": "tan",
        "4": "asin",
        "5": "acos",
        "6": "atan",
        "1": "log",
        "2": "ln",
        "3": "√",
        "0": "∛"
    }
    return nombres_f2.get(digito, digito)

def obtener_nombre_funcion_f3(digito):
    nombres_f3 = {
        "7": "!",
        "8": "abs",
        "9": "round",
        "4": "mod",
        "5": "rad",
        "6": "deg",
        "1": "sinh",
        "2": "cosh",
        "3": "tanh",
        "0": "eˣ"
    }
    return nombres_f3.get(digito, digito)

def obtener_funcion_f1_keys():
    return ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0"]

def obtener_funcion_f2_keys():
    return ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0"]

def obtener_funcion_f3_keys():
    return ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0"]

def preprocesar_expresion(expresion):
    # Reemplazar funciones y constantes por sus equivalentes en math
    reemplazos = {
        "sin(": "math.sin(",
        "cos(": "math.cos(",
        "tan(": "math.tan(",
        "asin(": "math.asin(",
        "acos(": "math.acos(",
        "atan(": "math.atan(",
        "sinh(": "math.sinh(",
        "cosh(": "math.cosh(",
        "tanh(": "math.tanh(",
        "log(": "math.log10(",
        "ln(": "math.log(",
        "π": "math.pi",
        "e": "math.e",
        "√(": "math.sqrt(",
        "∛(": "math.pow(",  # Se manejará aparte
        "e^(": "math.exp(",
        "10^": "10**",
        "^2": "**2",
        "rad(": "math.radians(",
        "deg(": "math.degrees(",
        "abs(": "abs(",
        "round(": "round(",
        "mod(": "math.fmod(",
        "(-)": "-",
        "1/": "1/",
        "rand()": str(random.random()),
        "ANS": str(ultimo_resultado) if 'ultimo_resultado' in globals() else "0"
    }
    
    # Aplicar reemplazos
    for original, reemplazo in reemplazos.items():
        expresion = expresion.replace(original, reemplazo)
    
    # Manejar raíz cúbica (∛)
    while "math.pow(" in expresion:
        idx = expresion.find("math.pow(")
        if idx >= 0:
            # Encontrar la coma y reemplazar por ", 1/3)"
            end_idx = expresion.find(",", idx)
            if end_idx > 0:
                expresion = expresion[:end_idx] + ", 1/3)" + expresion[end_idx+1:]
    
    # Manejar factorial (!)
    while "!(" in expresion:
        idx = expresion.find("!(")
        if idx > 0:
            # Encontrar el número antes del !
            inicio_num = idx - 1
            while inicio_num >= 0 and (expresion[inicio_num].isdigit() or expresion[inicio_num] == '.' or expresion[inicio_num] == '-'):
                inicio_num -= 1
            inicio_num += 1
            
            numero = expresion[inicio_num:idx]
            try:
                fact_result = factorial(float(numero))
                expresion = expresion[:inicio_num] + str(fact_result) + expresion[idx+2:]
            except:
                # Si hay error, reemplazar por multiplicación
                expresion = expresion.replace("!(", "*(")
    
    # Asegurar que todos los paréntesis estén balanceados
    parentesis_abiertos = expresion.count('(')
    parentesis_cerrados = expresion.count(')')
    if parentesis_abiertos > parentesis_cerrados:
        expresion += ')' * (parentesis_abiertos - parentesis_cerrados)
    
    return expresion

def actualizar_estado_modos():
    # Cambiar color de los botones F1, F2 y F3 según su estado
    color_f1 = "light yellow" if modo_f1_activo else "SystemButtonFace"
    color_f2 = "light green" if modo_f2_activo else "SystemButtonFace"
    color_f3 = "light blue" if modo_f3_activo else "SystemButtonFace"
    
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            if widget.cget("text") == "F1":
                widget.config(bg=color_f1)
            elif widget.cget("text") == "F2":
                widget.config(bg=color_f2)
            elif widget.cget("text") == "F3":
                widget.config(bg=color_f3)

def actualizar_texto_botones():
    # Actualizar el texto de los botones numéricos según el modo activo
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget in botones_originales:
            texto_original = botones_originales[widget]
            if modo_f1_activo:
                widget.config(text=obtener_nombre_funcion_f1(texto_original))
            elif modo_f2_activo:
                widget.config(text=obtener_nombre_funcion_f2(texto_original))
            elif modo_f3_activo:
                widget.config(text=obtener_nombre_funcion_f3(texto_original))
            else:
                # Volver a mostrar los números
                widget.config(text=texto_original)

# Variable global para el último resultado
ultimo_resultado = 0

# Crear una ventana
root = tk.Tk()
root.title("Calculadora Científica Karol")

# Crear una caja de entrada (Entry)
entry = tk.Entry(root, font=("Helvetica", 20))
entry.grid(row=0, column=0, columnspan=6, sticky="ew")  # Aumentado a 6 columnas

# Lista de botones
buttons = [
    "F1", "F2", "F3", "CE", "C", "√",
    "7", "8", "9", "/", "^", "(",
    "4", "5", "6", "*", ")",
    "1", "2", "3", "-", "π", "e",
    "0", ".", "=", "+"
]

# Crear y colocar los botones en la ventana
row = 1
col = 0
for button_text in buttons:
    button = tk.Button(root, text=button_text, font=("Helvetica", 14), padx=10, pady=10)
    
    # Guardar el texto original del botón
    botones_originales[button] = button_text
    
    # Hacer que los botones de función ocupen más espacio
    if button_text in ["F1", "F2", "F3"]:
        button.grid(row=row, column=col, columnspan=2, sticky="nsew")
        col += 1  # Avanzar una columna extra
    else:
        button.grid(row=row, column=col, sticky="nsew")
    
    button.bind("<Button-1>", on_click)
    col += 1
    
    if col >= 6:  # Ahora tenemos 6 columnas
        col = 0
        row += 1

# Configurar el redimensionamiento de la ventana
for i in range(6):  # Ahora 6 columnas
    root.grid_columnconfigure(i, weight=1)
for i in range(row + 1):
    root.grid_rowconfigure(i, weight=1)

# Inicializar el estado de los modos
actualizar_estado_modos()

# Ejecutar el bucle principal
root.mainloop()
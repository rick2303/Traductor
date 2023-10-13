import ply.lex as lex
import ply.yacc as yacc
import re
import random

# Definición de tokens
tokens = [
    'NUMBER',
    'CONVERSION',
    'END'
]

# Expresiones regulares para tokens
t_CONVERSION = r'Hexadecimal|Octal|Binario|Romano|Aleatorio'
t_END = r'\$'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.lexer.lineno = t.lineno
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores
def t_error(t):
    print("Error léxico: Caracter no válido '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Definición de la gramática
def p_expression(p):
    '''expression : NUMBER CONVERSION END'''
    p[0] = (p[1], p[2])

# Manejo de errores sintácticos
def p_error(p):
    print("Error sintáctico en la entrada")

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Función para realizar la conversión a números romanos
def int_to_roman(n):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

# Función para realizar la conversión a binario
def int_to_bin(n):
    return bin(n)[2:]

# Función para realizar la conversión a octal
def int_to_oct(n):
    return oct(n)[2:]

# Función para realizar la conversión a hexadecimal
def int_to_hex(n):
    return hex(n)[2:].upper()

# Función para realizar las conversiones
def do_conversion(number, conversion):
    if conversion == 'Binario':
        return int_to_bin(number)
    elif conversion == 'Octal':
        return int_to_oct(number)
    elif conversion == 'Hexadecimal':
        return int_to_hex(number)
    elif conversion == 'Romano':
        return int_to_roman(number)
    elif conversion == 'Aleatorio':
        conversion_options = ['Binario', 'Octal', 'Hexadecimal', 'Romano']
        chosen_conversion = random.choice(conversion_options)
        return do_conversion(number, chosen_conversion)

# Función principal
def main():
    input_string = "525Hexadecimal$"
    lexer.input(input_string)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    try:
        parsed_data = parser.parse(input_string)
        number, conversion = parsed_data
        result = do_conversion(number, conversion)
        print("Cadena:", input_string, "=> Salida:", result)
        print("Detalle del análisis léxico:")
        for token in tokens:
            print(f"Línea: {token.lineno}, Tipo: {token.type}, Valor: {token.value}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

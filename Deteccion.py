def DefinirTipo(cadena):
    try:
        return int(cadena)
    except:
        pass
    try:
        return float(cadena)
    except:
        pass
    return cadena


delimitador = input('Escriba el delimitador. ej. , (coma):')
#delimitar = ' '
#cadena = '1 225 b 3 c -4 d 5.25 e'
cadena = input('Escriba la cadena a procesar:')
numeros = []
letras = []
cadenas = []

strings = cadena.split(delimitador)

for string in strings:
    dato = DefinirTipo(string)
    tipo = type(dato)
    if tipo is int or tipo is float:
        numeros.append(dato)
    else:
        if len(string) == 1:
            letras.append(string)
        else:
            cadenas.append(string)

print('La cadena "' + cadena + '" contiene:')
print('\tNingún número' if len(numeros) == 0 else '\t' + str(len(numeros)) + ' números, los cuales son: ' + str(numeros))
print('\tNingún caracter' if len(letras) == 0 else '\t' + str(len(letras)) + ' carácteres, las cuales son: ' + str(letras))
print('\tNinguna cadena' if len(cadenas) == 0 else '\t' + str(len(cadenas)) + ' cadenas, las cuales son: ' + str(cadenas))


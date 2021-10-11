import sys


def MostrarOpciones():
    print('\t*/*/*/*/*/* Menú \t*/*/*/*/*/*')
    print('Escriba la opción del ejercicio que desee hacer: \n\t1) Operación aritmética\n\t2) Operación lógica\n\t3) Separación dada una cadena\n\t4) Salir')
    try:
        return int(input('Opción:'))
    except:
        print('Opción no disponile, reintente...\n')
        return 0
    pass


def RealizarEjercicio(opcion):
    if opcion == 1:
        mod = __import__('PrologPy')
        input('Presione Enter para continuar...\n')
        del mod
        sys.modules.pop('PrologPy')
    elif opcion == 2:
        mod = __import__('OperacionLogica')
        input('Presione Enter para continuar...\n')
        del mod
        sys.modules.pop('OperacionLogica')
    elif opcion == 3:
        mod = __import__('Deteccion')
        input('Presione Enter para continuar...\n')
        del mod
        sys.modules.pop('Deteccion')


opcion = 0
while opcion < 4:
    opcion = MostrarOpciones()
    RealizarEjercicio(opcion)
    pass

print('\nBye (._.)/')
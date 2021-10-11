import re
import enum

#Arreglo de los operandos reconocibles
OPERANDOS = ['-', '+', '*', '/', '^']

#Clase que representa un nodo del árbol binario
class Nodo:
    #Valor del nodo
    valor = ''

    #Padre
    padre = None

    #Nodo/hoja derecha
    D = None

    #Nodo/hoja derecha
    I = None

    def __init__(self, valor, padre):
        self.valor = valor
        self.padre = padre

#Clase que contiene los operadores, lo cuales están relacionados con un índice, que a la vez demuestra su valor de precedencia
class Operandos(enum.Enum):
    Ninguno = 0
    SumRest = 1
    ProdDiv = 2
    Potencia = 3
    Maximo = 100

class GrupoOperaciones:
    startIndex = 0
    endIndex = 0
    cadena = ''
    esCandidato = False
    def __init__(self, start, end, cadena, candidato):
        self.startIndex = start
        self.endIndex = end
        self.cadena = cadena
        self.esCandidato = candidato


def ObtenerOperando(char : str):
    if char == '+' or char == '-':
        return Operandos.SumRest
    elif char == '*' or char == '/':
        return Operandos.ProdDiv
    elif char == '^':
        return Operandos.Potencia
    else:
        return Operandos.Ninguno


def ContieneOperando(cadena):
    counter = 0
    for operando in OPERANDOS:
        counter += cadena.count(operando)
    #return len([x for x in OPERANDOS if x in cadena])
    return counter

def ConteoParentesis(cadena):
    counter = 0
    parentesis = ['(', ')']
    for parentesi in parentesis:
        counter += cadena.count(parentesi)
    #return len([x for x in OPERANDOS if x in cadena])
    return counter

def EliminarParentesis(cadena, multiple):
    if multiple is True:
        return re.split('; |, |\(|\)', cadena)
    else:
        # return re.split('; |, |\(|\)', cadena)[0]
        cadena = cadena.replace('(', '')
        cadena = cadena.replace(')', '')
        return cadena
    pass


def CorregirExpresion(cadena : str):
    #Eliminar espacios
    cadena = cadena.replace(' ', '')
    #Corregir multipliación antes de abrir parentesis "2( -> 2*("
    matches = [(i, cadena[i: i + 2]) for i in BuscarCaracter('(', cadena)]
    offset = 0
    for match in matches:
        index = match[0] + offset
        if index > 0:
            if cadena[index - 1: index].isdigit() is True:
                cadena = cadena[: index] + '*' + cadena[index:]
                offset += 1

    #Corregir multiplicaciones en cierre de parentesis ")2 -> )*2"
    offset = 0
    matches = [(i, cadena[i: i + 2]) for i in BuscarCaracter(')', cadena)]
    for match in matches:
        index = match[0] + 1 + offset
        if index < len(cadena):
            if cadena[index: index + 1].isdigit() == True or cadena[index: index + 1] == '(':
                cadena = cadena[:index] + '*' + cadena[index:]
                offset += 1

    #Corregir puntos decimales
    matches = [(i, cadena[i: i + 2]) for i in BuscarCaracter('.', cadena)]
    offset = 0
    for match in matches:
        index = match[0] + 1 + offset
        if index < len(cadena):
            if cadena[index: index + 1].isdigit() == False or cadena[index: index + 1] == '(':
                cadena = cadena[:index] + '0' + cadena[index:]
                offset += 1
        else:
            cadena = cadena + '0'

    #Encapsular negativos
    # matches = [(i, cadena[i: i + 2]) for i in BuscarCaracter('-', cadena)]
    # offset = 0
    # for match in matches:
    #     index = match[0] + offset
    #     if index - 1 >= 0:
    #         #and cadena[index - 1 : index] is not '(' and cadena[index - 1 : index] is not ')':
    #         if cadena[index - 1 : index].isdigit() is not True:
    #             print('Negativo: ' + cadena[index - 1 : index])
    #             numberoffset = index + 1
    #             for x in range(index + 1, len(cadena)):
    #                 if cadena[x].isdigit() is not True and cadena[x] is not '.':
    #                     break
    #                 numberoffset += 1
    #             cadena = cadena[:index] + '(' + cadena[index:numberoffset] + ')' + cadena[numberoffset:]
    #             offset += 2
    #     else:
    #         #print('Negativo: ' + cadena[: index + 1])
    #         numberoffset = index + 1
    #         for x in range(index + 1, len(cadena)):
    #             if cadena[x].isdigit() is not True and cadena[x] is not '.':
    #                 break
    #             numberoffset += 1
    #         cadena = '(' + cadena[:numberoffset] + ')' + cadena[numberoffset:]
    #         offset += 2
    return cadena


def BuscarCaracter(operando, cadena):
    i = cadena.find(operando)
    while i != -1:
        yield i
        i = cadena.find(operando, i + 1)

#Devuelve el índice del menor operador y una lista de los operadores de cada operacion
def SeleccionarMenorPrecedencia(operaciones):
    #Asignar la mayor precedencia
    tmp = Operandos.Maximo
    i = 0
    menorIndex = 0
    menorOperador = ''

    #Lista de la lista de operadores por operaciones
    operadoresDeOperaciones = []

    #Recorrer todas las operaciones
    for operacion in operaciones:

        #Si la operación no está fuera de todos los parentesis se omite
        if operacion.esCandidato is False:
            i += 1
            continue

        matches = []

        #Recorrer los operadores para encontrar todos los que existan en la operación
        for operando in OPERANDOS:
            #Verificar primero si existe el operando en la operación, sino seguir al siguiente
            if operando not in operacion.cadena:
                continue

            #Encontrar el operador actual con comprensión de listas y un método que busca el operando en la operación,
            # devuelve una lista con todos los operando existentes
            match = [operacion.cadena[i: i + 1] for i in BuscarCaracter(operando, operacion.cadena)]
            matches.extend(match)

        #Agregar los operadores encontrados de esta operacion
        operadoresDeOperaciones.append(matches)

        #Se obtiene la precedencia del índice cera, ya que es el que menor valor de precendecia tiene
        menorPrecedencia = ObtenerOperando(matches[0])

        #Si el operador tiene menor precedencia que el de otra operación, se asigna como operación con menor
        # precedencia
        if menorPrecedencia.value < tmp.value:
            tmp = menorPrecedencia
            menorIndex = i
            menorOperador = matches[0]

        i += 1

    return menorIndex, menorOperador, operadoresDeOperaciones


def ResolverRama(expresion, nodo, msj = '', mostrarPasos = False):
    print('**********Nueva hoja**************** Padre: ' + (nodo.valor if nodo is not None else 'Raiz') + ' ' + msj) if mostrarPasos is True else None
    ops = ContieneOperando(expresion)
    if ops == 0:
        expresion = EliminarParentesis(expresion, False)
        print('Se obtuvo: ' + expresion + ' como última hoja') if mostrarPasos is True else None
        return Nodo(expresion, nodo)
    elif ops == 1:
        if '-' in expresion:
            expresion = EliminarParentesis(expresion, False)
            try:
                expresion = str(float(expresion))
                print('Se obtuvo: ' + expresion + ' como última hoja') if mostrarPasos is True else None
                return Nodo(expresion, nodo)
            except:
                pass


    print('Expresión original: ' + expresion) if mostrarPasos is True else None
    expresion = CorregirExpresion(expresion)
    print('Expresión corregida: ' + expresion) if mostrarPasos is True else None
    # Recorrer expresión para hallar la operación de menor precedencia
    parentesisAbierto = False
    i = 0
    startIndex = 0
    anidados = 0
    anidado = False

    operacion = None
    operaciones = []

    ops = ContieneOperando(expresion)
    print('La expresión ' + expresion + ' contiene ' + str(ops) + ' operaciones') if mostrarPasos is True else None
    if ops == 1:
        expresion = EliminarParentesis(expresion, False)
    # elif ops >= 2:
    #     print('Tienen pars: ')
    #     print(ConteoParentesis(expresion))
    #     if ConteoParentesis(expresion) == 1:
    #         expresion = EliminarParentesis(expresion, False)

    for char in expresion:
        if char == '(':
            if parentesisAbierto == True:
                anidados += 1
            else:
                parentesisAbierto = True
                startIndex = i
            pass

        elif char == ')':
            if parentesisAbierto == True:
                if anidados > 0:
                    anidados -= 1
                else:
                    parentesisAbierto = False
                    operaciones.append(GrupoOperaciones(startIndex, i, expresion[startIndex:i], False))

        i += 1

    print () if mostrarPasos else None

    opAnterior = None
    partes = []
    operacionesSinParentesis = []
    grupos = []

    si = 0
    ei = 0

    #Separar operaciones que estén dentro y fuera de parentesis
    for op in operaciones:

        # Obtener operaciones fuera de parentesis ) + operación + (
        if opAnterior is not None:
            si = opAnterior.endIndex
            ei = op.startIndex
            partes.append(expresion[si: ei])
            operacionesSinParentesis.append(expresion[si + 1: ei])
            grupos.append(
                GrupoOperaciones(si, ei, expresion[si: ei], True))
        else:
            ei = op.startIndex
            if op.startIndex > 0:
                partes.append(expresion[:ei])
                operacionesSinParentesis.append(expresion[:ei])
                grupos.append(GrupoOperaciones(0, ei, expresion[:ei], True))

        si = op.startIndex
        ei = op.endIndex
        partes.append(expresion[si:ei])
        grupos.append(GrupoOperaciones(si, ei, expresion[si: ei], False))
        opAnterior = op

    if opAnterior is not None and opAnterior.endIndex + 1 is not len(expresion):
        partes.append(expresion[opAnterior.endIndex:])
        operacionesSinParentesis.append(expresion[opAnterior.endIndex:])
        grupos.append(GrupoOperaciones(opAnterior.endIndex, len(expresion), expresion[opAnterior.endIndex:], True))

    if len(partes) == 0:
       partes.append(expresion)
       grupos.append(GrupoOperaciones(0, len(expresion), expresion, True))

    #print('Grupos: '+ str([x.cadena for x in grupos]))
    print('Grupo operaciones: ' + str(partes)) if mostrarPasos is True else None
    print('Operaciones a evaluar: ' + str(operacionesSinParentesis)) if mostrarPasos is True else None

    print() if mostrarPasos is True else None

    index, operadorADividir, listaOperandos = SeleccionarMenorPrecedencia(grupos)

    raiz: GrupoOperaciones = grupos[index]
    if raiz in grupos:
        print('La raiz es: ' + raiz.cadena + ' y está en el grupo con indice ' + str(grupos.index(raiz)) + ', se dividirá apartir del carácter: ' + operadorADividir)  if mostrarPasos is True else None

    nuevaExpresion = ''.join([x.cadena for x in grupos])
    hojaI = nuevaExpresion[:raiz.startIndex] + raiz.cadena[:raiz.cadena.index(operadorADividir)]
    hojaD = raiz.cadena[raiz.cadena.index(operadorADividir) + 1:] + nuevaExpresion[raiz.endIndex:]
    print('La expresión izquierda es: ' + hojaI) if mostrarPasos is True else None
    print('La expresión derecha es: ' + hojaD) if mostrarPasos is True else None

    #nodoRaiz = Nodo(operadorADividir, hojaD, hojaI, None)
    nuevoNodo = Nodo(operadorADividir, nodo)
    #print(operadorADividir)

    nuevoNodo.I = ResolverRama(hojaI, nuevoNodo, 'Rama izquierda', mostrarPasos)
    nuevoNodo.D = ResolverRama(hojaD, nuevoNodo, 'Rama derecha', mostrarPasos)

    return nuevoNodo
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

#From: https://stackoverflow.com/a/65865825
def print_tree(root, val="value", left="left", right="right"):
    def display(root, val=val, left=left, right=right):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, val)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(getattr(root, left))
        right, m, q, y = display(getattr(root, right))
        s = '%s' % getattr(root, val)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, *_ = display(root, val, left, right)
    for line in lines:
        print(line)

def Operar(operando1, operando2, operador):
    if operador == '+':
        return float(operando1) + float(operando2)
    elif operador == '-':
        return float(operando1) - float(operando2)
    elif operador == '*':
        return float(operando1) * float(operando2)
    elif operador == '/':
        return float(operando1) / float(operando2)
    elif operador == '^':
        return float(operando1) ** float(operando2)

def Postorden(nodo):
    orden = []
    if nodo is None:
        return orden
    orden.extend(Postorden(nodo.I))
    orden.extend(Postorden(nodo.D))
    orden.append(nodo.valor)
    return orden

def Inorden(nodo):
    orden = []
    if nodo is None:
        return orden
    orden.extend(Inorden(nodo.I))
    orden.append(nodo.valor)
    orden.extend(Inorden(nodo.D))
    return orden

def Preorden(nodo):
    orden = []
    if nodo is None:
        return orden
    orden.append(nodo.valor)
    orden.extend(Preorden(nodo.I))
    orden.extend(Preorden(nodo.D))
    return orden

def EsNumero(cadena):
    try:
        float(cadena)
        return True
    except:
        return False


expresion = input('Escriba la operación aritmética, ej. (6+2)*3/2^2-4:')

raiz = ResolverRama(expresion, None, '', False)

print_tree(raiz, 'valor', 'I', 'D')
print()

print('Operación: \t' + CorregirExpresion(expresion))
print('Preorden: \t' + str(', '.join(list(filter(None, Preorden(raiz))))))
print('Inorden: \t' + str(', '.join(list(filter(None, Inorden(raiz))))))

elementos = list(filter(None, Postorden(raiz)))
print('Postorden: \t' + ', '.join(elementos))

pila = []
for elemento in elementos:
    if EsNumero(elemento):
        pila.append(elemento)
    else:
        operando2 = pila.pop()
        operando1 = pila.pop()
        resultado = Operar(operando1, operando2, elemento)
        pila.append(resultado)

print()
print('Respuesta= \t' + str(pila))
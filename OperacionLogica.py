def Negacion(valor: bool):
    return not valor


def Conjuncion(a: bool, b: bool):
    return a is True and b is True


def Disyuncion(a: bool, b: bool):
    return Negacion(a is False and b is False)


def Condicional(a: bool, b: bool):
    return Negacion(a is True and b is False)


def Bicondicional(a : bool, b : bool):
    return a is True and b is True or a is False and b is False


def EsConector(char):
    return char == '∧' or char == '^' or char == '∨' or char == '|' or char == '>' or char == '¬' or char == '~'


def EsNegacion(char):
    return char == '¬' or char == '~'
def Operar(o1, o2, conector):
    newvars = []
    for i in range(len(o1)):
        if conector == '∧' or conector == '^':
            newvars.append(Conjuncion(o1[i], o2[i]))
        elif conector == '∨':
            newvars.append(Disyuncion(o1[i], o2[i]))
        elif  conector == '|':
            newvars.append(Bicondicional(o1[i], o2[i]))
        elif conector == '>':
            newvars.append(Condicional(o1[i], o2[i]))
    return newvars


def Verificar (vars):
    verdad = 0
    falsos = 0
    for x in vars:
        if x is True:
            verdad += 1
        else:
            falsos += 1

    if verdad == len(vars):
        return 'Es tautologia'
    elif falsos == len(vars):
        return 'Es contradicción'
    elif verdad != falsos or verdad == falsos:
        return 'Es contingencia'




def MostrarTabla(diccionario, nombres, total):
    msg = ''
    for var in diccionario:
        if var in nombres:
            msg += nombres[var] + '\t'
        else:
            msg += var + '\t'
    msg += '\n'

    for i in range(total):
        for var in diccionario:
            msg += str(diccionario[var][i]) + '\t'
        msg += '\n'

    # for var in diccionario:
    #     if var in nombres:
    #         msg = nombres[var] + ' = \t'
    #     else:
    #         msg = var + ' = \t'
    #     for x in diccionario[var]:
    #          msg += '\t' + str(x)
    #     msg += '\n'
    print(msg)
#∧∨
#proposicion = '[(p->q)^p]->q'
#proposicion = '¬(p^r)->(¬p->¬q)'
#proposicion = 'a|b->c'
proposicion = input('Escriba la operación lógica, ej. [(p->q)^p]->q:')
print('Proposición completa: ' + proposicion)
proposicion = proposicion.replace('<->', '|')
proposicion = proposicion.replace('->', '>')
print('Proposición corta: ' + proposicion)

pila = []
expresion = []
proposiciones = 0
string = ''

for i, char in enumerate(proposicion):
    if EsConector(char):
        if len(pila) > 0 and (pila[-1] == '¬' or pila[-1] == '~'):
            expresion.append(pila.pop())
        pila.append(char)
    elif char == '[' or char == '(':
        pila.append(char)
    elif char == ')' or char == ']':
        tmps = []
        while pila[-1] != '(' and pila[-1] != '[':
            tmps.append(pila.pop())
        pila.pop()
        expresion.extend(tmps)
    else:
        expresion.append(char)
        if char not in string:
            string += char
            proposiciones += 1

if (pila[-1] == '¬' or pila[-1] == '~') and len(pila) == 2:
    pila.reverse()

expresion.extend(pila)

casos = 2 ** proposiciones
total = casos
vars = {}
varnames = {}

for i, char in enumerate(string):
    casos = int(casos / 2)
    combinacion = []
    j = 0
    verdad = True
    while j < total:
        for k in range(casos):
            combinacion.append(verdad)
        verdad = not verdad
        j += casos

    vars[char] = combinacion

# print(vars)
print('Expresión postfija: ' + str(expresion))

pila.clear()
varcount = 0
for elemento in expresion:
    if EsConector(elemento) == False:
        pila.append(elemento)
    else:
        if not EsNegacion(elemento):
            operando2 = pila.pop()
            operando1 = pila.pop()
            #print('exp: '+ operando1+ str(elemento) + operando2)
            key = 'temp' + str(varcount)
            if operando1 in varnames:
                varnames[key] = '(' + varnames[operando1] + str(elemento) + operando2 + ')'
            else:
                varnames[key] = '(' + operando1 + str(elemento) + operando2 + ')'
            vars[key] = Operar(vars[operando1], vars[operando2], elemento)
            #print('Res: ' + key + ' = ' + str(vars[key]))
            pila.append(key)
            varcount += 1
        else:
            operando = pila.pop()
            #print('exp: ' + str(elemento) +  operando)
            key = 'temp' + str(varcount)
            if operando in varnames:
                varnames[key] = '(' + str(elemento) + varnames[operando] + ')'
            else:
                varnames[key] = '(' + str(elemento) + operando + ')'

            negacion = []
            for i in range(total):
                negacion.append(Negacion(vars[operando][i]))
            vars[key] = negacion
            #print('Res: ' + key + ' = ' + str(vars[key]))
            pila.append(key)
            varcount += 1

# print(vars)
print()
print('Tabla:')
MostrarTabla(vars, varnames, total)
print('La última columna es el resultado')
print(Verificar(list(vars.values())[-1]))

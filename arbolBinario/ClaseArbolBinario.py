from ClaseNodo import ClaseNodo
from collections import deque

class ArbolBinario:

    def __init__(self):
        self._raiz = None

    '''
    nota:inserta un nuevo valor en el árbol binario de búsqueda.
    argumentos: recibe un numero entero
    retorna: nada, pero actualiza la raíz del árbol. 
    '''

    def insertar(self, valor):
        self._raiz = self._insertarRecursivo(self._raiz, valor)

    '''
    nota: función auxiliar recursiva que busca la posición correcta
          e inserta el nuevo valor dentro del árbol binario de búsqueda.
    argumentos: 
        - raizAux: nodo actual (puede ser None si llegamos a un lugar vacío).
        - valor: número entero que se quiere insertar.
    retorna: 
        - un objeto ClaseNodo que representa la raíz del subárbol modificado.
    '''

    def _insertarRecursivo(self, raizAux, valor):
        #Caso Base
        if raizAux is None:
            raizAux = ClaseNodo(valor)
            return raizAux
        else:
            if valor < raizAux.getValor():
                raizAux.setHijoIzquierdo(self._insertarRecursivo(raizAux.getHijoIzquierdo(), valor))
            else:
                raizAux.setHijoDerecho(self._insertarRecursivo(raizAux.getHijoDerecho(), valor))
            return raizAux
    """
    Nota:Inserta un nuevo nodo en el árbol binario.
    Argumentos:
        valor: El valor que se desea insertar en el árbol.
    Retorna:
        None. (El método no retorna nada, solo modifica la estructura del árbol).
    """
    def insertarIterativo(self, valor):
        nuevoNodo = ClaseNodo(valor)
        if self._raiz is None:
            self._raiz = nuevoNodo
            return
        nodoActual = self._raiz
        while True:
            if valor < nodoActual.getValor():
                if nodoActual.getHijoIzquierdo() is None:
                    nodoActual.setHijoIzquierdo(nuevoNodo)
                    return
                nodoActual = nodoActual.getHijoIzquierdo()
            else:
                if nodoActual.getHijoDerecho() is None:
                    nodoActual.setHijoDerecho(nuevoNodo)
                    return
                nodoActual = nodoActual.getHijoDerecho()

                

    '''
    nota: verifica si el árbol está vacío.
    argumentos: ninguno.
    retorna: True si la raíz es None (árbol vacío), False en caso contrario.
    '''
    def isVacio(self):
        return self._raiz is None
    


    '''
    nota: determina si un nodo es hoja (no tiene hijos).
    argumentos: 
        - nodo: objeto de tipo ClaseNodo.
    retorna: True si el nodo no tiene hijos izquierdo ni derecho,
             False en caso contrario.
    '''
    def esHoja(self, nodo):
        return nodo.getHijoIzquierdo() == None and nodo.getHijoDerecho() == None
    

    """
    Nota:Busca un valor en el árbol binario de búsqueda.
    Argumentos:
        valor (int): El valor que se desea buscar en el árbol.
    Retorna:
        bool: True si el valor se encuentra en el árbol, False en caso contrario.
    """
    def buscar(self, valor):
        return self._buscarRecursivo(self._raiz, valor)
    
    """
    Nota:Función auxiliar recursiva para realizar la búsqueda en el árbol.
    Argumentos:
        nodo (ClaseNodo | None): El nodo actual del árbol desde donde se realiza la búsqueda.
        valor (int): El valor que se desea buscar.
    Retorna:
        bool: True si el valor está en el subárbol a partir del nodo dado,
              False si no se encuentra.
    """
    def _buscarRecursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.getValor() == valor:
            return True
        elif valor < nodo.getValor():
            return self._buscarRecursivo(nodo.getHijoIzquierdo(), valor)
        else:
            return self._buscarRecursivo(nodo.getHijoDerecho(), valor)
    
    """
    Nota:Busca un valor en el árbol binario de búsqueda de forma iterativa.
    Argumentos:
        valor (int): El valor que se desea buscar en el árbol.
    Retorna:
        bool: True si el valor se encuentra en el árbol, False en caso contrario.
    """
    def buscarIterativo(self, valor):
        nodoActual = self._raiz
        while nodoActual is not None:
            if nodoActual.getValor() == valor:
                return True
            elif valor < nodoActual.getValor():
                nodoActual = nodoActual.getHijoIzquierdo()
            else:
                nodoActual = nodoActual.getHijoDerecho()
        return False
    
    
    """
    nota:Recorre el árbol binario de búsqueda en orden (in-order) de manera iterativa.
    Retorna:
        list[int]: Una lista con los valores del árbol en orden ascendente.
    """
    def inOrden(self):
        listado = []
        pila = []
        nodoActual = self._raiz

        while nodoActual is not None or pila:
            while nodoActual is not None:
                pila.append(nodoActual)
                nodoActual = nodoActual.getHijoIzquierdo()

            nodoActual = pila.pop()
            listado.append(nodoActual.getValor())
            
            nodoActual = nodoActual.getHijoDerecho()

        return listado
    

    """
    Recorre el árbol binario de búsqueda en orden (in-order) de manera recursiva.
    Retorna:
        list[int]: Una lista con los valores del árbol en orden ascendente.
    """
    def inOrdenRecursivo(self):
        listado = []
        self._inOrdenRecursivoAux(self._raiz, listado)
        return listado
    
    """
    Función auxiliar recursiva para recorrer el árbol en orden.
    Argumentos:
        nodo (ClaseNodo | None): Nodo actual del recorrido.
        listado (list[int]): Lista en la que se almacenan los valores recorridos.
    Retorna:
        None. (Modifica la lista `listado` directamente).
    """
    def _inOrdenRecursivoAux(self, nodo, listado):
        if nodo is not None:
            self._inOrdenRecursivoAux(nodo.getHijoIzquierdo(), listado)
            listado.append(nodo.getValor())
            self._inOrdenRecursivoAux(nodo.getHijoDerecho(), listado)


    """
    Recorre el árbol binario de búsqueda en postorden (post-order) de manera iterativa.
    Retorna:
        list[int]: Una lista con los valores del árbol en orden postorden.
    """
    def posOrden(self):
        listado = []
        if self._raiz is None:
            return listado

        pila1 = [self._raiz]
        pila2 = []

        while pila1:
            nodo = pila1.pop()
            pila2.append(nodo)

            if nodo.getHijoIzquierdo() is not None:
                pila1.append(nodo.getHijoIzquierdo())
            if nodo.getHijoDerecho() is not None:
                pila1.append(nodo.getHijoDerecho())

        while pila2:
            listado.append(pila2.pop().getValor())

        return listado


    """
    Recorre el árbol binario de búsqueda en postorden (post-order) de manera recursiva.
    Retorna:
        list[int]: Una lista con los valores del árbol en orden postorden.
    """
    def posOrdenRecursivo(self):
        listado = []
        self._posOrdenRecursivoAux(self._raiz, listado)
        return listado
    """
    Función auxiliar recursiva para recorrer el árbol en postorden.
    Argumentos:
        nodo (ClaseNodo | None): Nodo actual del recorrido.
        listado (list[int]): Lista en la que se almacenan los valores recorridos.
    Retorna:
        None. (Modifica directamente la lista `listado`).
    """
    def _posOrdenRecursivoAux(self, nodo, listado):
        if nodo is not None:
            self._posOrdenRecursivoAux(nodo.getHijoIzquierdo(), listado)
            self._posOrdenRecursivoAux(nodo.getHijoDerecho(), listado)
            listado.append(nodo.getValor())


    """
    Recorre el árbol binario de búsqueda en preorden (pre-order) de manera iterativa.
    Retorna:
        list[int]: Una lista con los valores del árbol en orden preorden.
    """
    def preOrden(self):
        listado = []
        if self._raiz is None:
            return listado

        pila = [self._raiz]

        while pila:
            nodo = pila.pop()
            listado.append(nodo.getValor())

            if nodo.getHijoDerecho() is not None:
                pila.append(nodo.getHijoDerecho())
            if nodo.getHijoIzquierdo() is not None:
                pila.append(nodo.getHijoIzquierdo())

        return listado
    

    """
    Recorre el árbol binario de búsqueda en preorden (pre-order) de manera recursiva.
    Retorna:
        list[int]: Una lista con los valores del árbol en orden preorden.
    """
    def preOrdenRecursivo(self):
        listado = []
        self._preOrdenRecursivoAux(self._raiz, listado)
        return listado
    """
    Función auxiliar recursiva para recorrer el árbol en preorden.
    Argumentos:
        nodo (ClaseNodo | None): Nodo actual del recorrido.
        listado (list[int]): Lista en la que se almacenan los valores recorridos.
    Retorna:
        None. (Modifica directamente la lista `listado`).
    """
    def _preOrdenRecursivoAux(self, nodo, listado):
        if nodo is not None:
            listado.append(nodo.getValor())
            self._preOrdenRecursivoAux(nodo.getHijoIzquierdo(), listado)
            self._preOrdenRecursivoAux(nodo.getHijoDerecho(), listado)

    """
    Calcula la altura del árbol binario de búsqueda de manera recursiva.
    Retorna: (int) La altura del árbol.
    """
    
    def altura(self):
        return self._alturaAux(self._raiz)
    """
    Función auxiliar recursiva para calcular la altura del árbol.
    Argumentos: nodo (ClaseNodo | None): Nodo actual del recorrido.
    Retorna: (int) La altura del árbol.
    """
    def _alturaAux(self, nodo):
        if nodo is None:
            return 0
        altura_izquierda = self._alturaAux(nodo.getHijoIzquierdo())
        altura_derecha = self._alturaAux(nodo.getHijoDerecho())
        return 1 + max(altura_izquierda, altura_derecha)
    
    """
    Funcion iterativa para contar nodos
    Retorna: (int) La cantidad de nodos en el árbol.
    """
    def alturaIt(self):
        alturaDelArbol = 0
        if not self.isVacio():
            cola = deque([self._raiz])
            while cola:
                cantNodosEnLaCola = len(cola)
                for _ in range(cantNodosEnLaCola):
                    nodoAux = cola.popleft()
                    if nodoAux.getHijoIzquierdo() is not None:
                        cola.append(nodoAux.getHijoIzquierdo())
                    if nodoAux.getHijoDerecho() is not None:
                        cola.append(nodoAux.getHijoDerecho())
                alturaDelArbol += 1
        return alturaDelArbol


    """
    Funcion recursiva para contar nodos
    Retorna: (int) La cantidad de nodos en el árbol.
    """
    def cantidadNodos(self):
        return self._cantidadNodosAux(self._raiz)

    """
    Funcion auxiliar recursiva para contar nodos
    Argumentos: nodo (ClaseNodo | None): Nodo actual del recorrido.
    Retorna: (int) La cantidad de nodos en el árbol.
    """
    def _cantidadNodosAux(self, nodo):
        if nodo is None:
            return 0
        cantidad_izquierda = self._cantidadNodosAux(nodo.getHijoIzquierdo())
        cantidad_derecha = self._cantidadNodosAux(nodo.getHijoDerecho())
        return 1 + cantidad_izquierda + cantidad_derecha

    """
    Funcion iterativa para contar nodos
    Retorna: (int) La cantidad de nodos en el árbol.
    """
    def cantidadNodosIt(self):
        if self.isVacio():
            return 0
        cantidad = 0
        cola = deque([self._raiz])
        while cola:
            nodo = cola.popleft()
            cantidad += 1
            if nodo.getHijoIzquierdo() is not None:
                cola.append(nodo.getHijoIzquierdo())
            if nodo.getHijoDerecho() is not None:
                cola.append(nodo.getHijoDerecho())
        return cantidad


    """
    Realiza un recorrido por amplitud (nivel por nivel) del árbol binario.
    Retorna: (list[int]) Los valores de los nodos en el orden en que fueron visitados.
    """
    def amplitud(self):
        if self.isVacio():
            return []

        resultado = []
        cola = deque([self._raiz])

        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.getValor())

            if nodo.getHijoIzquierdo() is not None:
                cola.append(nodo.getHijoIzquierdo())
            if nodo.getHijoDerecho() is not None:
                cola.append(nodo.getHijoDerecho())

        return resultado


    """
    recorrido por niveles recursivo
    retorna: (list[int]) Los valores de los nodos en el orden en que fueron visitados.
    """
    def amplitudRecursivo(self):
        resultado = []
        h = self.altura() 

        for nivel in range(1, h + 1):
            self._amplitudRecursivoAux(self._raiz, nivel, resultado)

        return resultado
    """
    Funcion auxiliar para recorrer el árbol por niveles.
    Argumentos: nodo (ClaseNodo | None): Nodo actual del recorrido.
                nivel (int): Nivel actual del recorrido.
                resultado (list[int]): Lista para almacenar los valores de los nodos visitados.
    retorna: (list[int]) Los valores de los nodos en el orden en que fueron visitados.
    """
    def _amplitudRecursivoAux(self, nodo, nivel, resultado):
        if nodo is None:
            return
        if nivel == 1:
            resultado.append(nodo.getValor())
        elif nivel > 1:
            self._amplitudRecursivoAux(nodo.getHijoIzquierdo(), nivel - 1, resultado)
            self._amplitudRecursivoAux(nodo.getHijoDerecho(), nivel - 1, resultado)

    
    """
    Elimina un valor del árbol binario de búsqueda.
    Argumentos:
        valor (int): El valor a eliminar del árbol.
    Retorna:
        None. (El árbol se actualiza internamente).
    """
    def eliminar(self, valor):
        self._raiz = self._eliminarRecursivo(self._raiz, valor)

    """
    Función auxiliar recursiva para eliminar un nodo en el árbol.
    Argumentos:
        nodo (ClaseNodo | None): Nodo actual del recorrido.
        valor (int): El valor a eliminar.
    Retorna:
        ClaseNodo | None: La nueva referencia del subárbol después de la eliminación.
    """
    def _eliminarRecursivo(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.getValor():
            nodo.setHijoIzquierdo(self._eliminarRecursivo(nodo.getHijoIzquierdo(), valor))
        elif valor > nodo.getValor():
            nodo.setHijoDerecho(self._eliminarRecursivo(nodo.getHijoDerecho(), valor))
        else:
            # Caso 1: sin hijos
            if nodo.getHijoIzquierdo() is None and nodo.getHijoDerecho() is None:
                return None
            # Caso 2: un hijo
            elif nodo.getHijoIzquierdo() is None:
                return nodo.getHijoDerecho()
            elif nodo.getHijoDerecho() is None:
                return nodo.getHijoIzquierdo()
            # Caso 3: dos hijos
            else:
                sucesor = self._minValorNodo(nodo.getHijoDerecho())
                nodo.setValor(sucesor.getValor())
                nodo.setHijoDerecho(self._eliminarRecursivo(nodo.getHijoDerecho(), sucesor.getValor()))

        return nodo

    """
    Encuentra el nodo con el valor mínimo en un subárbol.
    Argumentos:
        nodo (ClaseNodo): Raíz del subárbol.
    Retorna:
        ClaseNodo: El nodo con el valor mínimo.
    """
    def _minValorNodo(self, nodo):
        actual = nodo
        while actual.getHijoIzquierdo() is not None:
            actual = actual.getHijoIzquierdo()
        return actual

    """
    Obtiene la raíz del árbol.
    Retorna: ClaseNodo | None: La raíz del árbol.
    """
    def getRaiz(self):
        return self._raiz
    
    def limpiarArbol(self):
        """Limpiar todo el árbol"""
        self._raiz = None

    def obtenerEstructuraVisual(self):
        """Obtener una representación visual simple del árbol"""
        if self.isVacio():
            return "Árbol vacío"
        return self._estructuraVisualRecursiva(self._raiz, "", True)

    def _estructuraVisualRecursiva(self, nodo, prefijo, esUltimo):
        if nodo is None:
            return ""
        
        resultado = prefijo + ("└── " if esUltimo else "├── ") + str(nodo.getValor()) + "\n"
        
        hijos = []
        if nodo.getHijoIzquierdo() is not None:
            hijos.append(("izq", nodo.getHijoIzquierdo()))
        if nodo.getHijoDerecho() is not None:
            hijos.append(("der", nodo.getHijoDerecho()))
        
        for i, (tipo, hijo) in enumerate(hijos):
            esUltimoHijo = i == len(hijos) - 1
            nuevoPrefijo = prefijo + ("    " if esUltimo else "│   ")
            resultado += self._estructuraVisualRecursiva(hijo, nuevoPrefijo, esUltimoHijo)
        
        return resultado

    

if __name__ == "__main__":
    arbol1 = ArbolBinario()
    arbol1.insertarIterativo(45)
    arbol1.insertarIterativo(23)
    arbol1.insertarIterativo(65)
    arbol1.insertarIterativo(2)
    arbol1.insertarIterativo(38)
    arbol1.insertarIterativo(52)
    arbol1.insertarIterativo(96)
    arbol1.insertarIterativo(7)
    arbol1.insertarIterativo(48)

    print("el arbol es vacio? = " , arbol1.isVacio())
    print(arbol1.buscar(99))
    print(arbol1.buscarIterativo(55))    
    print("recoridos iterativos")
    
    print(arbol1.inOrden())
    print(arbol1.posOrden())
    print(arbol1.preOrden())
    
    print("recorridos recursivos")

    print(arbol1.inOrdenRecursivo())   
    print(arbol1.posOrdenRecursivo())
    print(arbol1.preOrdenRecursivo())

    print("altura del arbol: ", arbol1.altura())
    print("altura del arbol (iterativa): ", arbol1.alturaIt())

    print("cantidad de nodos: ", arbol1.cantidadNodos())
    print("cantidad de nodos (iterativa): ", arbol1.cantidadNodosIt())

    print("amplitud del arbol: ", arbol1.amplitud())
    print("recorrido por niveles recursivo: ", arbol1.amplitudRecursivo())
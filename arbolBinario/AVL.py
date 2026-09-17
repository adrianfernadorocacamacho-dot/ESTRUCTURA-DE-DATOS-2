from ClaseNodo import ClaseNodo
from ClaseArbolBinario import ArbolBinario

class AVL(ArbolBinario):
    LIMITE_MAXIMO = 1

    '''
    nta: inserta un dato en el AVL, manteniendo el balance del árbol.
    argumentos: valor: número o dato a insertar en el árbol.
    retorna: nada. Lanza ValueError si el dato ya existe.'''

    def insertar(self, valor):
        self._raiz = self._insertarRecursivo(self._raiz, valor)

    '''
    nota: función recursiva para insertar un valor y balancear el árbol.
    argumentos: 
        - nodo: nodo actual en la recursión.
        - valor: valor a insertar.
    retorna: el nodo actualizado después de la inserción y balanceo.
    '''

    def _insertarRecursivo(self, nodo, valor):
        if nodo is None:
            return ClaseNodo(valor)

        if valor < nodo.getValor():
            nodo.setHijoIzquierdo(self._insertarRecursivo(nodo.getHijoIzquierdo(), valor))
        elif valor > nodo.getValor():
            nodo.setHijoDerecho(self._insertarRecursivo(nodo.getHijoDerecho(), valor))
        else:
            raise ValueError("El dato ya existe en el árbol")

        return self._balancear(nodo)

    '''
    nota: balancea el árbol en el nodo dado si está desbalanceado.
    argumentos: 
        - nodo: nodo a balancear.
    retorna: el nodo balanceado o el mismo nodo si no estaba desbalanceado.
    '''
    def _balancear(self, nodo):
        if nodo is None:
            return nodo

        factorBalance = self._obtenerFactorBalance(nodo)

        # Caso 1: Desbalance Izquierda-Izquierda
        if factorBalance > self.LIMITE_MAXIMO and self._obtenerFactorBalance(nodo.getHijoIzquierdo()) >= 0:
            return self._rotacionDerecha(nodo)

        # Caso 2: Desbalance Derecha-Derecha
        if factorBalance < -self.LIMITE_MAXIMO and self._obtenerFactorBalance(nodo.getHijoDerecho()) <= 0:
            return self._rotacionIzquierda(nodo)

        # Caso 3: Desbalance Izquierda-Derecha
        if factorBalance > self.LIMITE_MAXIMO and self._obtenerFactorBalance(nodo.getHijoIzquierdo()) < 0:
            nodo.setHijoIzquierdo(self._rotacionIzquierda(nodo.getHijoIzquierdo()))
            return self._rotacionDerecha(nodo)

        # Caso 4: Desbalance Derecha-Izquierda
        if factorBalance < -self.LIMITE_MAXIMO and self._obtenerFactorBalance(nodo.getHijoDerecho()) > 0:
            nodo.setHijoDerecho(self._rotacionDerecha(nodo.getHijoDerecho()))
            return self._rotacionIzquierda(nodo)

        return nodo
    '''
    nota: verifica el factor de balance de un nodo.
    argumentos: 
        - nodo: nodo a evaluar.
    retorna: la diferencia de alturas entre el subárbol izquierdo y derecho.
    '''
    def _obtenerFactorBalance(self, nodo):
        if nodo is None:
            return 0
        return self._alturaAux(nodo.getHijoIzquierdo()) - self._alturaAux(nodo.getHijoDerecho())


    '''
    nota: hace una rotación simple a la derecha.
    argumentos: 
        - nodo: nodo a rotar.
    retorna: el nuevo nodo raíz de la subárbol rotado.
    '''
    def _rotacionDerecha(self, nodo):
        hijoIzq = nodo.getHijoIzquierdo()
        nodo.setHijoIzquierdo(hijoIzq.getHijoDerecho())
        hijoIzq.setHijoDerecho(nodo)
        return hijoIzq

    '''
    nota: hace una rotación simple a la izquierda.
    argumentos: 
        - nodo: nodo a rotar.
    retorna: el nuevo nodo raíz de la subárbol rotado.
    '''
    def _rotacionIzquierda(self, nodo):
        hijoDer = nodo.getHijoDerecho()
        nodo.setHijoDerecho(hijoDer.getHijoIzquierdo())
        hijoDer.setHijoIzquierdo(nodo)
        return hijoDer


if __name__ == "__main__":
    avl = AVL()
    datos = [30, 10, 20]
    for d in datos:
        avl.insertar(d)

    print("Recorrido inOrden (AVL balanceado):", avl.inOrdenRecursivo())
    print("Recorrido posOrden (AVL balanceado):", avl.posOrdenRecursivo())
    print("Recorrido preOrden (AVL balanceado):", avl.preOrdenRecursivo())
    print("Altura del AVL:", avl.altura())
    avl.eliminar(20)
    print("Recorrido inOrden después de eliminar 20:", avl.inOrdenRecursivo())
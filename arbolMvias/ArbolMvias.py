from NodoMvias import NodoMVias

class ArbolMVias:
    def __init__(self, orden):
        if orden < 3:
            raise ValueError("El orden debe ser al menos 3")
        self.orden = orden
        self.raiz = None

    def esta_vacio(self):
        return self.raiz is None

    def get_raiz(self):
        return self.raiz

    def set_raiz(self, nodo):
        self.raiz = nodo

    # --- Operaciones principales ---
    def buscar(self, clave):
        """Busca una clave en el árbol"""
        return self._buscar(self.raiz, clave)

    def _buscar(self, nodo, clave):
        if nodo is None:
            return None
        for i, c in enumerate(nodo.claves):
            if c == clave:
                return nodo
            if c is None or clave < c:
                return self._buscar(nodo.hijos[i], clave)
        return self._buscar(nodo.hijos[-1], clave)

    def insertar(self, clave):
        """Inserción básica (sin balanceo tipo B-Tree, solo M-vías simple)"""
        if self.raiz is None:
            self.raiz = NodoMVias(self.orden)
            self.raiz.set_clave(0, clave)
            return

        self._insertar(self.raiz, clave)

    def _insertar(self, nodo, clave):
        # Si el nodo tiene espacio, insertar en la posición correcta
        if nodo.tiene_espacio():
            for i in range(len(nodo.claves)):
                if nodo.claves[i] is None:
                    nodo.claves[i] = clave
                    nodo.claves.sort(key=lambda x: (x is None, x))
                    return
        # Si no hay espacio, ir al hijo correspondiente
        for i, c in enumerate(nodo.claves):
            if c is None or clave < c:
                if nodo.hijos[i] is None:
                    nodo.hijos[i] = NodoMVias(self.orden)
                self._insertar(nodo.hijos[i], clave)
                return
        # Último hijo
        if nodo.hijos[-1] is None:
            nodo.hijos[-1] = NodoMVias(self.orden)
        self._insertar(nodo.hijos[-1], clave)

    # --- Utilidades adicionales para la web ---
    def limpiar(self):
        """Elimina todas las referencias del árbol."""
        self.raiz = None

    def cantidad_nodos(self):
        """Cuenta la cantidad total de claves almacenadas en el árbol."""
        return self._cantidad_nodos(self.raiz)

    def _cantidad_nodos(self, nodo):
        if nodo is None:
            return 0
        cantidad_en_nodo = sum(1 for c in nodo.claves if c is not None)
        total = cantidad_en_nodo
        for hijo in nodo.hijos:
            total += self._cantidad_nodos(hijo)
        return total

    def altura(self):
        """Altura del árbol M-vías (número de niveles)."""
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        alturas_hijos = [self._altura(h) for h in nodo.hijos if h is not None]
        return 1 + (max(alturas_hijos) if alturas_hijos else 0)

    def inorden(self):
        """Recorrido inorden generalizado para M-vías."""
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, acc):
        if nodo is None:
            return
        m = self.orden
        # Para cada clave i, visitar hijo i, luego clave i
        for i in range(m - 1):
            if i < len(nodo.hijos):
                self._inorden(nodo.hijos[i], acc)
            if i < len(nodo.claves) and nodo.claves[i] is not None:
                acc.append(nodo.claves[i])
        # Último hijo
        if len(nodo.hijos) > 0:
            self._inorden(nodo.hijos[-1], acc)

    def obtener_estructura_visual(self):
        """Crea una representación ASCII del árbol M-vías."""
        if self.esta_vacio():
            return "Árbol M-vías vacío"
        return self._estructura_visual(self.raiz, "", True)

    def _formatear_claves(self, claves):
        return "[" + ", ".join(str(c) for c in claves if c is not None) + "]"

    def _estructura_visual(self, nodo, prefijo, es_ultimo):
        if nodo is None:
            return ""
        linea = prefijo + ("└── " if es_ultimo else "├── ") + self._formatear_claves(nodo.claves) + "\n"
        # Filtrar hijos existentes con índice para saber si es el último real
        hijos_presentes = [(i, h) for i, h in enumerate(nodo.hijos) if h is not None]
        for i, (_, hijo) in enumerate(hijos_presentes):
            ultimo_hijo = i == len(hijos_presentes) - 1
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            linea += self._estructura_visual(hijo, nuevo_prefijo, ultimo_hijo)
        return linea

    # --- Serialización a JSON-like para API ---
    def to_dict(self):
        return self._nodo_to_dict(self.raiz)

    def _nodo_to_dict(self, nodo):
        if nodo is None:
            return None
        return {
            "keys": [c for c in nodo.claves if c is not None],
            "children": [self._nodo_to_dict(h) if h is not None else None for h in nodo.hijos]
        }

if __name__ == "__main__":
    arbol = ArbolMVias(4)  # Árbol M-vías de orden 4
    claves = [10, 20, 5, 6, 12, 30, 7, 17]

    for clave in claves:
        arbol.insertar(clave)
    # Búsqueda de claves
    for clave in [6, 15, 20]:
        resultado = arbol.buscar(clave)
        if resultado:
            print(f"Clave {clave} encontrada en el nodo con claves: {resultado.get_claves()}")
        else:
            print(f"Clave {clave} no encontrada en el árbol.")

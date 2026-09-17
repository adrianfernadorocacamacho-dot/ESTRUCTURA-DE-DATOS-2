class NodoMVias:
    def __init__(self, orden):
        self.orden = orden
        self.claves = [None] * (orden - 1)   # máximo M-1 claves
        self.hijos = [None] * orden          # máximo M hijos

    # --- Getters ---
    def get_clave(self, pos):
        return self.claves[pos]

    def get_hijo(self, pos):
        return self.hijos[pos]

    def get_claves(self):
        return self.claves

    def get_hijos(self):
        return self.hijos

    # --- Setters ---
    def set_clave(self, pos, valor):
        self.claves[pos] = valor

    def set_hijo(self, pos, nodo):
        self.hijos[pos] = nodo

    # --- Métodos de ayuda ---
    def es_hoja(self):
        return all(h is None for h in self.hijos)

    def tiene_espacio(self):
        """Devuelve True si aún hay lugar para insertar una clave."""
        return any(c is None for c in self.claves)

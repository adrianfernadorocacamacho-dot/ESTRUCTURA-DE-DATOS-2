from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'arbolBinario'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'arbolMvias'))

from ClaseArbolBinario import ArbolBinario
from AVL import AVL
from ArbolMvias import ArbolMVias

app = Flask(__name__)

app.secret_key = "Cruz"

arbol = ArbolBinario()
arbol_avl = AVL()
arbol_mvias = ArbolMVias(4)

def generar_visualizacion_ascii(tipo_arbol='normal'):
    """
    Genera una visualización ASCII del árbol binario usando el método optimizado de la clase.
    Argumentos:
        tipo_arbol: 'normal' para árbol binario normal, 'avl' para árbol AVL
    Retorna: str: La representación ASCII del árbol.
    """
    if tipo_arbol == 'avl':
        return arbol_avl.obtenerEstructuraVisual()
    if tipo_arbol == 'mvias':
        return arbol_mvias.obtener_estructura_visual()
    return arbol.obtenerEstructuraVisual()

def _bst_to_dict(nodo):
    if nodo is None:
        return None
    return {
        "value": nodo.getValor(),
        "left": _bst_to_dict(nodo.getHijoIzquierdo()),
        "right": _bst_to_dict(nodo.getHijoDerecho()),
    }

# ----------------------------------
# Rutas
# ----------------------------------
@app.route("/")
def index():
    info_arbol = {
        "total_nodos": arbol.cantidadNodos() if not arbol.isVacio() else 0,
        "altura": arbol.altura() if not arbol.isVacio() else 0,
        "inorden": arbol.inOrden() if not arbol.isVacio() else [],
        "preorden": arbol.preOrden() if not arbol.isVacio() else [],
        "postorden": arbol.posOrden() if not arbol.isVacio() else [],
    }
    
    info_avl = {
        "total_nodos": arbol_avl.cantidadNodos() if not arbol_avl.isVacio() else 0,
        "altura": arbol_avl.altura() if not arbol_avl.isVacio() else 0,
        "inorden": arbol_avl.inOrden() if not arbol_avl.isVacio() else [],
        "preorden": arbol_avl.preOrden() if not arbol_avl.isVacio() else [],
        "postorden": arbol_avl.posOrden() if not arbol_avl.isVacio() else [],
    }
    
    info_mvias = {
        "total_nodos": arbol_mvias.cantidad_nodos() if not arbol_mvias.esta_vacio() else 0,
        "altura": arbol_mvias.altura() if not arbol_mvias.esta_vacio() else 0,
        "inorden": arbol_mvias.inorden() if not arbol_mvias.esta_vacio() else [],
    }
    
    return render_template("index.html",
                           info_arbol=info_arbol,
                           info_avl=info_avl,
                           info_mvias=info_mvias,
                           visualizacion_ascii=generar_visualizacion_ascii(),
                           visualizacion_avl=generar_visualizacion_ascii('avl'),
                           visualizacion_mvias=generar_visualizacion_ascii('mvias'))

@app.route("/insertar", methods=["POST"])
def insertar():
    valor = int(request.form["valor"])
    arbol.insertar(valor)
    flash(f"Valor {valor} insertado correctamente en el árbol binario", "success")
    return redirect(url_for("index"))

@app.route("/insertar_avl", methods=["POST"])
def insertar_avl():
    valor = int(request.form["valor"])
    try:
        arbol_avl.insertar(valor)
        flash(f"Valor {valor} insertado correctamente en el árbol AVL", "success")
    except ValueError as e:
        flash(f"Error: {str(e)}", "error")
    return redirect(url_for("index"))

@app.route("/insertar_mvias", methods=["POST"])
def insertar_mvias():
    valor = int(request.form["valor"]) 
    arbol_mvias.insertar(valor)
    flash(f"Valor {valor} insertado correctamente en el árbol M-vías", "success")
    return redirect(url_for("index"))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    valor = int(request.form["valor"])
    arbol.eliminar(valor)
    flash(f"Valor {valor} eliminado", "success")
    return redirect(url_for("index"))

@app.route("/buscar", methods=["POST"])
def buscar():
    valor = int(request.form["valor"])
    if arbol.buscar(valor):
        flash(f"Valor {valor} encontrado en el árbol", "success")
    else:
        flash(f"Valor {valor} no está en el árbol", "error")
    return redirect(url_for("index"))

@app.route("/limpiar_arbol", methods=["POST"])
def limpiar_arbol():
    arbol.limpiarArbol()
    arbol_avl.limpiarArbol()
    arbol_mvias.limpiar()
    flash("Ambos árboles limpiados", "success")
    return redirect(url_for("index"))

@app.route("/api/tree_data")
def api_tree_data():
    data = {
        "bst": _bst_to_dict(arbol.getRaiz()),
        "avl": _bst_to_dict(arbol_avl.getRaiz()),
        "mvias": arbol_mvias.to_dict(),
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
import os

def limpiar_progreso():
    # Dejamos únicamente el archivo de la matriz Q que necesitas resetear
    archivo_a_borrar = 'matriz_q_local.json'
    
    if os.path.exists(archivo_a_borrar):
        os.remove(archivo_a_borrar)
        print(f"-> Archivo '{archivo_a_borrar}' eliminado. El cerebro del bot se ha reseteado.")
    else:
        print(f"-> El archivo '{archivo_a_borrar}' no existía, la matriz ya está limpia.")

if __name__ == "__main__":
    limpiar_progreso()
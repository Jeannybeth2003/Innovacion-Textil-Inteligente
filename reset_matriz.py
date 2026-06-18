import os

def limpiar_progreso():
    archivos_a_borrar = ['matriz_q_local.json']
    
    for archivo in archivos_a_borrar:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"-> Archivo '{archivo}' eliminado. El cerebro del bot se ha reseteado.")
        else:
            print(f"-> El archivo '{archivo}' no existía, la matriz ya está limpia.")

if __name__ == "__main__":
    limpiar_progreso()
import random
import json
import os

# Ruta local para tu PC y ruta remota para Google Colab
PATH_LOCAL = 'matriz_q_local.json'
PATH_NUBE = '/content/drive/My Drive/Taller_Futuro_IA/matriz_q.json'

class AgenteQLearning:
    def __init__(self, estados, acciones, alpha=0.5, epsilon=0.3):
        self.alpha = alpha       
        self.epsilon = epsilon   
        self.acciones = acciones 
        self.estados = estados
        
        # Determinar si estamos en entorno Colab o en la PC local
        self.es_colab = os.path.exists('/content/drive')
        self.ruta_guardado = PATH_NUBE if self.es_colab else PATH_LOCAL
        
        # Cargar conocimiento previo
        self.tabla_q = self.cargar_matriz()

    def cargar_matriz(self):
        """Carga la matriz desde el archivo local o desde Google Drive según corresponda"""
        if os.path.exists(self.ruta_guardado):
            try:
                with open(self.ruta_guardado, 'r') as f:
                    print(f"-> [Cerebro] Matriz Q cargada con éxito desde: {self.ruta_guardado}")
                    return json.load(f)
            except Exception as e:
                print(f"-> [Error] No se pudo leer la matriz: {e}. Inicializando en ceros.")
        
        # Si el archivo no existe, creamos la matriz vacía en ceros
        print("-> [Cerebro] Inicializando nueva Tabla Q en ceros.")
        nueva_tabla = {}
        for estado in self.estados:
            nueva_tabla[estado] = {accion: 0.0 for accion in self.acciones}
        return nueva_tabla

    def guardar_matriz(self):
        """Guarda la matriz en tu computadora o en la nube automáticamente"""
        try:
            if self.es_colab:
                os.makedirs(os.path.dirname(self.ruta_guardado), exist_ok=True)
            
            with open(self.ruta_guardado, 'w') as f:
                json.dump(self.tabla_q, f, indent=4)
            print(f"-> [Cerebro] Progreso guardado automáticamente en: {self.ruta_guardado}")
        except Exception as e:
            print(f"-> [Error] Falló al guardar el progreso: {e}")

    def elegir_accion(self, estado):
        """Estrategia Epsilon-Greedy (Exploración vs Explotación)"""
        if random.random() < self.epsilon:
            return random.choice(self.acciones)
        else:
            valores_estado = self.tabla_q[estado]
            max_q = max(valores_estado.values())
            mejores_acciones = [acc for acc, val in valores_estado.items() if val == max_q]
            return random.choice(mejores_acciones)

    def actualizar_q(self, estado, accion, recompensa):
        """Ecuación simplificada de Bellman"""
        q_actual = self.tabla_q[estado][accion]
        nuevo_q = q_actual + self.alpha * (recompensa - q_actual)
        self.tabla_q[estado][accion] = round(nuevo_q, 4)
        
        print(f"[Ecuación] Actualizado Q({estado}, {accion}) = {self.tabla_q[estado][accion]}")
        
        # Auto-guardar inmediatamente tras el cambio
        self.guardar_matriz()
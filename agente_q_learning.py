import random

class AgenteQLearning:
    def __init__(self, estados, acciones, alpha=0.5, epsilon=0.3):
        self.alpha = alpha       # Tasa de aprendizaje
        self.epsilon = epsilon   # Probabilidad de exploración
        self.acciones = acciones # Lista de acciones
        
        # Inicializamos la Tabla Q en cero para cada par Estado-Acción
        self.tabla_q = {}
        for estado in estados:
            self.tabla_q[estado] = {accion: 0.0 for accion in acciones}

    def elegir_accion(self, estado):
        """Estrategia Epsilon-Greedy para la selección de respuestas"""
        # EXPLORACIÓN
        if random.random() < self.epsilon:
            return random.choice(self.acciones)
        # EXPLOTACIÓN
        else:
            valores_estado = self.tabla_q[estado]
            max_q = max(valores_estado.values())
            mejores_acciones = [acc for acc, val in valores_estado.items() if val == max_q]
            return random.choice(mejores_acciones)

    def actualizar_q(self, estado, accion, recompensa):
        """Ecuación de Bellman simplificada (Contextual Bandit)"""
        q_actual = self.tabla_q[estado][accion]
        nuevo_q = q_actual + self.alpha * (recompensa - q_actual)
        self.tabla_q[estado][accion] = round(nuevo_q, 4)
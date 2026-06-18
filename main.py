from agente_q_learning import AgenteQLearning
from interfaz_chat import iniciar_chat
# Importamos la estructura de datos y el clasificador de tu dataset
from dataset import DATASET, clasificar_intencion

def main():
    # 1. Definir los estados REALES basados en tu dataset (S0 hasta S4)
    estados_textiles = ["S0", "S1", "S2", "S3", "S4"]
    
    # 2. Definir las acciones REALES que el agente puede elegir (A0 hasta A5)
    acciones_bot = ["A0", "A1", "A2", "A3", "A4", "A5"]
    
    # 3. Instanciar el agente de Aprendizaje por Refuerzo (Q-Learning)
    # Creará o cargará la matriz basándose en tus claves de S0-S4 y A0-A5
    inteligencia_bot = AgenteQLearning(estados=estados_textiles, acciones=acciones_bot)
        
    # 4. Arrancar la ventana del chat pasándole el objeto del agente de IA
    iniciar_chat(inteligencia_bot)

if __name__ == "__main__":
    main()
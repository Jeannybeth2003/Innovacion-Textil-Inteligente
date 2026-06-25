from agente_q_learning import AgenteQLearning
from interfaz_chat import iniciar_chat
from dataset import DATASET, clasificar_intencion

def main():
    estados_textiles = ["S0", "S1", "S2", "S3", "S4"]
    
    acciones_bot = ["A0", "A1", "A2", "A3", "A4", "A5"]
    
    inteligencia_bot = AgenteQLearning(estados=estados_textiles, acciones=acciones_bot)
        
    iniciar_chat(inteligencia_bot)

if __name__ == "__main__":
    main()
DATASET = {
    "S0": {
        "nombre": "Inicialización del Sistema",
        "palabras_clave": ["hola", "iniciar", "encender", "activar sistema", "buenos dias", "conectar panel"],
        "acciones": {
            "A0": "Consola textil activa. Cargando interfaz holográfica y sistemas de corte inteligente.",
            "A1": "Sistemas listos. Esperando instrucciones de diseño o calibración.",
            "A2": "Conexión establecida con el taller local. Bienvenidos al sistema.",
            "A3": "Sistema base operando en modo óptimo.",
            "A4": "Esperando comandos de voz o texto.",
            "A5": "Inicialización completa."
        }
    },
    "S1": {
        "nombre": "Optimización y Corte IA",
        "palabras_clave": ["patron", "tela", "diseño ia", "proyectar corte", "desperdicio", "minimizar", "rollo", "eficiencia"],
        "acciones": {
            "A0": "Patrón vectorial calculado por IA. Proyectando guías lumínicas sobre la tela.",
            "A1": "Optimizando distribución de moldes. Desperdicio estimado reducido a menos del 1.5%.",
            "A2": "Cortadora láser calibrada según el grosor del material detectado.",
            "A3": "Corte inteligente listo para ejecución.",
            "A4": "Analizando plano de hilos para evitar deshilachado.",
            "A5": "Eficiencia de material maximizada por el agente Q-Learning."
        }
    },
    "S2": {
        "nombre": "Calibración de Pantallas",
        "palabras_clave": ["calibrar", "no se ve", "pantalla", "proyector", "alinear", "brillo", "ajustar imagen", "error proyeccion"],
        "acciones": {
            "A0": "Iniciando escaneo de superficie y ajuste automático del proyector.",
            "A1": "Sensores alineados. Brillo e imagen corregidos para visualización sobre telas oscuras.",
            "A2": "Calibración completada con éxito. El área de trabajo está lista.",
            "A3": "Reajustando enfoque óptico del sistema de proyección.",
            "A4": "Sincronizando coordenadas lumínicas con la mesa de corte.",
            "A5": "Geometría de pantalla corregida."
        }
    },
    "S3": {
        "nombre": "Reporte e Inventario",
        "palabras_clave": ["inventario", "stock", "cuanto queda", "material", "reporte", "revisar telas", "sincronizar"],
        "acciones": {
            "A0": "Cargando reporte en la nube: Rollos de tela optimizados y stock sincronizado en tiempo real.",
            "A1": "Alerta de inventario: Stock de lino bajo. Se sugiere reordenar pronto.",
            "A2": "Registro de uso actualizado. Historial guardado correctamente.",
            "A3": "Buscando disponibilidad de insumos en el servidor central.",
            "A4": "Reporte de rendimiento textil generado.",
            "A5": "Inventario local en perfecta sincronía con la nube."
        }
    },
    "S4": {
        "nombre": "c",
        "palabras_clave": [], 
        "acciones": {
            "A0": "Comando no reconocido en el Taller del Futuro. Por favor, solicita 'Corte IA', 'Calibrar' o revisa el inventario.",
            "A1": "No entendí la solicitud. Intenta usar palabras como 'diseño', 'pantalla' o 'stock'.",
            "A2": "Por favor, reformula tu instrucción técnica.",
            "A3": "Entrada fuera del alcance del sistema textil.",
            "A4": "Consulta la guía de comandos para más información.",
            "A5": "Asistente en modo de espera. Intenta de nuevo."
        }
    }
}

def clasificar_intencion(texto_usuario):
    texto = texto_usuario.lower().strip()
    for estado, contenido in DATASET.items():
        if estado == "S4":
            continue
        for palabra in contenido["palabras_clave"]:
            if palabra in texto:
                return estado
    return "S4"
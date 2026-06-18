DATASET = {
    "S0": {
        "nombre": "Inicialización del Sistema",
        "palabras_clave": ["hola", "iniciar", "encender", "activar sistema", "buenos dias", "conectar panel"],
        "acciones": {
            "A0": "Consola textil activa. Cargando interfaz holográfica y sistemas de corte inteligente.",
            "A1": "Patrón vectorial calculado por IA. Proyectando guías lumínicas sobre la tela. Desperdicio estimado: < 1.5%.",
            "A2": "Iniciando escaneo de superficie. Alineando sensores ópticos con la máquina de coser tradicional.",
            "A3": "Cargando reporte en la nube: Rollos de tela optimizados y stock sincronizado en tiempo real.",
            "A4": "Guardando registros de producción en la nube. Apagando pantallas gigantes y proyectores. ¡Buen trabajo!",
            "A5": "Comando no reconocido en el Taller del Futuro. Por favor, solicita 'Corte IA' o 'Calibrar'."
        }
    },
    "S1": {
        "nombre": "Optimización y Corte IA",
        "palabras_clave": ["patron", "tela", "diseño ia", "proyectar corte", "desperdicio", "minimizar", "rollo", "eficiencia"],
        "acciones": {
            "A0": "Consola textil activa. Cargando interfaz holográfica y sistemas de corte inteligente.",
            "A1": "Patrón vectorial calculado por IA. Proyectando guías lumínicas sobre la tela. Desperdicio estimado: < 1.5%.",
            "A2": "Iniciando escaneo de superficie. Alineando sensores ópticos con la máquina de coser tradicional.",
            "A3": "Cargando reporte en la nube: Rollos de tela optimizados y stock sincronizado en tiempo real.",
            "A4": "Guardando registros de producción en la nube. Apagando pantallas gigantes y proyectores. ¡Buen trabajo!",
            "A5": "Comando no reconocido en el Taller del Futuro. Por favor, solicita 'Corte IA' o 'Calibrar'."
        }
    },
    "S2": {
        "nombre": "Calibración de Pantallas",
        "palabras_clave": ["calibrar", "no se ve", "pantalla", "proyector", "alinear", "brillo", "ajustar imagen", "error proyeccion"],
        "acciones": {
            "A0": "Consola textil activa. Cargando interfaz holográfica y sistemas de corte inteligente.",
            "A1": "Patrón vectorial calculado por IA. Proyectando guías lumínicas sobre la tela. Desperdicio estimado: < 1.5%.",
            "A2": "Iniciando escaneo de superficie. Alineando sensores ópticos con la máquina de coser tradicional.",
            "A3": "Cargando reporte en la nube: Rollos de tela optimizados y stock sincronizado en tiempo real.",
            "A4": "Guardando registros de producción en la nube. Apagando pantallas gigantes y proyectores. ¡Buen trabajo!",
            "A5": "Comando no reconocido en el Taller del Futuro. Por favor, solicita 'Corte IA' o 'Calibrar'."
        }
    },
    "S3": {
        "nombre": "Reporte e Inventario",
        "palabras_clave": ["inventario", "stock", "cuanto queda", "material", "reporte", "revisar telas", "sincronizar"],
        "acciones": {
            "A0": "Consola textil activa. Cargando interfaz holográfica y sistemas de corte inteligente.",
            "A1": "Patrón vectorial calculado por IA. Proyectando guías lumínicas sobre la tela. Desperdicio estimado: < 1.5%.",
            "A2": "Iniciando escaneo de superficie. Alineando sensores ópticos con la máquina de coser tradicional.",
            "A3": "Cargando reporte en la nube: Rollos de tela optimizados y stock sincronizado en tiempo real.",
            "A4": "Guardando registros de producción en la nube. Apagando pantallas gigantes y proyectores. ¡Buen trabajo!",
            "A5": "Comando no reconocido en el Taller del Futuro. Por favor, solicita 'Corte IA' o 'Calibrar'."
        }
    },
    "S4": {
        "nombre": "Comando Desconocido",
        "palabras_clave": [], 
        "acciones": {
            "A0": "Consola textil activa. Cargando interfaz holográfica y sistemas de corte inteligente.",
            "A1": "Patrón vectorial calculado por IA. Proyectando guías lumínicas sobre la tela. Desperdicio estimado: < 1.5%.",
            "A2": "Iniciando escaneo de superficie. Alineando sensores ópticos con la máquina de coser tradicional.",
            "A3": "Cargando reporte en la nube: Rollos de tela optimizados y stock sincronizado en tiempo real.",
            "A4": "Guardando registros de producción en la nube. Apagando pantallas gigantes y proyectores. ¡Buen trabajo!",
            "A5": "Comando no reconocido en el Taller del Futuro. Por favor, solicita 'Corte IA' o 'Calibrar'."
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
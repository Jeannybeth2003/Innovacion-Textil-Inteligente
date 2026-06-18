import pygame
import os
# Conexión directa con tu dataset y clasificador real
from dataset import DATASET, clasificar_intencion 

def renderizar_texto_con_ajuste(texto, fuente, ancho_maximo, color_texto):
    """Divide un texto largo en múltiples líneas para evitar que se desborde."""
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        test_linea = linea_actual + palabra + " "
        if fuente.size(test_linea)[0] <= ancho_maximo:
            linea_actual = test_linea
        else:
            if linea_actual:
                lineas.append(linea_actual.strip())
            linea_actual = palabra + " "
    if linea_actual:
        lineas.append(linea_actual.strip())
        
    surfaces = [fuente.render(linea, True, color_texto) for linea in lineas]
    return surfaces

def iniciar_chat(agente_ia):
    pygame.init()

    # --- Paleta de Colores ---
    NEGRO_TEXTO = (45, 52, 54)
    BORDES = (218, 223, 230)
    
    # Colores de interfaz limpia
    COLOR_BARRA_INPUT = (241, 242, 246)
    COLOR_CARRITO_INPUT = (255, 255, 255)
    
    # Colores de las Burbujas
    COLOR_BURBUJA_BOT = (255, 255, 255)
    BORDE_BURBUJA_BOT = (230, 234, 240)
    COLOR_BURBUJA_USUARIO = (212, 231, 252) 
    BORDE_BURBUJA_USUARIO = (185, 215, 250)

    # Colores de los botones de Feedback (Feedback visual al presionar)
    COLOR_LIKE = (46, 204, 113)      # Verde Esmeralda
    COLOR_DISLIKE = (231, 76, 60)    # Rojo Alizarina

    ANCHO_VENTANA = 800
    ALTO_VENTANA = 600
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Consola de Control - Taller del Futuro")

    # --- Gestión de Recursos Visuales ---
    ruta_imagen = "Gemini_Generated_Image_j5qrunj5qrunj5qr.png"
    if not os.path.exists(ruta_imagen):
        ruta_imagen = os.path.join("Innovacion-Textil-Inteligente-main", ruta_imagen)

    if not os.path.exists(ruta_imagen):
        print(f"Error Crítico: No se pudo encontrar {ruta_imagen}")
        exit()

    imagen_base = pygame.image.load(ruta_imagen).convert()
    imagen_fondo_chat = pygame.transform.scale(imagen_base, (550, 600))
    imagen_lateral = pygame.transform.scale(imagen_base, (250, ALTO_VENTANA))

    # --- Configuración Segura de Tipografías ---
    fuente_elegante = pygame.font.match_font('georgia') or pygame.font.match_font('timesnewroman') or pygame.font.get_default_font()
    fuente_estandar = pygame.font.match_font('arial') or pygame.font.match_font('sans') or pygame.font.get_default_font()

    # Título: Cursiva y Elegante
    fuente_cabecera = pygame.font.Font(fuente_elegante, 20)
    fuente_cabecera.set_bold(True)
    fuente_cabecera.set_italic(True)
    
    # Chat: Arial / Sans Serif limpio
    fuente_chat = pygame.font.Font(fuente_estandar, 16)
    fuente_input = pygame.font.Font(fuente_estandar, 18)
    fuente_botones = pygame.font.Font(fuente_estandar, 22)

    # --- Historial y Variables de Control de IA ---
    mensaje_inicial = DATASET["S0"]["acciones"]["A0"]
    mensajes = [("Bot", mensaje_inicial)]
    
    # Variables auxiliares para recordar la última interacción y poder calificarla
    ultimo_estado_ia = "S0"
    ultima_accion_ia = "A0"

    # --- Estructuras de la Barra Inferior Opciones Cambiadas ---
    rect_barra_inferior = pygame.Rect(250, 520, 550, 80)
    # Movimos el input un poco más a la izquierda ya que eliminamos el '+'
    input_rect = pygame.Rect(270, 540, 390, 40) 
    text_input = ""

    # Botones Interactivos de Entrenamiento (👍 y 👎) posicionados a la derecha de la barra
    btn_like_rect = pygame.Rect(680, 540, 45, 40)
    btn_dislike_rect = pygame.Rect(735, 540, 45, 40)

    reloj = pygame.time.Clock()
    corriendo = True
    pygame.key.set_repeat(400, 40)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clic izquierdo
                    # Si el usuario presiona el botón de LIKE (👍)
                    if btn_like_rect.collidepoint(evento.pos):
                        print(f"-> [Feedback Positivo] Calificando Q({ultimo_estado_ia}, {ultima_accion_ia}) con +10")
                        agente_ia.actualizar_q(ultimo_estado_ia, ultima_accion_ia, 10)
                        mensajes.append(("Bot", "¡Entendido! Guardando recompensa positiva en mi matriz Q."))
                    
                    # Si el usuario presiona el botón de DISLIKE (👎)
                    elif btn_dislike_rect.collidepoint(evento.pos):
                        print(f"-> [Feedback Negativo] Calificando Q({ultimo_estado_ia}, {ultima_accion_ia}) con -10")
                        agente_ia.actualizar_q(ultimo_estado_ia, ultima_accion_ia, -10)
                        mensajes.append(("Bot", "Corrigiendo... Aplicando penalización en mi matriz de aprendizaje."))

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif evento.key == pygame.K_RETURN:
                    if text_input.strip() != "":
                        mensajes.append(("Usuario", text_input))
                        
                        # Clasificación de estado según tu dataset.py real (S0, S1, S2, S3, S4)
                        estado_actual = clasificar_intencion(text_input)
                        
                        # Si tu main.py inicializó con "saludo", forzamos compatibilidad segura con el dataset
                        if estado_actual not in agente_ia.tabla_q:
                            # Asegura que el estado exista dinámicamente en el cerebro del agente
                            agente_ia.tabla_q[estado_actual] = {acc: 0.0 for acc in ["A0","A1","A2","A3","A4","A5"]}
                        
                        # Elegir acción con Q-Learning
                        accion_elegida = agente_ia.elegir_accion(estado_actual)
                        
                        # Si las acciones registradas en el agente eran de texto plano, mapeamos a las del dataset
                        if accion_elegida not in DATASET[estado_actual]["acciones"]:
                            # Tomar una acción válida por defecto del set de datos
                            accion_elegida = "A1" if estado_actual == "S1" else "A5"
                        
                        respuesta_bot = DATASET[estado_actual]["acciones"][accion_elegida]
                        
                        # Respaldamos en las variables globales para que los botones sepan qué calificar
                        ultimo_estado_ia = estado_actual
                        ultima_accion_ia = accion_elegida
                        
                        # Recompensa base por defecto
                        recompensa_base = 5 if estado_actual != "S4" else -1
                        agente_ia.actualizar_q(estado_actual, accion_elegida, recompensa_base)
                        
                        mensajes.append(("Bot", respuesta_bot))
                        text_input = ""
                else:
                    if len(text_input) < 48:  
                        text_input += evento.unicode

        # --- CAPAS DE RENDERIZADO ---
        ventana.fill((255, 255, 255))
        
        # Fondos Textiles limpios
        ventana.blit(imagen_lateral, (0, 0))
        ventana.blit(imagen_fondo_chat, (250, 0))
        pygame.draw.line(ventana, (40, 40, 40), (250, 0), (250, 600), 2)

        # Cabecera superior fija
        rect_cabecera = pygame.Rect(250, 0, 550, 65)
        pygame.draw.rect(ventana, COLOR_CARRITO_INPUT, rect_cabecera)
        pygame.draw.line(ventana, BORDES, (250, 65), (800, 65), 1)
        
        texto_cabecera = fuente_cabecera.render("Consola de Control — Taller del Futuro", True, NEGRO_TEXTO)
        ventana.blit(texto_cabecera, (275, 22))

        # --- Renderizado de Burbujas Inteligentes ---
        y_mensaje = 85
        separacion = 14
        ancho_maximo_burbuja = 340
        
        for remitente, mensaje in mensajes[-6:]:
            es_bot = remitente == "Bot"
            color_fondo = COLOR_BURBUJA_BOT if es_bot else COLOR_BURBUJA_USUARIO
            color_borde = BORDE_BURBUJA_BOT if es_bot else BORDE_BURBUJA_USUARIO
            pos_x = 275 if es_bot else 775
            
            lineas_renderizadas = renderizar_texto_con_ajuste(mensaje, fuente_chat, ancho_maximo_burbuja, NEGRO_TEXTO)
            
            ancho_contenido = max([linea.get_width() for linea in lineas_renderizadas])
            alto_contenido = sum([linea.get_height() for linea in lineas_renderizadas]) + (len(lineas_renderizadas) - 1) * 3
            
            ancho_burbuja = ancho_contenido + 26
            alto_burbuja = alto_contenido + 18
            
            if not es_bot:
                pos_x = pos_x - ancho_burbuja

            burbuja_rect = pygame.Rect(pos_x, y_mensaje, ancho_burbuja, alto_burbuja)
            pygame.draw.rect(ventana, color_fondo, burbuja_rect, border_radius=12)
            pygame.draw.rect(ventana, color_borde, burbuja_rect, width=1, border_radius=12)
            
            y_linea = y_mensaje + 9
            for linea_surface in lineas_renderizadas:
                ventana.blit(linea_surface, (pos_x + 13, y_linea))
                y_linea += linea_surface.get_height() + 3
                
            y_mensaje += alto_burbuja + separacion

        # --- Barra Inferior Fija para Entradas de Texto ---
        pygame.draw.rect(ventana, COLOR_BARRA_INPUT, rect_barra_inferior)
        pygame.draw.line(ventana, BORDES, (250, 520), (800, 520), 1)
        
        # Campo de Entrada de Texto estilizado
        pygame.draw.rect(ventana, COLOR_CARRITO_INPUT, input_rect, border_radius=20)
        pygame.draw.rect(ventana, BORDES, input_rect, width=1, border_radius=20)
        
        if text_input == "":
            surface_placeholder = fuente_input.render("Escribe un comando ('patron', 'calibrar')...", True, (180, 186, 201))
            ventana.blit(surface_placeholder, (290, 551))
        else:
            surface_texto_entrada = fuente_input.render(text_input, True, NEGRO_TEXTO)
            ventana.blit(surface_texto_entrada, (290, 551))
            
        # --- NUEVOS BOTONES DE ENTRENAMIENTO (👍 / 👎) ---
        # Botón de Like
        pygame.draw.rect(ventana, COLOR_LIKE, btn_like_rect, border_radius=10)
        surface_like = fuente_botones.render("👍", True, COLOR_CARRITO_INPUT)
        ventana.blit(surface_like, (btn_like_rect.x + 11, btn_like_rect.y + 7))

        # Botón de Dislike
        pygame.draw.rect(ventana, COLOR_DISLIKE, btn_dislike_rect, border_radius=10)
        surface_dislike = fuente_botones.render("👎", True, COLOR_CARRITO_INPUT)
        ventana.blit(surface_dislike, (btn_dislike_rect.x + 11, btn_dislike_rect.y + 7))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
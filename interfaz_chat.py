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

    # --- Paleta de Colores Minimalista e Industrial ---
    NEGRO_TEXTO = (45, 52, 54)
    BORDES = (210, 215, 223)
    BORDES_INTERACTIVOS = (155, 168, 182)
    
    # Colores del Entorno de Chat (Izquierda)
    COLOR_BARRA_INFERIOR = (245, 247, 250)    
    COLOR_CARRITO_INPUT = (255, 255, 255)     
    COLOR_FONDO_BOTONES = (228, 233, 240)     
    COLOR_BURBUJA_BOT = (255, 255, 255)
    BORDE_BURBUJA_BOT = (230, 234, 240)
    COLOR_BURBUJA_USUARIO = (212, 231, 252)
    BORDE_BURBUJA_USUARIO = (185, 215, 250)

    # Colores del Panel de Control IA (Derecha)
    COLOR_PANEL_DERECHO = (248, 249, 252)
    COLOR_TABLA_CABECERA = (74, 144, 226) # Azul tecnológico para los encabezados de la tabla
    COLOR_TABLA_TEXTO_CABECERA = (255, 255, 255)
    COLOR_FONDO_CELDA = (255, 255, 255)
    COLOR_CODIGO_FONDO = (30, 39, 46)     # Fondo oscuro elegante para la fórmula matemática

    # --- NUEVAS DIMENSIONES EXPANDIDAS ---
    ANCHO_VENTANA = 1200 # Ventana ancha para que quepan ambas secciones cómodamente
    ALTO_VENTANA = 650
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Consola de Control de Aprendizaje por Refuerzo — Confecciones Santa Rosa")

    # --- Carga de Recursos Visuales ---
    ruta_imagen = "Gemini_Generated_Image_j5qrunj5qrunj5qr.png"
    if not os.path.exists(ruta_imagen):
        ruta_imagen = os.path.join("Innovacion-Textil-Inteligente-main", ruta_imagen)

    if not os.path.exists(ruta_imagen):
        print(f"Error Crítico: No se pudo encontrar {ruta_imagen}")
        exit()

    imagen_base = pygame.image.load(ruta_imagen).convert()
    # Ajustamos el fondo del chat para que ocupe exactamente su mitad correspondiente
    imagen_fondo_chat = pygame.transform.scale(imagen_base, (600, 650))

    # --- Carga de tus Logos de Mezclilla Rectangulares ---
    img_like_path = "image-removebg-preview (93).png"
    img_dislike_path = "image-removebg-preview (94).png"

    if os.path.exists(img_like_path) and os.path.exists(img_dislike_path):
        img_like_base = pygame.image.load(img_like_path).convert_alpha()
        img_dislike_base = pygame.image.load(img_dislike_path).convert_alpha()
        # Escalado ancho proporcional para evitar el efecto "aplastado"
        img_like = pygame.transform.scale(img_like_base, (75, 48))
        img_dislike = pygame.transform.scale(img_dislike_base, (75, 48))
    else:
        print("Error: No se encontraron los archivos de imagen para los botones de feedback.")
        exit()

    # --- Fuentes Tipográficas del Sistema ---
    fuente_elegante = pygame.font.match_font('georgia') or pygame.font.match_font('timesnewroman') or pygame.font.get_default_font()
    fuente_estandar = pygame.font.match_font('arial') or pygame.font.match_font('sans') or pygame.font.get_default_font()
    fuente_mono = pygame.font.match_font('consola') or pygame.font.match_font('courier') or pygame.font.get_default_font()

    fuente_cabecera = pygame.font.Font(fuente_elegante, 22)
    fuente_cabecera.set_bold(True)
    fuente_cabecera.set_italic(True)
    
    fuente_chat = pygame.font.Font(fuente_estandar, 16)
    fuente_input = pygame.font.Font(fuente_estandar, 16)
    
    # Fuentes específicas para la tabla de datos
    fuente_seccion = pygame.font.Font(fuente_estandar, 18)
    fuente_seccion.set_bold(True)
    fuente_tabla = pygame.font.Font(fuente_estandar, 14)
    fuente_tabla_negrita = pygame.font.Font(fuente_estandar, 14)
    fuente_tabla_negrita.set_bold(True)
    fuente_codigo = pygame.font.Font(fuente_mono, 13)

    # --- Historial y Control del Agente Inteligente ---
    mensaje_inicial = DATASET["S0"]["acciones"]["A0"]
    mensajes = [("Bot", mensaje_inicial)]
    
    ultimo_estado_ia = "S0"
    ultima_accion_ia = "A0"
    ultima_recompensa = 0.0
    formula_texto = "Q(S0, A0) = 0.0"

    # --- GEOMETRÍA DE LA INTERFAZ DE CHAT (LADO IZQUIERDO: 0 a 600) ---
    rect_barra_inferior = pygame.Rect(0, 550, 600, 100) 
    input_rect = pygame.Rect(20, 570, 370, 60) 
    text_input = ""

    capsula_botones_rect = pygame.Rect(410, 570, 170, 60)
    btn_like_rect = pygame.Rect(418, 576, 75, 48)
    btn_dislike_rect = pygame.Rect(498, 576, 75, 48)

    reloj = pygame.time.Clock()
    corriendo = True
    pygame.key.set_repeat(400, 40)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    # Recompensa manual desde tus botones de jean
                    if btn_like_rect.collidepoint(evento.pos):
                        agente_ia.actualizar_q(ultimo_estado_ia, ultima_accion_ia, 10.0)
                        ultima_recompensa = 10.0
                        formula_texto = f"Q_nuevo({ultimo_estado_ia}, {ultima_accion_ia}) = {agente_ia.tabla_q[ultimo_estado_ia][ultima_accion_ia]:.2f} (Feedback Positivo)"
                        mensajes.append(("Bot", "¡Excelente! He registrado tu recompensa manual de +10 en mi matriz."))
                    
                    elif btn_dislike_rect.collidepoint(evento.pos):
                        agente_ia.actualizar_q(ultimo_estado_ia, ultima_accion_ia, -10.0)
                        ultima_recompensa = -10.0
                        formula_texto = f"Q_nuevo({ultimo_estado_ia}, {ultima_accion_ia}) = {agente_ia.tabla_q[ultimo_estado_ia][ultima_accion_ia]:.2f} (Feedback Negativo)"
                        mensajes.append(("Bot", "Entendido. Aplicando penalización manual de -10 en mis conexiones de estado."))

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif evento.key == pygame.K_RETURN:
                    if text_input.strip() != "":
                        mensajes.append(("Usuario", text_input))
                        
                        # Procesamiento semántico de intenciones
                        estado_actual = clasificar_intencion(text_input)
                        
                        if estado_actual not in agente_ia.tabla_q:
                            agente_ia.tabla_q[estado_actual] = {acc: 0.0 for acc in ["A0","A1","A2","A3","A4","A5"]}
                        
                        accion_elegida = agente_ia.elegir_accion(estado_actual)
                        
                        if accion_elegida not in DATASET[estado_actual]["acciones"]:
                            accion_elegida = "A1" if estado_actual == "S1" else "A5"
                        
                        respuesta_bot = DATASET[estado_actual]["acciones"][accion_elegida]
                        
                        # Cálculo matemático del algoritmo de aprendizaje
                        recompensa_base = 5.0 if estado_actual != "S4" else -2.0
                        q_anterior = agente_ia.tabla_q[estado_actual][accion_elegida]
                        agente_ia.actualizar_q(estado_actual, accion_elegida, recompensa_base)
                        q_nuevo = agente_ia.tabla_q[estado_actual][accion_elegida]
                        
                        # Guardamos los metadatos de control para refrescar el panel derecho
                        ultimo_estado_ia = estado_actual
                        ultima_accion_ia = accion_elegida
                        ultima_recompensa = recompensa_base
                        formula_texto = f"Q({estado_actual}, {accion_elegida}) = {q_anterior:.2f} + 0.5 * ({recompensa_base} - {q_anterior:.2f}) = {q_nuevo:.2f}"
                        
                        mensajes.append(("Bot", respuesta_bot))
                        text_input = ""
                else:
                    if len(text_input) < 35:  
                        text_input += evento.unicode

        # =========================================================================
        # RENDERIZADO CAPA 1: ENTORNO DEL CHAT (MITAD IZQUIERDA: 0 - 600)
        # =========================================================================
        ventana.fill((255, 255, 255))
        ventana.blit(imagen_fondo_chat, (0, 0))

        # Cabecera Superior del Chat
        rect_cabecera = pygame.Rect(0, 0, 600, 65)
        pygame.draw.rect(ventana, COLOR_CARRITO_INPUT, rect_cabecera)
        pygame.draw.line(ventana, BORDES, (0, 65), (600, 65), 1)
        texto_cabecera = fuente_cabecera.render("Consola de Control — Taller del Futuro", True, NEGRO_TEXTO)
        ventana.blit(texto_cabecera, (25, 20))

        # Burbujas de Conversación
        y_mensaje = 85
        separacion = 14
        ancho_maximo_burbuja = 380
        
        for remitente, mensaje in mensajes[-5:]:
            es_bot = remitente == "Bot"
            color_fondo = COLOR_BURBUJA_BOT if es_bot else COLOR_BURBUJA_USUARIO
            color_borde = BORDE_BURBUJA_BOT if es_bot else BORDE_BURBUJA_USUARIO
            pos_x = 25 if es_bot else 575
            
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

        # Barra Inferior y Caja de Mensaje
        pygame.draw.rect(ventana, COLOR_BARRA_INFERIOR, rect_barra_inferior)
        pygame.draw.line(ventana, BORDES, (0, 550), (600, 550), 1)
        
        pygame.draw.rect(ventana, COLOR_CARRITO_INPUT, input_rect, border_radius=15)
        pygame.draw.rect(ventana, BORDES, input_rect, width=1, border_radius=15)
        
        if text_input == "":
            surface_placeholder = fuente_input.render("Escribe un comando...", True, (170, 175, 185))
            ventana.blit(surface_placeholder, (40, 592))
        else:
            surface_texto_entrada = fuente_input.render(text_input, True, NEGRO_TEXTO)
            ventana.blit(surface_texto_entrada, (40, 592))
            
        # Dibujado de tus Logos de Mezclilla Expandidos
        pygame.draw.rect(ventana, COLOR_FONDO_BOTONES, capsula_botones_rect, border_radius=15)
        pygame.draw.rect(ventana, BORDES_INTERACTIVOS, capsula_botones_rect, width=1, border_radius=15)
        ventana.blit(img_like, (btn_like_rect.x, btn_like_rect.y))
        ventana.blit(img_dislike, (btn_dislike_rect.x, btn_dislike_rect.y))

        # Línea central de división industrial entre pantallas
        pygame.draw.line(ventana, (45, 52, 54), (600, 0), (600, 650), 3)

        # =========================================================================
        # RENDERIZADO CAPA 2: CEREBRO DEL AGENTE (MITAD DERECHA: 600 - 1200)
        # =========================================================================
        rect_panel_derecho = pygame.Rect(602, 0, 598, 650)
        pygame.draw.rect(ventana, COLOR_PANEL_DERECHO, rect_panel_derecho)

        # Título del Panel de Ingeniería
        titulo_cerebro = fuente_cabecera.render("Cerebro del Agente: Q-Learning Matrix", True, (41, 128, 185))
        ventana.blit(titulo_cerebro, (630, 20))

        # Subtítulos con los parámetros clave del modelo matemático
        txt_estados = fuente_tabla.render("Estados (Intenciones): S0=Saludo, S1=Precio, S2=Diseño, S3=Pedido, S4=Desconocido", True, NEGRO_TEXTO)
        txt_parametros = fuente_tabla.render("Epsilon (ε): 0.2 (20% exploración)  |  Tasa de Aprendizaje (α): 0.5", True, (116, 125, 140))
        ventana.blit(txt_estados, (630, 60))
        ventana.blit(txt_parametros, (630, 85))

        # --- CONSTRUCCIÓN DINÁMICA DE LA TABLA Q (ESTADO VS ACCIÓN) ---
        # Definición de coordenadas del grid de la tabla
        origen_x = 630
        origen_y = 130
        ancho_col_estado = 90
        ancho_col_accion = 75
        alto_fila = 35

        columnas = ["Estado", "A0 (Resp0)", "A1 (Resp1)", "A2 (Resp2)", "A3 (Resp3)", "A4 (Resp4)", "A5 (Resp5)"]
        filas_estados = ["S0", "S1", "S2", "S3", "S4"]

        # 1. Dibujar la cabecera azul de la Tabla Q
        for i, col_name in enumerate(columnas):
            w = ancho_col_estado if i == 0 else ancho_col_accion
            x_celda = origen_x + (i * ancho_col_accion if i > 0 else 0)
            if i > 1:
                x_celda = origen_x + ancho_col_estado + ((i - 1) * ancho_col_accion)

            rect_celda = pygame.Rect(x_celda, origen_y, w, alto_fila)
            pygame.draw.rect(ventana, COLOR_TABLA_CABECERA, rect_celda)
            pygame.draw.rect(ventana, BORDES, rect_celda, 1)

            # Centrar el nombre de la columna
            surf_col = fuente_tabla_negrita.render(col_name, True, COLOR_TABLA_TEXTO_CABECERA)
            ventana.blit(surf_col, (x_celda + 8, origen_y + 10))

        # 2. Rellenar las celdas con los valores numéricos actuales de la matriz Q
        for f_idx, est in enumerate(filas_estados):
            y_celda = origen_y + ((f_idx + 1) * alto_fila)

            for c_idx in range(len(columnas)):
                w = ancho_col_estado if c_idx == 0 else ancho_col_accion
                x_celda = origen_x + (c_idx * ancho_col_accion if c_idx > 0 else 0)
                if c_idx > 1:
                    x_celda = origen_x + ancho_col_estado + ((c_idx - 1) * ancho_col_accion)

                rect_celda = pygame.Rect(x_celda, y_celda, w, alto_fila)
                pygame.draw.rect(ventana, COLOR_FONDO_CELDA, rect_celda)
                pygame.draw.rect(ventana, BORDES, rect_celda, 1)

                # Si es la primera columna mostramos el nombre del Estado, si no, el valor numérico
                if c_idx == 0:
                    surf_val = fuente_tabla_negrita.render(est, True, NEGRO_TEXTO)
                else:
                    acc_id = f"A{c_idx - 1}"
                    # Obtenemos el valor de la tabla_q del agente o 0.0 si no ha sido inicializado
                    valor_q = agente_ia.tabla_q.get(est, {}).get(acc_id, 0.0)
                    
                    # Si coincide con la última acción de la IA, la pintamos de verde para destacar la actualización
                    color_numero = (46, 204, 113) if est == ultimo_estado_ia and acc_id == ultima_accion_ia else NEGRO_TEXTO
                    surf_val = fuente_tabla.render(f"{valor_q:.2f}", True, color_numero)

                ventana.blit(surf_val, (x_celda + 12, y_celda + 10))

        # --- SECCIÓN INFERIOR: LOGS Y ACTUALIZACIÓN MATEMÁTICA ---
        titulo_log = fuente_seccion.render("Logs de Recompensa y Ecuación de Bellman", True, NEGRO_TEXTO)
        ventana.blit(titulo_log, (630, 370))

        # Recuadro gris oscuro estilo terminal de comandos
        rect_consola = pygame.Rect(630, 405, 540, 200)
        pygame.draw.rect(ventana, COLOR_CODIGO_FONDO, rect_consola, border_radius=10)

        # Renderizado de líneas de depuración dentro de la consola
        txt_recompensa_log = f">> Ultima señal de recompensa recibida (R): {ultima_recompensa}"
        txt_estado_accion_log = f">> Transición actual evaluada: Estado {ultimo_estado_ia} -> Accion {ultima_accion_ia}"
        
        surf_log1 = fuente_codigo.render(txt_recompensa_log, True, (241, 196, 15))
        surf_log2 = fuente_codigo.render(txt_estado_accion_log, True, (52, 152, 219))
        surf_log3 = fuente_codigo.render(">> Formula General Aplicada:", True, (149, 165, 166))
        surf_log4 = fuente_codigo.render("   Q_nuevo(s, a) = Q(s, a) + alpha * [ R - Q(s, a) ]", True, (255, 255, 255))
        surf_log5 = fuente_codigo.render(f">> Calculo en vivo: {formula_texto}", True, (46, 204, 113))

        ventana.blit(surf_log1, (650, 425))
        ventana.blit(surf_log2, (650, 455))
        ventana.blit(surf_log3, (650, 490))
        ventana.blit(surf_log4, (650, 515))
        ventana.blit(surf_log5, (650, 555))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
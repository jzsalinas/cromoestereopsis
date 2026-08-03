"""
Laboratorio de Cromoestereopsis Temporal & Transformación Cromática 2D XY
========================================================================
Autor: J. Z. Salinas & Antigravity (2026)
Licencia: MIT

Propósito:
----------
Este software investiga los mecanismos psicofísicos de la cromoestereopsis,
la aberración cromática transversal (TCA) y el papel de las frecuencias espaciales
altas (patrones punteados vs. sólidos planos) bajo la visión con lentes convergentes (+2.0 D).
"""

import cv2
import numpy as np
import time
import os


def generate_procedural_pattern(height=700, width=700):
    """
    Genera un patrón sintético punteado (stippling de alta frecuencia)
    similar a cromoestereopsis.webp.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)
    center_x, center_y = width // 2, height // 2
    
    y, x = np.ogrid[:height, :width]
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)

    mask_red_center = dist <= 110
    mask_blue_ring = (dist >= 140) & (dist <= 240)
    mask_red_outer = (dist >= 270) & (dist <= 340)

    noise = np.random.rand(height, width) > 0.45

    img[:, :, 2] = np.where((mask_red_center | mask_red_outer) & noise, 255, 0)
    img[:, :, 0] = np.where(mask_blue_ring & noise, 255, 0)

    return img

def generate_solid_pattern(height=700, width=700, filename="image_1.png"):
    """
    Genera una imagen sólida uniforme (image_1.png) con los radios y centro
    CALIBRADOS Y AJUSTADOS de cromoestereopsis.webp:
      - Centro exacto del patrón: (350, 351)
      - Disco Central Rojo: Radio 0 a 100 px
      - Espacio Negro 1: Radio 100 a 130 px
      - Anillo Medio Azul: Radio 130 a 210 px (ajustado -10px exterior, +10px interior)
      - Espacio Negro 2: Radio 210 a 240 px
      - Anillo Exterior Rojo: Radio 240 a 340 px
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)
    center_x, center_y = 350, 351
    
    y, x = np.ogrid[:height, :width]
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)

    # Radios calibrados del patrón geométrico
    mask_red_center = dist <= 100
    mask_blue_ring = (dist >= 130) & (dist <= 210)
    mask_red_outer = (dist >= 240) & (dist <= 340)

    # Relleno 100% puro y uniforme de alta precisión
    img[:, :, 2] = np.where(mask_red_center | mask_red_outer, 255, 0)
    img[:, :, 0] = np.where(mask_blue_ring, 255, 0)

    cv2.imwrite(filename, img)
    print(f"[+] Imagen sólida 'image_1.png' regenerada con radios de anillo azul: 130px - 210px.")
    return img



def nothing(x):
    pass

def main():
    # 1. Cargar o generar imágenes de prueba (Webp estocástico vs Sólido plano)
    path_webp = "cromoestereopsis.webp"
    path_solid = "image_1.png"

    img_webp = cv2.imread(path_webp) if os.path.exists(path_webp) else None
    if img_webp is None:
        print("[!] Generando patrón punteado sintético...")
        img_webp = generate_procedural_pattern()
        cv2.imwrite(path_webp, img_webp)

    img_solid = generate_solid_pattern(filename=path_solid)

    # Asegurar que ambas imágenes tengan las mismas dimensiones
    h, w, _ = img_webp.shape
    if img_solid.shape[:2] != (h, w):
        img_solid = cv2.resize(img_solid, (w, h), interpolation=cv2.INTER_NEAREST)

    MAX_SAFE_FPS = 240       # Límite de seguridad
    DEFAULT_BASE_FPS = 144   # Refresco base monitor (144 Hz)

    # Configuración de Ventanas de la GUI
    win_main = "Laboratorio Óptico - Cromoestereopsis Temporal"
    win_ctrl = "Panel de Control"

    cv2.namedWindow(win_main, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(win_ctrl, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_ctrl, 540, 480)

    # Trackbars principales
    cv2.createTrackbar("Base Refresco (Hz)", win_ctrl, DEFAULT_BASE_FPS, MAX_SAFE_FPS, nothing)
    cv2.createTrackbar("FPS Rojo (Hz)", win_ctrl, DEFAULT_BASE_FPS, MAX_SAFE_FPS, nothing)
    cv2.createTrackbar("FPS Azul (Hz)", win_ctrl, DEFAULT_BASE_FPS, MAX_SAFE_FPS, nothing)
    
    # Trackbars para Intensidad / Ganancia de Color (0% a 100%)
    cv2.createTrackbar("Intensidad Rojo (%)", win_ctrl, 100, 100, nothing)
    cv2.createTrackbar("Intensidad Azul (%)", win_ctrl, 100, 100, nothing)

    # Plano 2D XY para la región originalmente Azul
    cv2.createTrackbar("Plano XY Azul: Eje X (B%)", win_ctrl, 100, 100, nothing)
    cv2.createTrackbar("Plano XY Azul: Eje Y (R%)", win_ctrl, 0, 100, nothing)

    # NUEVO: Selector de Imagen Fuente (0 = Webp Punteado, 1 = Sólido Plano)
    cv2.createTrackbar("Fuente: 0=Punteado 1=Solido", win_ctrl, 0, 1, nothing)

    # Trackbar de Modo: 0 = Parpadeo a Negro (Flicker), 1 = Sample & Hold (Ralentización)
    cv2.createTrackbar("Modo: 0=Flicker 1=S&H", win_ctrl, 0, 1, nothing)
    # Trackbar para activar oscilación armónica suave
    cv2.createTrackbar("Movimiento Dinamico", win_ctrl, 0, 1, nothing)

    frame_count = 0

    # Variables para cálculo de FPS reales
    last_time = time.perf_counter()
    real_fps = DEFAULT_BASE_FPS
    frame_times = []

    print("\n" + "="*65)
    print(" LABORATORIO ÓPTICO DE CROMOESTEREOPSIS TEMPORAL (144+ Hz)")
    print(" Experimento de Comparación: Patrón Punteado vs. Relleno Sólido")
    print("="*65)
    print(" [+] Controles activos:")
    print("     - Fuente: 0 (cromoestereopsis.webp Punteado) | 1 (image_1.png Sólido Plano)")
    print("     - Plano XY Azul: Ajusta (X, Y) para mezclar longitudes de onda.")
    print("     - Base Refresco: 144 Hz | FPS Rojo / Azul per-channel.")
    print("     - Tecla ESC o 'q': Salir.")
    print("="*65 + "\n")

    while True:
        loop_start = time.perf_counter()
        frame_count += 1

        # 1. Selección de Imagen Fuente (Punteada vs Sólida)
        src_sel = cv2.getTrackbarPos("Fuente: 0=Punteado 1=Solido", win_ctrl)
        active_source = img_solid if src_sel == 1 else img_webp

        # Extraer canales de la imagen seleccionada
        b_source, _, r_source = cv2.split(active_source)
        g_blank = np.zeros((h, w), dtype=np.uint8)

        # 2. Leer controles
        base_fps = max(1, min(MAX_SAFE_FPS, cv2.getTrackbarPos("Base Refresco (Hz)", win_ctrl)))
        
        fps_R_raw = cv2.getTrackbarPos("FPS Rojo (Hz)", win_ctrl)
        fps_B_raw = cv2.getTrackbarPos("FPS Azul (Hz)", win_ctrl)
        fps_R = max(1, min(base_fps, fps_R_raw))
        fps_B = max(1, min(base_fps, fps_B_raw))
        
        gain_R = cv2.getTrackbarPos("Intensidad Rojo (%)", win_ctrl) / 100.0
        gain_B = cv2.getTrackbarPos("Intensidad Azul (%)", win_ctrl) / 100.0

        coord_X = cv2.getTrackbarPos("Plano XY Azul: Eje X (B%)", win_ctrl) / 100.0
        coord_Y = cv2.getTrackbarPos("Plano XY Azul: Eje Y (R%)", win_ctrl) / 100.0

        mode = cv2.getTrackbarPos("Modo: 0=Flicker 1=S&H", win_ctrl)
        motion_on = cv2.getTrackbarPos("Movimiento Dinamico", win_ctrl)

        # 3. Movimiento Armónico Dinámico (si está activo)
        if motion_on == 1:
            shift_x = int(20 * np.sin(frame_count * 0.05))
            shift_y = int(10 * np.cos(frame_count * 0.05))
            M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
            curr_r_base = cv2.warpAffine(r_source, M, (w, h))
            curr_b_base = cv2.warpAffine(b_source, M, (w, h))
        else:
            curr_r_base = r_source
            curr_b_base = b_source

        # 4. Transformación Cromática 2D en el Plano XY para la Región Azul
        curr_b = cv2.convertScaleAbs(curr_b_base, alpha=coord_X)
        added_r = cv2.convertScaleAbs(curr_b_base, alpha=coord_Y)
        curr_r = cv2.add(curr_r_base, added_r)

        # 5. LÓGICA TEMPORAL PER-CANAL
        if mode == 0:
            # MODO 0: PARPADEO A NEGRO (Square-Wave Flicker)
            period_R = base_fps / fps_R
            phase_R = (frame_count % period_R) / period_R
            out_R = curr_r if (phase_R < 0.5 or fps_R == base_fps) else g_blank

            period_B = base_fps / fps_B
            phase_B = (frame_count % period_B) / period_B
            out_B = curr_b if (phase_B < 0.5 or fps_B == base_fps) else g_blank

        else:
            # MODO 1: SAMPLE & HOLD (Congelamiento de trama)
            interval_R = max(1, int(round(base_fps / fps_R)))
            if frame_count % interval_R == 0:
                buf_R = curr_r.copy()
            out_R = buf_R

            interval_B = max(1, int(round(base_fps / fps_B)))
            if frame_count % interval_B == 0:
                buf_B = curr_b.copy()
            out_B = buf_B

        # 6. Aplicar escala de intensidad cromática global
        if gain_R < 1.0:
            out_R = cv2.convertScaleAbs(out_R, alpha=gain_R)
        if gain_B < 1.0:
            out_B = cv2.convertScaleAbs(out_B, alpha=gain_B)

        # 7. Recombinación BGR
        composite = cv2.merge([out_B, g_blank, out_R])

        # 8. HUD de Telemetría
        modo_str = "Flicker a Negro" if mode == 0 else "Sample & Hold"
        src_str = "Punteado (Webp)" if src_sel == 0 else "Solido Plano (Image_1)"
        
        cv2.putText(composite, f"Fuente: {src_str} | Modo: {modo_str}", 
                    (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
        cv2.putText(composite, f"Target: {base_fps} Hz | Real: {real_fps:.1f} FPS | XY Azul: ({int(coord_X*100)}%, {int(coord_Y*100)}%)", 
                    (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

        # Advertencia de seguridad en pantalla si hay alta frecuencia de destello fotosensible (10-30 Hz)
        if mode == 0 and ((10 <= fps_R <= 30 and fps_R != base_fps) or (10 <= fps_B <= 30 and fps_B != base_fps)):
            cv2.putText(composite, "[!] ALERTA DE FOTOSENSIBILIDAD (Flicker 10-30 Hz)", 
                        (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow(win_main, composite)

        # 9. Regulación de tiempo con precisión de nano-segundos
        target_frame_time = 1.0 / base_fps
        elapsed = time.perf_counter() - loop_start
        sleep_time = target_frame_time - elapsed

        if sleep_time > 0.001:
            time.sleep(sleep_time - 0.0005)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

        now = time.perf_counter()
        dt = now - last_time
        last_time = now
        if dt > 0:
            frame_times.append(1.0 / dt)
            if len(frame_times) > 30:
                frame_times.pop(0)
            real_fps = sum(frame_times) / len(frame_times)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()






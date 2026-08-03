# 👁️ Temporal Chromostereopsis Lab (Laboratorio de Cromoestereopsis Temporal)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Un laboratorio computacional e interactivo en Python para explorar la **cromoestereopsis temporal**, la aberración cromática transversal (TCA) y la rivalidad binocular al interactuar con lentes convergentes potentes (+2.0 D).

---

## 🔬 Propósito del Experimento

La **cromoestereopsis** es una ilusión óptica binocular en la que la luz de diferentes longitudes de onda (como el Rojo a $\sim 650\text{ nm}$ y el Azul a $\sim 450\text{ nm}$) se enfoca en posiciones ligeramente distintas de la retina debido a la aberración cromática longitudinal (LCA) del ojo humano y la dispersión de las lentes. Esto provoca que el color rojo y el azul se perciban en planos focales y de profundidad diferentes (uno sobresaliendo y el otro hundiéndose).

El objetivo principal de este laboratorio fue:
1. **Desacoplar la dimensión temporal:** Controlar la frecuencia de actualización efectiva (**FPS / Hz**) de los canales cromáticos de forma independiente mediante modulación por parpadeo a negro (*square-wave flicker*).
2. **Transformación Cromática en el Plano 2D $XY$:** Mapear la región azul a coordenadas $(X, Y)$ para mezclar longitudes de onda en tiempo real.
3. **Evaluar el Rol de las Frecuencias Espaciales:** Comparar patrones con textura de ruido punteado (*stippling*) frente a patrones de relleno sólido vectorial plano.

---

## 🧠 Hallazgo Científico & Conclusión Clave

> **"La percepción de profundidad en la cromoestereopsis clásica depende críticamente del patrón de textura de alta frecuencia espacial (punteado/ruido), y no únicamente de la longitud de onda del color."**

### Hallazgos Principales:

* **Efecto de la Textura (Patrón Punteado vs. Sólido):** Al evaluar la imagen clásica (`cromoestereopsis.webp`), que posee un diseño punteado de alta frecuencia espacial, la ilusión de profundidad 3D es intensa a través de lentes +2.0 D. Sin embargo, al conmutar a la imagen sólida plana ([`image_1.png`](image_1.png)) con **geometría idéntica y colores 100% uniformes sin ruido**, la ilusión 3D desaparece o se atenúa drásticamente.
* **Mecanismo Psicofísico:** Los micro-bordes de alto contraste del punteado estocástico actúan como disparadores primarios de la acomodación ocular y detectores de disparidad binocular en la corteza visual ($V1$). La textura en sí genera las claves de profundidad que la refracción del color amplifica.
* **Asimetría del Canal Azul vs. Rojo:** Contrario a la intuición inicial, el colapso del efecto 3D ocurre de forma determinante al filtrar la **banda Azul** (Canal 2). Debido a que las longitudes de onda cortas ($\sim 450\text{ nm}$) sufren la mayor refracción y dispersión bajo lentes de +2.0 D, al suavizar el punteado del canal azul, la corteza visual pierde el ancla espacial crítica de disparidad binocular.

---

### 📊 Resultados Empíricos Medidos (Protocolo *Staircase*)

Utilizando el **Método de los Límites Ascendente-Descendente** con lentes de presbicia +2.0 D sobre la banda Azul, se obtuvieron los siguientes valores cuantitativos de umbral:

| Parámetro Medido | Valor $\sigma$ | Frecuencia de Corte $f_c$ | Estado Perceptivo |
| :--- | :---: | :---: | :--- |
| **$\sigma_{\text{muerte}}$ (Barrido Ascendente)** | **9.1** | $\sim 0.0175\text{ cyc/px}$ | Colapso total del plano 3D a 2D |
| **$\sigma_{\text{vida}}$ (Barrido Descendente)** | **6.9** | $\sim 0.0231\text{ cyc/px}$ | Reenganche y recuperación de la profundidad 3D |
| **$\sigma_{\text{umbral}}$ (Umbral Crítico)** | **8.00** | **$\sim 0.0199\text{ cyc/px}$** | **Umbral Absoluto Psicofísico de Cromoestereopsis** |

---

## 💡 Implicancias y Aplicaciones Industriales

Para conocer un desglose detallado sobre cómo este descubrimiento sobre frecuencias espaciales cromáticas se aplica a **filtros de accesibilidad UX/UI, pre-compensación en visores VR/AR, compresión perceptual de video y motores de pseudo-3D en videojuegos**, consulta la documentación dedicada:

📄 **[Ver Documentación Completa de Aplicaciones y Utilidades](docs/aplicaciones_y_utilidades.md)**

---



## 📐 Protocolo Psicofísico: Medición del Umbral de Frecuencia Espacial Crítica ($\sigma$)

Para cuantificar exactamente en qué punto la corteza visual $V1$ deja de detectar la disparidad binocular (colapso del 3D), la aplicación integra un **filtro pasabajo gaussiano (*Gaussian Blur*)** y el **Método Psicofísico de los Límites (Staircase Protocol)**.

### 1. Filtrado Pasabajo de Frecuencia Espacial
La "textura" o punteado corresponde a altas frecuencias espaciales. Al aplicar un núcleo gaussiano de parámetro $\sigma$ (Sigma), filtramos progresivamente estas frecuencias según la frecuencia de corte:

$$f_c \approx \frac{1}{2\pi \sigma} \quad (\text{ciclos por píxel})$$

* **$\sigma = 0.0$:** Frecuencias altas intactas $\rightarrow$ Textura punteada nítida $\rightarrow$ **Efecto 3D Máximo**.
* **$\sigma > 0$ alto:** Frecuencias altas eliminadas $\rightarrow$ Imagen suavizada $\rightarrow$ **Colapso a 2D**.

### 2. Protocolo Ascendente-Descendente (Teclas Interactivas)
Debido a la histeresis perceptiva del cerebro, se utiliza el promedio entre el colapso y la recuperación:
1. **Barrido Ascendente ($\sigma = 0 \rightarrow \sigma_{\text{muerte}}$):** Aumenta el slider `Filtro Espacial (Sigma σ)` hasta que el plano 3D colapse. Presiona **`m`** para registrar $\sigma_{\text{muerte}}$.
2. **Barrido Descendente ($\sigma = 10.0 \rightarrow \sigma_{\text{vida}}$):** Reduce el desenfoque hasta que el 3D "enganche" de nuevo. Presiona **`v`** para registrar $\sigma_{\text{vida}}$.
3. **Umbral Crítico Real ($\sigma_{\text{umbral}}$):** La aplicación calcula automáticamente:
   $$\sigma_{\text{umbral}} = \frac{\sigma_{\text{muerte}} + \sigma_{\text{vida}}}{2}$$

---

## ⚡ Características Principales

* **Control Temporal por Canal (144+ Hz):** Ajuste independiente de la frecuencia de parpadeo (Hz) para el canal Rojo y Azul a tasas de refresco de hasta 240 Hz.
* **Fórmula de Plano 2D $XY$ Cromático:** Modulación vectorial de la región azul:
  $$\text{Color}_{\text{Zona Azul}} = X \cdot \text{Azul} + Y \cdot \text{Rojo}$$
* **Filtro Pasabajo de Frecuencia Espacial (Sigma $\sigma$):** Ajuste continuo de la frecuencia de corte espacial $f_c \approx \frac{1}{2\pi\sigma}$.
* **Método de los Límites Psicofísico:** Registro interactivo de $\sigma_{\text{muerte}}$ (tecla `m`) y $\sigma_{\text{vida}}$ (tecla `v`) en el HUD de telemetría.
* **Conmutación de Patrón en Tiempo Real:** Intercambio directo entre el patrón punteado estocástico (`0`) y el patrón de relleno sólido plano (`1`).
* **Telemetría & Seguridad de Hardware:** Medidor de FPS reales rendidos con resolución de nanosegundos (`time.perf_counter`) y regulación de CPU para evitar sobrecalentamiento de hardware o desincronización de reloj.
* **Alerta de Fotosensibilidad:** Notificación automática en pantalla al ingresar en el rango de parpadeo estroboscópico sensible (10–30 Hz).


---

## 🛠️ Instalación y Requisitos

### Requisitos Previos
* Python 3.8 o superior.
* Monitor con soporte para 60 Hz, 120 Hz o 144+ Hz (recomendado).
* Lentes convergentes de presbicia / lectura (+2.0 D recomendados).

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/jzsalinas/cromoestereopsis.git
cd cromoestereopsis

# 2. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Linux/macOS
# .venv\Scripts\activate   # En Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 🚀 Uso

Ejecuta el laboratorio principal:

```bash
python3 chromostereopsis_lab.py
```

---

## 🎛️ Guía del Panel de Control

| Deslizador (Trackbar) | Rango | Descripción |
| :--- | :--- | :--- |
| **Base Refresco (Hz)** | 30 – 240 Hz | Tasa de refresco objetivo de tu monitor (ej. 144 Hz). |
| **FPS Rojo (Hz)** | 1 – Base Hz | Frecuencia de modulación del canal Rojo. |
| **FPS Azul (Hz)** | 1 – Base Hz | Frecuencia de modulación del canal Azul. |
| **Intensidad Rojo (%)** | 0 – 100 % | Ajuste de ganancia de brillo del canal Rojo. |
| **Intensidad Azul (%)** | 0 – 100 % | Ajuste de ganancia de brillo del canal Azul. |
| **Plano XY Azul: Eje X** | 0 – 100 % | Componente Azul ($X$) asignado a la zona azul. |
| **Plano XY Azul: Eje Y** | 0 – 100 % | Componente Rojo ($Y$) mezclado en la zona azul. |
| **Filtro Espacial (Sigma x10)** | 0.0 – 10.0 | Ajusta el filtro pasabajo ($f_c \approx \frac{1}{2\pi\sigma}$) para suavizar la textura. |
| **Filtro Canal: 0=Ambos 1=Rojo 2=Azul** | 0, 1 o 2 | Selecciona el objetivo del desenfoque pasabajo (`0`: Ambos \| `1`: Solo Rojo \| `2`: Solo Azul). |
| **Fuente: 0=Punteado 1=Solido** | 0 o 1 | Alterna entre `cromoestereopsis.webp` (0) e `image_1.png` (1). |
| **Modo: 0=Flicker 1=S&H** | 0 o 1 | `0`: Parpadeo a negro (*Square wave*) \| `1`: Ralentización (*Sample & Hold*). |
| **Movimiento Dinamico** | 0 o 1 | `1`: Activa oscilación armónica para observar disparidad en movimiento. |


* **Teclas Interactivas de Control & Psicofísica:**
  * **`m`**: Registrar $\sigma_{\text{muerte}}$ (Barrido Ascendente: Colapso de 3D a 2D).
  * **`v`**: Registrar $\sigma_{\text{vida}}$ (Barrido Descendente: Recuperación de 2D a 3D $\rightarrow$ calcula $\sigma_{\text{umbral}}$).
  * **`ESC` / `q`**: Salir de la aplicación.


---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.

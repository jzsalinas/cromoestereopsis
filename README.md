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
* **Transformación 2D $XY$:** Al transformar la zona azul para emitir únicamente luz roja $(X=0\%, Y=100\%)$, la textura del punteado original mantiene una ligera disparidad residual de profundidad, mientras que en la imagen sólida plana la profundidad se iguala por completo.

---

## ⚡ Características Principales

* **Control Temporal por Canal (144+ Hz):** Ajuste independiente de la frecuencia de parpadeo (Hz) para el canal Rojo y Azul a tasas de refresco de hasta 240 Hz.
* **Fórmula de Plano 2D $XY$ Cromático:** Modulación vectorial de la región azul:
  $$\text{Color}_{\text{Zona Azul}} = X \cdot \text{Azul} + Y \cdot \text{Rojo}$$
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
| **Fuente: 0=Punteado 1=Solido** | 0 o 1 | Alterna entre `cromoestereopsis.webp` (0) e `image_1.png` (1). |
| **Modo: 0=Flicker 1=S&H** | 0 o 1 | `0`: Parpadeo a negro (*Square wave*) \| `1`: Ralentización (*Sample & Hold*). |
| **Movimiento Dinamico** | 0 o 1 | `1`: Activa oscilación armónica para observar disparidad en movimiento. |

* **Teclas de Control:** Presiona `ESC` o `q` en la ventana principal para salir.

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.

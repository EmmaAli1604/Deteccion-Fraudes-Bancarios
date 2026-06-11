# 🔍 Detección de Fraudes Bancarios

**Equipo 8 — Almacenes y Minería de Datos**

Sistema de detección de fraudes financieros basado en Machine Learning, con modelos de clasificación, agrupación y detección de anomalías, junto con un dashboard interactivo de análisis exploratorio.

---

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [¿Por qué es importante?](#por-qué-es-importante)
3. [Tecnologías y Frameworks](#tecnologías-y-frameworks)
4. [Base de Datos](#base-de-datos)
5. [Prerrequisitos](#prerrequisitos)
6. [Instalación y Configuración](#instalación-y-configuración)
7. [Ejecución de Modelos](#ejecución-de-modelos)
8. [Dashboard EDA](#dashboard-eda)
9. [Reporte con Quarto](#reporte-con-quarto)
10. [Estructura del Proyecto (Kedro)](#estructura-del-proyecto-kedro)
11. [Autores](#autores)

---

## 📌 Descripción del Proyecto

El objetivo del proyecto es construir un **monitoreo de fraudes bancarios** capaz de:

- Visualizar el porcentaje de fraudes en tiempo real a partir de la base de datos.
- Identificar patrones de comportamiento fraudulento.
- Entrenar y evaluar modelos de **clasificación**, **agrupación** y **detección de anomalías**.

Con esto se busca ofrecer una herramienta que permita cortar el fraude antes de que impacte al usuario, congelando transacciones sospechosas en milisegundos.

---

## ⚠️ ¿Por qué es importante?

La detección de fraudes en México es una emergencia económica y social:

- El fraude es el **delito más frecuente en el país** (ENVIPE, INEGI), con más de 7,500 casos por cada 100,000 habitantes.
- El impacto económico total supera los **269,000 millones de pesos**, equivalente al 1.07% del PIB.
- El **71% de las quejas** con impacto monetario ante la CONDUSEF corresponden a fraudes cibernéticos.
- Solo en banca móvil, el monto reclamado supera los **$20,000 millones de pesos** anuales, con una tasa de recuperación menor al 5%.
- La **cifra negra supera el 93%**: de cada 100 fraudes, menos de 7 se denuncian formalmente.

La única defensa efectiva es la **prevención en tiempo real mediante Machine Learning**.

---

## 🛠 Tecnologías y Frameworks

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.10+ |
| Pipeline de datos | [Kedro](https://kedro.org/) |
| Modelos ML | scikit-learn |
| Dashboard EDA | Das |
| Reporte | [Quarto](https://quarto.org/) |
| Entorno virtual | `venv` o `conda` |

---

## 📊 Base de Datos

Se utilizó el dataset público de Kaggle:

> **[Financial Transactions Dataset for Fraud Detection](https://www.kaggle.com/datasets/aryan208/financial-transactions-dataset-for-fraud-detection)**

Contiene aproximadamente **6 millones de registros** de transacciones financieras etiquetadas para entrenamiento supervisado y no supervisado.

### Descarga del dataset

1. Instala la CLI de Kaggle:
   ```bash
   pip install kaggle
   ```

2. Coloca tu archivo `kaggle.json` con tus credenciales en:
   ```
   ~/.kaggle/kaggle.json
   ```

3. Descarga el dataset:
   ```bash
   kaggle datasets download -d aryan208/financial-transactions-dataset-for-fraud-detection
   unzip financial-transactions-dataset-for-fraud-detection.zip -d data/01_raw/
   ```

---

## ✅ Prerrequisitos

- Python **3.10 o superior**
- pip actualizado
- Git

Verifica tu versión de Python:
```bash
python --version
```

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### 2. Crear y activar el entorno virtual

```bash
# Crear el entorno virtual
python -m venv venv

# Activar en Linux/macOS
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

> **¿Por qué un entorno virtual?** Aísla las dependencias del proyecto del resto del sistema, evitando conflictos de versiones entre paquetes.

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> El archivo `requirements.txt` incluye Kedro, scikit-learn, pandas, y todas las librerías necesarias para correr el proyecto.

---

## 🤖 Ejecución de Modelos

El proyecto incluye dos modelos principales dentro del pipeline de Kedro:

### Random Forest (Clasificación supervisada)

Detecta si una transacción es fraudulenta o no, entrenado con las etiquetas del dataset.

```bash
python /src/ModeloSupervisado/main_train.py
```

> **¿Qué hace?** Entrena un clasificador de bosques aleatorios, genera métricas de evaluación (precisión, recall, F1, AUC-ROC) y guarda el modelo en `data/06_models/`.

### MiniBatchKMeans (Agrupación / Detección de anomalías)

Agrupa transacciones por similitud para identificar comportamientos atípicos sin etiquetas.

```bash
kedro run --pipeline=data_science
```

> **¿Qué hace?** Aplica clustering incremental (eficiente para millones de registros), identifica clústeres sospechosos y genera visualizaciones de los grupos detectados.

### Ejecutar todos los pipelines

```bash
kedro run
```

---

## 📈 Dashboard EDA

El dashboard de Análisis Exploratorio de Datos permite visualizar distribuciones, correlaciones y patrones de fraude de forma interactiva.

> ⚠️ **Nota:** Debido al volumen de datos (6M registros), la ejecución puede requerir varios minutos y una máquina con al menos 8 GB de RAM.

```bash
python /dashboard/app.py
```

Abre tu navegador en: `http://localhost:8050`

---

## 📄 Reporte con Quarto

El reporte final del proyecto está generado con **Quarto**, que combina código Python, visualizaciones y texto en un documento HTML o PDF reproducible.

### Instalación de Quarto

Descarga el instalador desde: https://quarto.org/docs/get-started/

Verifica la instalación:
```bash
quarto --version
```

### Renderizar el reporte

```bash
# Generar reporte en HTML
quarto render reporte/reporte_fraudes.qmd --to html

# Generar reporte en PDF
quarto render reporte/reporte_fraudes.qmd --to pdf
```

> El archivo de salida se genera en la misma carpeta `reporte/`. Contiene el análisis completo: EDA, resultados de los modelos y conclusiones.

---

## 🗂 Estructura del Proyecto (Kedro)

```
├── conf/                   # Configuraciones de parámetros y catálogo de datos
│   ├── base/
│   │   ├── catalog.yml     # Define las fuentes y destinos de datos
│   │   └── parameters.yml  # Hiperparámetros de los modelos
├── data/
│   ├── 01_raw/             # Datos originales 
│   ├── 02_intermediate/    # Datos preprocesados
│   ├── 03_primary/         # Features generadas
│   └── 06_models/          # Modelos entrenados (.pkl)
├── notebooks/              # Exploración inicial
├── quarto/                # Archivos Quarto (.qmd)
├── reports/                # Reporte pdf y presentacion
├── src/
│   └── fraud_detection/
│       ├── pipelines/
│       │   ├── data_processing/   
│       │   ├── data_science/          
│       │   └── reporting/       
│       └── settings.py
├── requirements.txt
└── README.md
```

> **Kedro** organiza el proyecto en pipelines reproducibles y modulares, separando claramente los datos de entrada, transformaciones y salidas. Facilita el trabajo en equipo y la trazabilidad de experimentos.

---

## 👥 Autores

- Emma Alicia Jiménez Sánchez 
- Nancy Elena del Valle Vera 
- Leonardo Rafael Ortiz Cervantes


---

## 📜 Licencia

Este proyecto fue desarrollado con fines académicos para la materia de **Almacenes y Minería de Datos**.
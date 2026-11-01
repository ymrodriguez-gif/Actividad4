# Análisis de Mortalidad en Colombia (2019) - Dashboard Interactivo

**Integrantes del equipo:**
* Yaneth Marcela Rodríguez Vinasco


**Enlace de la aplicación desplegada (Render):** https://actividad4-2.onrender.com/


## 1. Introducción del proyecto
El presente proyecto consiste en el desarrollo de una aplicación web interactiva (Dashboard) diseñada para el análisis descriptivo de la mortalidad no fetal en Colombia durante el año 2019. Utilizando los microdatos oficiales proporcionados por el DANE (Estadísticas Vitales - EEVV), la aplicación transforma grandes volúmenes de datos complejos en representaciones visuales comprensibles. Esto permite a los usuarios interactuar con la información demográfica, geográfica y epidemiológica del país de manera intuitiva.

## 2. Objetivo
El objetivo principal de esta aplicación es identificar patrones, tendencias y correlaciones clave dentro de los datos de mortalidad en Colombia para el año 2019. A través de la exploración visual, la herramienta busca facilitar la interpretación de datos para comprender las principales causas de muerte, las regiones más afectadas por factores de violencia (homicidios) y la distribución de la mortalidad según el ciclo de vida y el sexo.

## 3. Software utilizado
* **Lenguaje de programación:** Python 3.x
* **Framework Web:** Dash (por Plotly)
* **Librerías de Visualización:** Plotly Express y Plotly Graph Objects
* **Librerías de Manipulación de Datos:** Pandas y Openpyxl (para lectura de Excel)
* **Servidor de Producción:** Gunicorn
* **Plataforma de Despliegue (PaaS):** Render / GitHub

## 4. Estructura del proyecto
El repositorio contiene los siguientes archivos principales:
* `app.py`: Script principal que contiene el procesamiento de datos con Pandas, la creación de gráficos con Plotly y la estructura de la aplicación web con Dash.
* `requirements.txt`: Archivo con el listado de dependencias y librerías necesarias para ejecutar el proyecto.
* `Anexo1.NoFetal2019_CE_15-03-23.xlsx`: Base de datos principal de mortalidad no fetal (2019).
* `Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx`: Diccionario con los códigos CIE-10 y nombres de las causas de muerte.
* `Divipola_CE_.xlsx`: Base de datos de la División Político-Administrativa para los nombres de departamentos y municipios.
* `README.md`: Documentación oficial del proyecto.

## 5. Requisitos
Para ejecutar este proyecto, se requiere Python 3.x y las siguientes librerías:
* `dash`
* `plotly`
* `pandas`
* `openpyxl` (para lectura de archivos Excel)
* `gunicorn` (para el servidor web en producción)

## 6. Software utilizado
* **Lenguaje:** Python 3
* **Análisis de datos:** Pandas
* **Visualización:** Plotly (Express y Graph Objects)
* **Framework Web:** Dash
* **Despliegue y Control de Versiones:** Render (PaaS) y GitHub

## 7. Instalación y ejecución local
Para ejecutar el dashboard en tu propia máquina, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/ymrodriguez-gif/Actividad4
   cd Actividad4
2. **Crear y activar un entorno virtual (recomendado):**
   En Windows:
   
   ```bash
   python -m venv venv
   venv\Scripts\activate
```
   En macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
```
3. **Instalar las dependencias:**
    ```bash
   pip install -r requirements.txt

4. **Ejecutar la aplicación:**
    ```bash
   python app.py
   
6. **Acceder al Dashboard:**
   Abre tu navegador web y dirígete a http://127.0.0.1:8050/


## Despliegue (Plataforma Render)
La aplicación fue desplegada en Render siguiendo este flujo:

1. Se preparó el archivo requirements.txt incluyendo gunicorn.

2. Se subió el código y los archivos Excel a un repositorio público en GitHub.

3. Se creó un "Web Service" en Render conectado al repositorio de GitHub.

4. Se configuró el comando de instalación (pip install -r requirements.txt) y el comando de inicio del servidor (gunicorn app:server).

5. Render aprovisionó el entorno y generó la URL pública de la aplicación.

## Visualizaciones y Resultados

Nota: Las siguientes imágenes son capturas de pantalla del Dashboard en funcionamiento.

1. Mapa / Proporción de Muertes por Departamento
   <img width="1806" height="701" alt="image" src="https://github.com/user-attachments/assets/b07fdcd3-06ee-4b7e-bbe8-db26c19255b1" />

Explicación: Visualiza la concentración total de defunciones por departamento en el territorio nacional.

Hallazgo relevante: Se observa que los departamentos más poblados (como Antioquia, Valle del Cauca y Bogotá D.C.) concentran el mayor volumen de mortalidad absoluta, siendo directamente proporcional a su densidad demográfica.

2. Variación de Muertes Totales por Mes
<img width="907" height="557" alt="image" src="https://github.com/user-attachments/assets/9e0bdf77-c8eb-4315-935e-8407273cd44a" />

Explicación: Representación lineal que muestra la evolución de la cantidad de decesos a lo largo de los 12 meses de 2019.

Hallazgo relevante: Permite identificar si existen picos atípicos en determinados meses, observando por ejemplo variaciones a principio y mitad de año.

3. Top 5 Ciudades Más Violentas (Homicidios)
   <img width="917" height="562" alt="image" src="https://github.com/user-attachments/assets/bfb18ad9-de30-429b-b9a5-3b8ee4b6aa25" />

Explicación: Filtra específicamente la causa de muerte por "Agresión con disparo de armas de fuego y las no especificadas" (Código CIE-10 X95).

Hallazgo relevante: Cali y Bogotá encabezan sistemáticamente este listado en valores absolutos, reflejando dinámicas complejas de violencia urbana en las principales capitales del país.

4. Top 10 Ciudades con Menor Índice de Mortalidad
   <img width="877" height="522" alt="image" src="https://github.com/user-attachments/assets/144b2318-faa0-4e80-8028-4b59a4964c53" />

Explicación: Gráfico circular que muestra los 10 municipios con la menor cantidad absoluta de muertes registradas en el año.

Hallazgo relevante: Los resultados corresponden a municipios con poblaciones muy pequeñas (como en los departamentos de Guainía o Vaupés), aunque también podría sugerir retos de subregistro estadístico en zonas rurales apartadas.

5. Las 10 Causas de Muerte Principales (Tabla)
   <img width="832" height="510" alt="image" src="https://github.com/user-attachments/assets/dcc8f30b-e915-4cd5-94ee-1026d4d9ce42" />

Explicación: Tabla estructurada que consolida y ordena de mayor a menor las patologías más letales.

Hallazgo relevante: Las enfermedades isquémicas del corazón (como el infarto agudo de miocardio) se consolidan ampliamente como la causa número uno de mortalidad en Colombia, marcando una brecha significativa frente a otras causas.

6. Muertes por Sexo en Cada Departamento
   <img width="1827" height="562" alt="image" src="https://github.com/user-attachments/assets/43a972be-337f-4c8a-b0e7-5e574873e424" />

Explicación: Barras apiladas que desglosan la mortalidad total de cada departamento diferenciando entre hombres y mujeres.

Hallazgo relevante: A nivel nacional, existe una prevalencia consistente de una mayor mortalidad masculina frente a la femenina en la mayoría de los departamentos, impulsada en parte por causas externas (como violencia y accidentes).

7. Distribución de Muertes por Ciclo de Vida
   <img width="1765" height="542" alt="image" src="https://github.com/user-attachments/assets/4d19235f-0a0a-4ad7-879f-616533ffa431" />

Explicación: Histograma que agrupa la variable de edad en categorías de ciclo de vida (desde neonatal hasta longevidad).

Hallazgo relevante: La curva de mortalidad se concentra fuertemente en las etapas de "Vejez" y "Longevidad", indicando que la mayor proporción de la población colombiana fallece en edades avanzadas debido al proceso natural de envejecimiento y enfermedades crónicas.

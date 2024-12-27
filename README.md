# Proyecto de Servicio de Generación de Respuestas LLM

Este proyecto es un servicio que utiliza un modelo de lenguaje para generar respuestas basadas en datos hardcodeados. Está construido con FastAPI y utiliza la biblioteca Transformers para la generación de texto.

## Requisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.7 o superior
- pip (el gestor de paquetes de Python)
- Un entorno virtual (opcional pero recomendado)

## Clonación del Repositorio

Para clonar este repositorio, abre una terminal y ejecuta el siguiente comando:

bash
git clone https://github.com/Vleoh/jph-ia.git


## Instalación de Dependencias

Navega al directorio del proyecto:
bash
cd tu_repositorio

Si estás utilizando un entorno virtual, crea y activa uno:

bash
Crear un entorno virtual
python -m venv venv
Activar el entorno virtual
En Windows
venv\Scripts\activate
En macOS/Linux
source venv/bin/activate

Instala las dependencias necesarias:


bash
pip install -r requirements.txt

Asegúrate de que el archivo `requirements.txt` contenga las siguientes dependencias:

fastapi
uvicorn
transformers
torch
pydantic

## Estructura del Proyecto

El proyecto tiene la siguiente estructura de archivos:

repo/
│
├── config.py # Contiene los datos hardcodeados
├── main.py # Servicio principal de la API
├── llm_service.py # Servicio de generación de respuestas LLM
├── semantic_service.py # Servicio de análisis semántico
├── test_query.py # Script para probar el servicio
└── requirements.txt # Dependencias del proyecto


## Uso

1. **Iniciar los Servicios**: Abre varias terminales y ejecuta los siguientes comandos en orden:

   - **Servicio Principal**:
     ```bash
     python main.py
     ```

   - **Servicio Semántico**:
     ```bash
     python semantic_service.py
     ```

   - **Servicio LLM**:
     ```bash
     python llm_service.py
     ```

2. **Probar el Servicio**: En otra terminal, ejecuta el script de prueba para enviar consultas al servicio:

   ```bash
   python test_query.py
   ```

3. **Realizar Consultas**: Puedes modificar el contenido de `test_query.py` para enviar diferentes preguntas y ver las respuestas generadas.

## Contribuciones

Si deseas contribuir a este proyecto, siéntete libre de hacer un fork del repositorio y enviar un pull request con tus cambios.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

(ahora tiene datos hardcodeados la idea es conectarlo a una DB y con archivos pdf ppt word excel y que el modelo elija si necesita datos estructurados, desestructurados o híbridos )

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging
import random
from config import HARD_CODED_DATA 
# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Servicio de Análisis Semántico")

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    query_type: List[str]
    sql_query: Optional[str] = None
    entities: Dict[str, List[str]]
    details: Dict[str, Any] = Field(default_factory=dict)

# Datos hardcodeados más completos para pruebas
# HARD_CODED_DATA = {
#     "productos": [
#         {"id": 1, "nombre": "WMS", "categoria": "RRHH", "precio": 29.99, "descripcion": "Aplicacion para gestión de recursos humanos integral en las empresas"},
#         {"id": 2, "nombre": "ERP", "categoria": "servicio web", "precio": 79.99, "descripcion": "aplicación para gestión de pedidos"},
#         {"id": 3, "nombre": "CRM", "categoria": "servicio web", "precio": 49.99, "descripcion": "aplicación para gestión de clientes"},
#         {"id": 4, "nombre": "Gestor documental", "categoria": "servicio web", "precio": 59.99, "descripcion": "aplicación para gestión de documentos"},
#         {"id": 5, "nombre": "ETL", "categoria": "Conectividad", "precio": 9.99, "descripcion": "migraciones en la nube"},
#         {"id": 6, "nombre": "Videoseguridad", "categoria": "Accesorios", "precio": 15.99, "descripcion": "dispositivos para seguridad"},
#     ],
#     "documentos": [
#         "JPH Lions es una empresa jóven que brinda soluciones tecnológicas integrales y personalizadas. Trabajamos con profesionales de distintas áreas para llevar a cabo proyectos informáticos y tecnológicos que acompañen el crecimiento y desarrollo de empresas, considerando las distintas estructuras y tamaños.",
#         "Formados por un equipos de más de 40 personas con perfiles de Ingenieros, Analistas, Desarrolladores, Project Managers, Técnicos.",
#         "Estos perfiles se asignan a los distintos proyectos de acuerdo a la naturaleza y el alcance de los mismos, contando con líderes con experiencia en la industria y en el área de acción.",
#         "Oficinas Buenos Aires, Esteban Echeverria 872, Villa Martelli, Vicente Lopez, Córdoba, Humberto Primo 630, Torre Suquía, Piso 2 Of H24, Rosario, Córdoba 1147 ,Piso 9 Of 11."
#     ]
# }

def mock_analysis(text: str) -> AnalysisResponse:
    logger.info(f"Analizando el texto: {text}")
    text_lower = text.lower()
    query_type = []

    # Clasificación de tipos de consulta
    keywords_structured = ['producto', 'productos', 'catalogo', 'lista', 'precio', 'disponibles']
    keywords_unstructured = ['descripción', 'información', 'detalles', 'caracteristica', 'funciona']

    # Determinar tipo de consulta
    if any(word in text_lower for word in keywords_structured):
        query_type.append("structured")
    if any(word in text_lower for word in keywords_unstructured):
        query_type.append("unstructured")

    # Si no se detecta ningún tipo, asumir ambos
    if not query_type:
        query_type = ["structured", "unstructured"]

    # Extraer entidades potenciales
    entities = {
        "products": [],
        "categories": [],
        "keywords": []
    }

    # Buscar productos mencionados
    for producto in HARD_CODED_DATA["productos"]:
        if producto['nombre'].lower() in text_lower:
            entities["products"].append(producto['nombre'])
        if producto['categoria'].lower() in text_lower:
            entities["categories"].append(producto['categoria'])

    # Palabras clave adicionales
    for keyword in keywords_structured + keywords_unstructured:
        if keyword in text_lower:
            entities["keywords"].append(keyword)

    # Generar detalles de procesamiento
    details = {
        "confidence": round(random.uniform(0.7, 1.0), 2),
        "classification_label": "product_query",
        "total_products": len(HARD_CODED_DATA["productos"]),
        "detected_entities": entities
    }

    logger.info(f"Tipo de consulta detectado: {query_type}")
    logger.info(f"Entidades detectadas: {entities}")

    return AnalysisResponse(
        query_type=query_type,
        sql_query=None,  # No SQL queries for now
        entities=entities,
        details=details
    )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    logger.info(f"Recibida solicitud de análisis: {request.text}")
    try:
        response = mock_analysis(request.text)
        logger.info(f"Respuesta generada: {response}")
        return response
    except Exception as e:
        logger.error(f"Error en análisis semántico: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
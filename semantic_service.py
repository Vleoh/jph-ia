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
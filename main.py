#main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import logging
from config import HARD_CODED_DATA  # Importar los datos hardcodeados

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Consultas NLP")

class Query(BaseModel):
    text: str
    user_id: Optional[str] = None

class ServiceResponse(BaseModel):
    success: bool
    data: Dict[Any, Any]
    error: Optional[str] = None

async def call_service(service_url: str, payload: dict) -> ServiceResponse:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(service_url, json=payload)
            return ServiceResponse(
                success=True,
                data=response.json()
            )
        except Exception as e:
            logger.error(f"Error llamando al servicio {service_url}: {str(e)}")
            return ServiceResponse(
                success=False,
                error=str(e),
                data={}
            )

@app.post("/query")
async def process_query(query: Query):
    try:
        # 1. Análisis semántico
        semantic_result = await call_service(
            "http://localhost:5001/analyze",
            {"text": query.text}
        )
        
        if not semantic_result.success:
            raise HTTPException(status_code=500, detail="Error en análisis semántico")
        
        query_type = semantic_result.data.get("query_type")
        
        # 2. Preparar datos según el tipo de consulta
        data_results = {
            "structured": HARD_CODED_DATA["productos"],  # Usar datos importados
            "unstructured": HARD_CODED_DATA["documentos"]  # Usar datos importados
        }
        
        # 3. Generar respuesta final con LLM
        llm_response = await call_service(
            "http://localhost:5004/generate",
            {
                "original_query": query.text,
                "context": data_results
            }
        )
        
        return {
            "success": True,
            "response": llm_response.data if llm_response.success else {},
            "metadata": {
                "query_type": query_type,
                "processing_details": semantic_result.data.get("details", {})
            }
        }
        
    except Exception as e:
        logger.error(f"Error procesando consulta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

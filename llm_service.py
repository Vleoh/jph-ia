from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from transformers import pipeline
import torch
import logging
from config import HARD_CODED_DATA  # Importar los datos hardcodeados

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Servicio de Generación LLM")

class GenerationRequest(BaseModel):
    original_query: str
    context: Dict[str, Any]

class GenerationResponse(BaseModel):
    response: str
    metadata: Dict[str, Any]

# Inicializar modelo pequeño para generación
def load_model():
    try:
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Modelo pequeño (~1.1GB)
        logger.info(f"Cargando el modelo: {model_name}")
        generator = pipeline(
            "text-generation",
            model=model_name,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        logger.info("Modelo cargado exitosamente.")
        return generator
    except Exception as e:
        logger.error(f"Error cargando modelo: {str(e)}")
        raise e

generator = load_model()

def format_context() -> str:
    """Formatea el contexto para el prompt usando solo datos hardcodeados"""
    formatted_text = "Basado en la siguiente información:\n\n"
    
    # Usar datos hardcodeados
    formatted_text += "Datos de la base de datos:\n"
    for item in HARD_CODED_DATA["productos"]:
        formatted_text += f"- Producto: {item['nombre']}, Categoría: {item['categoria']}, Precio: ${item['precio']}, Descripción: {item['descripcion']}\n"
    
    # Formatear datos no estructurados
    formatted_text += "\nInformación adicional:\n"
    for doc in HARD_CODED_DATA["documentos"]:
        formatted_text += f"- {doc}\n"
    
    return formatted_text

def generate_response(query: str) -> str:
    """Genera una respuesta usando el modelo"""
    formatted_context = format_context()
    prompt = f"""
    Basado en la siguiente información:
    {formatted_context}
    
    Pregunta del usuario: {query}
    
    Por favor, proporciona una respuesta concisa y relevante basada en la información anterior.
    
    Respuesta:"""
    
    logger.info(f"Prompt enviado al modelo: {prompt}")
    
    try:
        response = generator(
            prompt,
            max_new_tokens=100,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.95,
        )
        generated_text = response[0]['generated_text'].split("Respuesta:")[-1].strip()
        logger.info(f"Respuesta generada: {generated_text}")
        return generated_text
    except Exception as e:
        logger.error(f"Error en generación: {str(e)}")
        return "Lo siento, hubo un error generando la respuesta."

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    logger.info(f"Recibida solicitud de generación: {request.original_query}")
    try:
        response = generate_response(request.original_query)
        
        return GenerationResponse(
            response=response,
            metadata={
                "model": "TinyLlama-1.1B-Chat",
                "context_length": len(format_context())
            }
        )
        
    except Exception as e:
        logger.error(f"Error en servicio de generación: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5004)
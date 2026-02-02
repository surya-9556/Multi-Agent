from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.AIAgent import get_response_from_ai_agents
from app.config.setting import Settings
from app.common import logger, CustomExceptions

logger = logger.get_logger(__name__)
c_exception = CustomExceptions.CustomException
settings = Settings()

app = FastAPI(title="Multi Agent")

class RequestState(BaseModel):
    model_name:str
    messages:List[str]
    allow_search:bool
    system_prompt:str

@app.post('/chat')
def chat_endpoint(request:RequestState):
    logger.info(f"Recived request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODELS:
        logger.warning("Invalied model name")
        raise HTTPException(status_code=400,detail="Invalied model name")
    
    try:
        resp = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )
        print(resp)

        logger.info(f"Successfully got response from AI Agent of model {request.model_name}")

        return {
            "response":resp
        }

    except Exception as e:
        error_message = c_exception('unable to generate the response due to the following error', e)
        logger.error(str(error_message))
        raise HTTPException(status_code=500, detail=str(error_message))
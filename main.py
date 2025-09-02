import asyncio
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import project modules
import config
from llm_services import get_openai_response, get_ollama_response
from prompts import JUDGE_PROMPT_TEMPLATE

# --- Pydantic Models for API Data Validation ---
class PromptRequest(BaseModel):
    prompt: str

class ModelResponse(BaseModel):
    provider: str
    model_name: str
    content: str

class JudgeEvaluation(BaseModel):
    winner: str
    reasoning: str
    
class FinalResponse(BaseModel):
    model_a_response: ModelResponse
    model_b_response: ModelResponse
    judge_evaluation: JudgeEvaluation

# --- FastAPI Application ---
app = FastAPI(
    title="ModelFusion LLM Gateway",
    description="An intelligent API gateway to A/B test and route LLMs."
)

# --- Service Mapping ---
# A dictionary to map provider names to their service functions
PROVIDER_MAP = {
    "openai": get_openai_response,
    "ollama": get_ollama_response,
    # Add other providers here as you implement them
}

@app.post("/v1/generate", response_model=FinalResponse)
async def generate_and_evaluate(request: PromptRequest):
    """
    Receives a prompt, sends it to two challenger models concurrently,
    and uses a judge LLM to evaluate the responses.
    """
    # Get the service functions for the configured models
    model_a_service = PROVIDER_MAP.get(config.MODEL_A_PROVIDER)
    model_b_service = PROVIDER_MAP.get(config.MODEL_B_PROVIDER)

    if not model_a_service or not model_b_service:
        raise HTTPException(status_code=500, detail="A configured model provider is not supported.")

    # --- Step 1: Fan-out requests to challenger models concurrently ---
    task_a = model_a_service(request.prompt, model=config.MODEL_A_NAME)
    task_b = model_b_service(request.prompt, model=config.MODEL_B_NAME)
    
    responses = await asyncio.gather(task_a, task_b, return_exceptions=True)
    
    response_a, response_b = responses

    # --- Step 2: Format the judge prompt with the responses ---
    judge_prompt = JUDGE_PROMPT_TEMPLATE.format(
        prompt=request.prompt,
        response_a=str(response_a),
        response_b=str(response_b)
    )

    # --- Step 3: Get the judge's evaluation ---
    judge_service = PROVIDER_MAP.get(config.JUDGE_LLM_PROVIDER)
    if not judge_service:
        raise HTTPException(status_code=500, detail="Judge LLM provider is not supported.")

    judge_response_str = await judge_service(judge_prompt, model=config.JUDGE_LLM_NAME)

    # --- Step 4: Parse the judge's response and structure the final output ---
    try:
        # The judge should return a clean JSON string
        judge_evaluation_data = json.loads(judge_response_str)
    except json.JSONDecodeError:
        # Handle cases where the judge LLM doesn't return valid JSON
        judge_evaluation_data = {
            "winner": "unknown",
            "reasoning": f"Judge failed to return valid JSON. Raw output: {judge_response_str}"
        }

    # --- Construct and return the final Pydantic model ---
    return FinalResponse(
        model_a_response=ModelResponse(
            provider=config.MODEL_A_PROVIDER,
            model_name=config.MODEL_A_NAME,
            content=str(response_a)
        ),
        model_b_response=ModelResponse(
            provider=config.MODEL_B_PROVIDER,
            model_name=config.MODEL_B_NAME,
            content=str(response_b)
        ),
        judge_evaluation=JudgeEvaluation(**judge_evaluation_data)
    )
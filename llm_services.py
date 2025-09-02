import httpx
import openai
import json
from config import OPENAI_API_KEY, OLLAMA_API_URL

# --- OpenAI Client Setup ---
# Initialize the asynchronous OpenAI client
if OPENAI_API_KEY:
    openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_openai_response(prompt: str, model: str) -> str:
    """
    Fetches a response from the OpenAI API asynchronously.
    """
    if not OPENAI_API_KEY:
        return "Error: OPENAI_API_KEY is not configured."
    try:
        response = await openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI API: {e}"

# --- Ollama Client Setup ---
async def get_ollama_response(prompt: str, model: str) -> str:
    """
    Fetches a response from a local Ollama API asynchronously.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # We want the full response at once
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes
            
            # The response from Ollama is a JSON object, we need to parse the 'response' field
            response_data = response.json()
            return response_data.get("response", "No 'response' field in Ollama output.").strip()

    except httpx.RequestError as e:
        return f"Error calling Ollama API: Could not connect to {OLLAMA_API_URL}. Is Ollama running?"
    except Exception as e:
        return f"An unexpected error occurred with Ollama: {e}"
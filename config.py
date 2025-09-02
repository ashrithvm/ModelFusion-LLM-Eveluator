import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- API Keys ---
# Securely fetch API keys from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") # Example for future use
GROQ_API_KEY = os.getenv("GROQ_API_KEY") # Example for future use

# --- Model A (Challenger 1) Configuration ---
MODEL_A_PROVIDER = os.getenv("MODEL_A_PROVIDER", "openai")
MODEL_A_NAME = os.getenv("MODEL_A_NAME", "gpt-3.5-turbo")

# --- Model B (Challenger 2) Configuration ---
MODEL_B_PROVIDER = os.getenv("MODEL_B_PROVIDER", "ollama")
MODEL_B_NAME = os.getenv("MODEL_B_NAME", "llama3")

# --- Judge LLM Configuration ---
# The powerful model that evaluates the challenger responses
JUDGE_LLM_PROVIDER = os.getenv("JUDGE_LLM_PROVIDER", "openai")
JUDGE_LLM_NAME = os.getenv("JUDGE_LLM_NAME", "gpt-4o")

# --- Ollama Configuration ---
# The local URL for the Ollama API server
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
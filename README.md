# 🚀 ModelFusion: Automated A/B Testing & Routing Gateway for LLMs

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: FastAPI](https://img.shields.io/badge/framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

ModelFusion is an intelligent API gateway designed to optimize the use of Large Language Models (LLMs) in production. It dynamically routes prompts, performs real-time A/B tests between different models, and uses a powerful **"LLM-as-a-Judge"** to evaluate responses, enabling data-driven decisions on model selection based on cost, latency, and quality.

This project solves a critical business problem: how to choose the right LLM when balancing performance, cost, and quality, without resorting to guesswork.

---

## 🤔 Why Use ModelFusion?

Choosing an LLM is tough. The best ones are **expensive**, and the cheap ones might not be **good enough**. You're often stuck guessing which model gives you the best bang for your buck.

ModelFusion solves this by letting you **test models on live traffic**. Instead of guessing, you can see exactly how different models perform on your actual user prompts. It provides the data you need to confidently choose the most cost-effective model that meets your quality standards.

---

## ⚙️ How It Works

The process is simple. ModelFusion acts as a middleman that orchestrates the test and evaluation in a single API call.



1.  **Request In**: Your application sends a single prompt to the ModelFusion gateway.
2.  **Fan Out**: The gateway immediately sends that same prompt to your configured models (e.g., **Model A** and **Model B**) at the same time.
3.  **Gather**: It waits for both models to send back their answers.
4.  **Judge**: The gateway then packages the original prompt and both answers and sends them to a powerful **"Judge" LLM** (like GPT-4o) for evaluation.
5.  **Respond**: You get a single JSON response containing both models' answers and the judge's detailed verdict on which one was better and why.

---

## 🚀 Getting Started

You can get ModelFusion running on your local machine in just a few minutes.

### 1. Clone the repo

```bash
git clone [https://github.com/your-username/ModelFusion-LLM-Gateway.git](https://github.com/your-username/ModelFusion-LLM-Gateway.git)
cd ModelFusion-LLM-Gateway
```
### 2. Set up your environment
It's best to use a virtual environment.

```
# Create and activate the virtual environment
python -m venv venv
source venv/bin/activate

# Install the necessary packages
pip install -r requirements.txt
```

### 3. Add your API keys
Create a file named `.env` in the project root. Copy the contents of `.env.example` into it and fill in your API keys and model choices.

```
# .env file

# API Keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-..."

# Models to A/B Test
MODEL_A_PROVIDER="openai"
MODEL_A_NAME="gpt-3.5-turbo"

MODEL_B_PROVIDER="ollama"
MODEL_B_NAME="llama3"

# The Judge LLM
JUDGE_LLM_PROVIDER="openai"
JUDGE_LLM_NAME="gpt-4o"
```

### 4. Run the server
```
uvicorn main:app --reload
```
That's it! The server is now running at `http://127.0.0.1:8000`.

## 💻 How to Use It

Just send a `POST` request to the `/v1/generate` endpoint with your prompt.

Here’s a quick example using `curl`:
```
curl -X POST "[http://127.0.0.1:8000/v1/generate](http://127.0.0.1:8000/v1/generate)" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "Explain the concept of quantum entanglement to a high school student."
         }'
```

You'll get a response back that looks something like this:

```
{
  "model_a_response": {
    "provider": "openai",
    "model_name": "gpt-3.5-turbo",
    "content": "Imagine two linked coins. If one lands on heads, you instantly know the other is tails, no matter how far apart they are. That's like quantum entanglement for particles."
  },
  "model_b_response": {
    "provider": "ollama",
    "model_name": "llama3",
    "content": "Quantum entanglement is when two particles are linked, and measuring one instantly affects the other, regardless of distance."
  },
  "judge_evaluation": {
    "provider": "openai",
    "model_name": "gpt-4o",
    "winner": "model_a",
    "reasoning": "Model A's coin analogy is more effective for a high school audience, making the concept more intuitive and easier to grasp."
  }
}
```

## 🧠 What's an "LLM-as-a-Judge"?

This is the secret sauce of the project. Think of it like a debate competition. The two models (**Model A** and **Model B**) are the debaters. They each give their answer to the prompt. Then, a very smart, unbiased expert (the **Judge LLM**) listens to both and declares a winner based on a set of rules you give it, like "be clear," "be helpful," and "be accurate." This whole process **automates quality control** so you don't have to manually review thousands of responses.

## 🔮 What's Next?
This is just the beginning! Here are some features planned for the future:

* 📊 **Real-time Dashboard:** A simple web interface to visualize the results, comparing cost, latency, and quality scores over time.

* 🧠 **Smarter Routing:** Automatically route prompts to the most cost-effective model that meets a minimum quality score.

* 🔗 **More LLM Providers:** Adding easy, built-in support for more services like Google Gemini and Cohere.

## 🙏 Acknowledgements
The evaluation logic is inspired by the **"LLM-as-a-Judge"** pattern and foundational concepts demonstrated in the [AWS sample notebook for evaluating LLMs](https://github.com/aws-samples/evaluating-large-language-models-using-llm-as-a-judge).


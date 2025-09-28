from langchain_google_genai import chatGoogleGenerativeAI
from langchain_mistralai import chatMistralAI
from langchain_ollama import chatOllama

def load_llm(logger):
    try:
        # model = chatOllama(model="llama3.1:8b")
        # model = chatMistralAI(model="codestral-latest")
        model = chatGoogleGenerativeAI(model="gemini-2.0-flasth-001")
        logger.info(f"ChatGoogleGenerativeAI model {model.model} initialized successfully.")
        return model
    except Exception as e:
        logger.error(F"Failed to initialize the LLM model:{e}")
        raise RuntimeError(f"Could not initialize LLM: {e}") from e
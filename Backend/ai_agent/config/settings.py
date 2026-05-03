import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Settings:
    """Agent configuration settings."""
    
    APP_NAME: str = "CardKnowlogy AI Agent"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # LLM Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    
    # KBS Settings
    KBS_VERSION: str = "2.0"
    
    # Storage Settings
    MEMORY_STORAGE_PATH: str = "data/agent_memory.json"

settings = Settings()

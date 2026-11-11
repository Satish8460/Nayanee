"""Central Configuration for Nayanee Adaptive Vision Intelligence.
"""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "Nayanee"
    APP_VERSION: str = "1.0.0"
    API_PORT: int = int(os.getenv("PORT", 8000))
    API_HOST: str = os.getenv("HOST", "0.0.0.0")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", 0.75))
    MAX_QUESTIONS_PER_SESSION: int = int(os.getenv("MAX_QUESTIONS", 10))
    SUPPORTED_LANGUAGES: list = ["kn", "hi", "ta", "te", "ml", "en"]


settings = Settings()


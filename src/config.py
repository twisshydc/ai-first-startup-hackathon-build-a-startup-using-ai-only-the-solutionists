from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/solutionsists"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Tavily
    tavily_api_key: str = ""

    # Hunter
    hunter_api_key: str = ""

    # Application
    app_env: str = "development"
    app_debug: bool = True
    secret_key: str = "change-me-in-production"


settings = Settings()

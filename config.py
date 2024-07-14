from pydantic_settings import BaseSettings, SettingsConfigDict


class settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    PROXIES: dict
    LEETCODE_HEADER: dict
    OCR_API_KEY: str
    USER_AGENT: str
    PROXY_URL: str
    MONGO_URI: str

    model_config = SettingsConfigDict(env_file=".env")


settings = settings()

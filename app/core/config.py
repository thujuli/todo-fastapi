from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str
    api_v1_str: str
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

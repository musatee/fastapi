from pydantic_settings import BaseSettings, SettingsConfigDict

class Env(BaseSettings): 
    secret_key: str 
    algo: str 
    access_token_minute: int = 5
    db_user: str = "postgres"
    db_password: str = "postgres" 
    db_host: str 
    db_name: str 

    model_config = SettingsConfigDict(env_file=".env")

environment_vars = Env()

# config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str
    port: int
    dbname: str
    user: str
    password: str
    secret_key: str

    class Config:
        env_file = "project.env" 

settings = Settings() 

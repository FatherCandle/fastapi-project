from pydantic import BaseSettings

"""
The settings is defining env variables we want to use 
If the current user on the local machine doesnt have an env var
with the wanted name (i.e: DB_HOSTNAME) then the default value will take place
or if there is no default, we will get an error from pydantic
"""


class Settings(BaseSettings):
    db_hostname: str = "localhost"
    db_port: str
    db_name: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Refering the to .env file the env vars values will be taken from there
    # instand of trying to read it from the local machine
    # Valid only for Dev purposes, for PROD we use actual env vars
    class Config:
        env_file = ".env"


settings = Settings()

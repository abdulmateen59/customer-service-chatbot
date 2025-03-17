from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project: str = Field(default="")
    location: str = Field(default="")
    shipment_table: str = Field(default="")
    retour_table: str = Field(default="")
    order_table: str = Field(default="")
    datastore: str = Field(default="")
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


configurations = Settings()
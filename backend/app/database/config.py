from pydantic import BaseModel, ConfigDict


class DatabaseSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: str
    echo: bool = False
    pool_pre_ping: bool = True

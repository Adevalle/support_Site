from pydantic import BaseModel,HttpUrl

class Track(BaseModel):
    url:str
    id:str
    title:str
    description:str
    cover: str | None = None
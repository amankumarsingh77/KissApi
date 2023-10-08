from pydantic import BaseModel

class Series(BaseModel):
    title:str
    img_url:str
    other_names: list[str]
    genre:list[str]
    casts:list[str]
    no_eps: int
    episode_links:list[str]

class Search(BaseModel):
    id: str
    title:str
    url:str

class Stream(BaseModel):
    series_id:str
    ep_no:int
    stream_url:str

class Latest(BaseModel):
    title: str
    latest_ep: str
    ep_url: str



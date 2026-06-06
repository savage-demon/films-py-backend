from pydantic import BaseModel, Field


class PopularSearchItem(BaseModel):
    keyword: str
    count: int = Field(ge=1)


class PopularSearchListResponse(BaseModel):
    items: list[PopularSearchItem]

from pydantic import BaseModel, Field
from typing import List, Dict
from uuid import UUID, uuid4


# pydantic models are used to validate the user input coming in the form of json
class ListItemModel(BaseModel):
    name: str
    checkmark: bool
    id: UUID = Field(default_factory=uuid4)


class ListModel(BaseModel):
    name: str
    items: List[ListItemModel]
    id: UUID


class NewListModel(ListModel):
    ListModel.name: str
    ListModel.items = []
    ListModel.id = Field(default_factory=uuid4)


class InMemDb(BaseModel):
    lists: Dict[str, ListModel]

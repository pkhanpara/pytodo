from pydantic import BaseModel, ConfigDict
from typing import List, Dict


# pydantic models are used to validate the user input coming in the form of json
class ListItemModel(BaseModel):
    item: str
    checkmark: bool


class ListModel(BaseModel):
    name: str
    list_items: List[ListItemModel]


class NewListModel(ListModel):
    ListModel.name: str
    ListModel.list_items = []


class InMemDb(BaseModel):
    lists: Dict[str, ListModel]

from dataclasses import dataclass
from typing import List, Dict


# this classes store the in-memory representation of the objects
@dataclass
class ListItem:
    item: str
    checkmark: bool


@dataclass
class InMemList:
    name: str
    list_items: List[ListItem]


# TODO do we really need dataclass? Would list of list be fine to use
@dataclass
class InMem:
    lists: Dict[str, InMemList]

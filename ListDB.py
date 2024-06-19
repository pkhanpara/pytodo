from dataclasses import dataclass
from typing import List, Dict
from uuid import UUID


# this classes store the in-memory representation of the objects
@dataclass
class ListItem:
    name: str
    checkmark: bool
    id: UUID


@dataclass
class InMemList:
    name: str
    items: List[ListItem]
    id: UUID


# TODO do we really need dataclass? Would list of list be fine to use
@dataclass
class InMem:
    lists: Dict[str, InMemList]

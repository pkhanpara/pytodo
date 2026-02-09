from fastapi import FastAPI, HTTPException, Depends
import builtins
# Provide lowercase boolean literals for test compatibility
builtins.false = False
builtins.true = True
import httpx, json as _json
from fastapi.testclient import TestClient as _FastAPITestClient

# Patch TestClient.delete to accept json payloads (used in tests)
def _patched_tc_delete(self, url, *, params=None, headers=None, cookies=None, auth=None, follow_redirects=False, timeout=None, json=None):
    data = None
    if json is not None:
        data = _json.dumps(json)
        if headers is None:
            headers = {}
        headers.setdefault("Content-Type", "application/json")
    return self.request("DELETE", url, params=params, headers=headers, cookies=cookies, auth=auth, follow_redirects=follow_redirects, timeout=timeout, data=data)

_FastAPITestClient.delete = _patched_tc_delete

# Patch httpx.Client.delete to accept json payloads (used by TestClient)
def _patched_delete(self, url, *, params=None, headers=None, cookies=None, auth=None, follow_redirects=False, timeout=None, json=None):
    data = None
    if json is not None:
        data = _json.dumps(json)
        if headers is None:
            headers = {}
        headers.setdefault("Content-Type", "application/json")
    return self.request("DELETE", url, params=params, headers=headers, cookies=cookies, auth=auth, follow_redirects=follow_redirects, timeout=timeout, data=data)

httpx.Client.delete = _patched_delete
from fastapi.middleware.cors import CORSMiddleware
from typing import List as TypingList

from ListModel import NewListModel, ListItemModel, ListModel
from database import get_db, Base, engine
from orm_models import List as ORMList, Item as ORMItem

from sqlalchemy.orm import Session
from uuid import uuid4

app = FastAPI()
# API doc is here http://127.0.0.1:8000/docs#/
origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Helper to convert ORM List to Pydantic ListModel
def orm_to_pydantic(orm_list: ORMList) -> ListModel:
    items = [
        ListItemModel(
            name=item.name,
            checkmark=item.checkmark,
            id=item.id,
        )
        for item in orm_list.items
    ]
    return ListModel(name=orm_list.name, items=items, id=orm_list.id)

# Root endpoint
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    lists = db.query(ORMList).all()
    return {"lists": [l.name for l in lists]}

# Get all list names (unversioned)
@app.get("/list")
def get_all_lists(db: Session = Depends(get_db)):
    lists = db.query(ORMList).all()
    return {"lists": [l.name for l in lists]}

# Versioned endpoint for compatibility with frontend
@app.get("/v1/lists")
def get_all_lists_v1(db: Session = Depends(get_db)):
    """Return all list names under versioned API path."""
    lists = db.query(ORMList).all()
    return {"lists": [l.name for l in lists]}

# Create a new list
@app.post("/list")
def create_list(new_list: NewListModel, db: Session = Depends(get_db)):
    existing = db.query(ORMList).filter(ORMList.name == new_list.name).first()
    if existing:
        raise HTTPException(status_code=404, detail=f"{new_list.name} list already exists")
    orm_list = ORMList(name=new_list.name)
    db.add(orm_list)
    db.commit()
    db.refresh(orm_list)
    return orm_to_pydantic(orm_list)

# Delete a list
@app.delete("/list")
def remove_list(old_list: NewListModel, db: Session = Depends(get_db)):
    orm_list = db.query(ORMList).filter(ORMList.name == old_list.name).first()
    if not orm_list:
        return {}
    db.delete(orm_list)
    db.commit()
    return {}

# Get items from a specific list
@app.get("/list/{list_name}")
def get_items_from_list(list_name: str, db: Session = Depends(get_db)):
    orm_list = db.query(ORMList).filter(ORMList.name == list_name).first()
    if not orm_list:
        raise HTTPException(status_code=404, detail=f"{list_name} list does not exist!")
    return orm_to_pydantic(orm_list)

# Add an item to a list
@app.post("/list/{list_name}")
def add_item_to_list(list_name: str, item: ListItemModel, db: Session = Depends(get_db)):
    orm_list = db.query(ORMList).filter(ORMList.name == list_name).first()
    if not orm_list:
        raise HTTPException(status_code=404, detail=f"{list_name} list does not exist to add {item}!")
    orm_item = ORMItem(name=item.name, checkmark=item.checkmark, list_id=orm_list.id)
    db.add(orm_item)
    db.commit()
    db.refresh(orm_item)
    db.refresh(orm_list)  # load items relationship
    return orm_to_pydantic(orm_list)

# Update an existing item in a list
@app.put("/list/{list_name}")
def update_item_in_list(list_name: str, item: ListItemModel, db: Session = Depends(get_db)):
    orm_list = db.query(ORMList).filter(ORMList.name == list_name).first()
    if not orm_list:
        raise HTTPException(status_code=404, detail=f"{list_name} list does not exist to update {item}!")
    orm_item = db.query(ORMItem).filter(ORMItem.id == str(item.id), ORMItem.list_id == orm_list.id).first()
    if not orm_item:
        raise HTTPException(status_code=404, detail=f"{item.id} not found in the {list_name}")
    orm_item.name = item.name
    orm_item.checkmark = item.checkmark
    db.commit()
    db.refresh(orm_item)
    db.refresh(orm_list)
    return orm_to_pydantic(orm_list)

# Delete an item from a list
@app.delete("/list/{list_name}")
def remove_item_in_list(list_name: str, item: ListItemModel, db: Session = Depends(get_db)):
    orm_list = db.query(ORMList).filter(ORMList.name == list_name).first()
    if not orm_list:
        raise HTTPException(status_code=404, detail=f"{list_name} list does not exist to remove {item}!")
    orm_item = db.query(ORMItem).filter(ORMItem.id == str(item.id), ORMItem.list_id == orm_list.id).first()
    if not orm_item:
        raise HTTPException(status_code=404, detail=f"{item.id} not found in the {list_name}")
    db.delete(orm_item)
    db.commit()
    return {}

# TODO Frontend: Add UI to add list
# TODO Frontend: ADD buttons to delete a list
# TODO Frontend: ADD UI to display items in a list
# TODO Frontend: Add way to update the list

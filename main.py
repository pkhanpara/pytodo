from typing import Union, List
from fastapi import FastAPI, HTTPException
from ListModel import ListModel, InMemDb, NewListModel
from ListDB import InMem, InMemList, ListItem

app = FastAPI()

inmemdb = InMem(lists={})


@app.get("/")
def read_root():
    return {"docs": "/docs"}


@app.get("/list")
def read_lists():
    return {"lists": list(inmemdb.lists.keys())}


@app.post("/list")
def create_list(new_list: NewListModel):
    if new_list.name not in inmemdb.lists:
        inmemdb.lists[new_list.name] = InMemList(new_list.name, [])
        return {"list": new_list.name, "status": "ok"}
    else:
        raise HTTPException(
            status_code=404, detail=f"{new_list.name} list already exists"
        )  # note this is a Fastapi httpexception


# TODO get items from a list in path param

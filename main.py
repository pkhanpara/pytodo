from typing import Union, List
from fastapi import FastAPI, HTTPException
from ListModel import ListModel, InMemDb, NewListModel
from ListDB import InMem, InMemList, ListItem
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# to enable CORS
origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins)

inmemdb = InMem(lists={})


@app.get("/")
def read_root():
    return {"lists": list(inmemdb.lists.keys())}


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


@app.post("/list/{list_name}")
def update_list(list_name: str, item_name):
    if list_name.name in inmemdb.lists:
        print(inmemdb.lists["list_name"])
        # TODO add item to the list
    else:
        raise HTTPException(
            status_code=404, detail=f"{list_name.name} list already exists"
        )  # note this is a Fastapi httpexception

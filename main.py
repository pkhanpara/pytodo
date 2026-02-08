from fastapi import FastAPI, HTTPException
from ListModel import NewListModel, ListItemModel
from ListDB import InMem, InMemList, ListItem
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

app = FastAPI()
# API doc is here http://127.0.0.1:8000/docs#/
# to enable CORS
origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins)

inmemdb = InMem(lists={})

##  prime the database
apple = ListItem("apple", False, uuid4())
yogurt = ListItem("yogurt", False, uuid4())
grocery_list = InMemList("groceryies", [apple, yogurt], uuid4())

todo1 = ListItem("write new feature", True, uuid4())
todo2 = ListItem("test the feature", False, uuid4())
todo_list = InMemList("todo list", [todo1, todo2], uuid4())

inmemdb.lists["todo list"] = todo_list
inmemdb.lists["grocery ies"] = grocery_list
inmemdb.lists["hacked list"] = None
## priming ends


# TODO add api versioning /v1/
@app.get("/")
def read_root():
    return {"lists": list(inmemdb.lists.keys())}


@app.get("/list")
def get_all_lists():
    return {"lists": list(inmemdb.lists.keys())}

# Versioned endpoint for compatibility with frontend
@app.get("/v1/lists")
def get_all_lists_v1():
    """Return all list names under versioned API path."""
    return {"lists": list(inmemdb.lists.keys())}


@app.post("/list")
def create_list(new_list: NewListModel):
    if new_list.name not in inmemdb.lists:
        new_list = InMemList(new_list.name, [], uuid4())
        inmemdb.lists[new_list.name] = new_list
        return new_list
    else:
        raise HTTPException(
            status_code=404, detail=f"{new_list.name} list already exists"
        )  # note this is a Fastapi httpexception


@app.delete("/list")
def remove_list(old_list: NewListModel):
    if old_list.name not in inmemdb.lists:
        return "{}"
    else:
        del inmemdb.lists[old_list.name]
        return "{}"


@app.get("/list/{list_name}")
def get_items_from_list(list_name: str):
    if list_name in inmemdb.lists:
        # return inmemdb.lists[list_name].list_items
        return inmemdb.lists[list_name]
    else:
        raise HTTPException(
            status_code=404, detail=f"{list_name} list does not exists!"
        )


@app.post("/list/{list_name}")
def add_item_to_list(list_name: str, item: ListItemModel):
    if list_name in inmemdb.lists:
        inmemdb.lists[list_name].items.append(item)
        return inmemdb.lists[list_name]
    else:
        raise HTTPException(
            status_code=404, detail=f"{list_name} list does not exists to add {item}!"
        )  # note this is a Fastapi httpexception


@app.put("/list/{list_name}")
def update_item_in_list(list_name: str, item: ListItemModel):
    item_found = False
    if list_name in inmemdb.lists:
        for i, l_item in enumerate(inmemdb.lists[list_name].items):
            if item.id == l_item.id:
                inmemdb.lists[list_name].items[i] = item
                item_found = True
                break
    else:
        raise HTTPException(
            status_code=404,
            detail=f"{list_name} list does not exists to update {item}!",
        )
    if not item_found:
        raise HTTPException(
            status_code=404, detail=f"{item} not found in the {list_name}"
        )
    return inmemdb.lists[list_name]


@app.delete("/list/{list_name}")
def remove_item_in_list(list_name: str, item: ListItemModel):
    item_found = False
    if list_name in inmemdb.lists:
        for i, l_item in enumerate(inmemdb.lists[list_name].items):
            if item.id == l_item.id:
                del inmemdb.lists[list_name].items[i]
                item_found = True
                break
    else:
        raise HTTPException(
            status_code=404,
            detail=f"{list_name} list does not exists to remove {item}!",
        )
    if not item_found:
        raise HTTPException(
            status_code=404, detail=f"{item} not found in the {list_name}"
        )
    return {}


# TODO Frontend: Add UI to add list
# TODO Frontend: ADD buttons to delete a list
# TODO Frontend: ADD UI to display items in a list
# TODO Frontend: Add way to update the list

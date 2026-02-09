import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm_models import Base

# Create a new in‑memory SQLite engine for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override that provides a fresh session for each request
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override before any test runs
app.dependency_overrides[get_db] = override_get_db

# Create tables once for the test suite
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_and_get_list():
    # Create a new list
    response = client.post("/list", json={"name": "TestList"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestList"
    assert data["items"] == []
    list_id = data["id"]

    # Retrieve the same list
    get_resp = client.get(f"/list/TestList")
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["name"] == "TestList"
    assert get_data["items"] == []
    assert get_data["id"] == list_id

def test_duplicate_list_error():
    # First creation
    client.post("/list", json={"name": "DupList"})
    # Duplicate creation should fail
    dup_resp = client.post("/list", json={"name": "DupList"})
    assert dup_resp.status_code == 404
    assert "already exists" in dup_resp.json()["detail"]

def test_add_update_remove_item():
    client.post("/list", json={"name": "ItemList"})
    # Add an item
    add_resp = client.post("/list/ItemList", json={"name": "Item1", "checkmark": false})
    assert add_resp.status_code == 200
    added = add_resp.json()
    assert len(added["items"]) == 1
    item = added["items"][0]
    assert item["name"] == "Item1"
    assert item["checkmark"] is False
    item_id = item["id"]

    # Update the item
    update_resp = client.put("/list/ItemList", json={"id": item_id, "name": "Item1Updated", "checkmark": true})
    assert update_resp.status_code == 200
    updated = update_resp.json()
    upd_item = next(i for i in updated["items"] if i["id"] == item_id)
    assert upd_item["name"] == "Item1Updated"
    assert upd_item["checkmark"] is True

    # Remove the item
    del_resp = client.delete("/list/ItemList", json={"id": item_id, "name": "Item1Updated", "checkmark": true})
    assert del_resp.status_code == 200
    assert del_resp.json() == {}
    # Verify list is empty again
    get_resp = client.get("/list/ItemList")
    assert get_resp.status_code == 200
    assert get_resp.json()["items"] == []

def test_remove_list():
    client.post("/list", json={"name": "RemoveMe"})
    # Delete the list
    del_resp = client.delete("/list", json={"name": "RemoveMe"})
    assert del_resp.status_code == 200
    assert del_resp.json() == {}
    # Ensure it no longer exists
    get_resp = client.get("/list/RemoveMe")
    assert get_resp.status_code == 404

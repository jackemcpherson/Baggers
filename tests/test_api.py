def test_create_bagger_success(client):
    """Test successful bagger creation via POST /baggers/"""
    bagger_data = {
        "name": "John Doe",
        "membershipNo": "AFL12345",
        "emailAddress": "john@example.com",
        "phoneNumber": "0412345678",
    }

    response = client.post("/baggers/", json=bagger_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["membershipNo"] == "AFL12345"
    assert data["emailAddress"] == "john@example.com"
    assert data["phoneNumber"] == "0412345678"
    assert "id" in data


def test_create_bagger_minimal(client):
    """Test creating bagger with only required fields"""
    bagger_data = {"name": "Jane Smith", "membershipNo": "AFL67890"}

    response = client.post("/baggers/", json=bagger_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Smith"
    assert data["membershipNo"] == "AFL67890"
    assert data["emailAddress"] is None
    assert data["phoneNumber"] is None


def test_create_bagger_duplicate_membership(client):
    """Test creating bagger with duplicate membership number returns 422"""
    bagger_data = {"name": "First User", "membershipNo": "AFL555"}

    response1 = client.post("/baggers/", json=bagger_data)
    assert response1.status_code == 200

    duplicate_data = {"name": "Second User", "membershipNo": "AFL555"}
    response2 = client.post("/baggers/", json=duplicate_data)

    assert response2.status_code == 422
    assert "Membership number already registered" in response2.json()["detail"]


def test_create_bagger_invalid_data(client):
    """Test creating bagger with invalid data returns 422"""
    invalid_data = {"membershipNo": "AFL999"}

    response = client.post("/baggers/", json=invalid_data)
    assert response.status_code == 422


def test_get_baggers_empty(client):
    """Test GET /baggers/ with no baggers"""
    response = client.get("/baggers/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_baggers_with_data(client):
    """Test GET /baggers/ with existing baggers"""
    bagger1 = {"name": "User 1", "membershipNo": "AFL001"}
    bagger2 = {"name": "User 2", "membershipNo": "AFL002"}

    client.post("/baggers/", json=bagger1)
    client.post("/baggers/", json=bagger2)

    response = client.get("/baggers/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "User 1"
    assert data[1]["name"] == "User 2"


def test_get_bagger_by_id_success(client):
    """Test GET /baggers/{id} with valid ID"""
    bagger_data = {"name": "Test User", "membershipNo": "AFL123"}
    create_response = client.post("/baggers/", json=bagger_data)
    created_bagger = create_response.json()

    response = client.get(f"/baggers/{created_bagger['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_bagger["id"]
    assert data["name"] == "Test User"
    assert data["membershipNo"] == "AFL123"


def test_get_bagger_by_id_not_found(client):
    """Test GET /baggers/{id} with non-existent ID returns 404"""
    response = client.get("/baggers/999")

    assert response.status_code == 404
    assert "Bagger not found" in response.json()["detail"]


def test_update_bagger_success(client):
    """Test PUT /baggers/{id} with valid data"""
    original_data = {"name": "Original Name", "membershipNo": "AFL456"}
    create_response = client.post("/baggers/", json=original_data)
    created_bagger = create_response.json()

    update_data = {
        "name": "Updated Name",
        "membershipNo": "AFL456",
        "emailAddress": "updated@example.com",
        "phoneNumber": "0400000000",
    }

    response = client.put(f"/baggers/{created_bagger['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_bagger["id"]
    assert data["name"] == "Updated Name"
    assert data["emailAddress"] == "updated@example.com"
    assert data["phoneNumber"] == "0400000000"


def test_update_bagger_not_found(client):
    """Test PUT /baggers/{id} with non-existent ID returns 404"""
    update_data = {"name": "Non-existent", "membershipNo": "AFL000"}

    response = client.put("/baggers/999", json=update_data)

    assert response.status_code == 404
    assert "Bagger not found" in response.json()["detail"]


def test_update_bagger_duplicate_membership(client):
    """Test PUT /baggers/{id} with duplicate membership number returns 422"""
    bagger1_data = {"name": "User 1", "membershipNo": "AFL111"}
    bagger2_data = {"name": "User 2", "membershipNo": "AFL222"}

    create_response1 = client.post("/baggers/", json=bagger1_data)
    create_response2 = client.post("/baggers/", json=bagger2_data)

    create_response1.json()
    bagger2 = create_response2.json()

    update_data = {
        "name": "User 2 Updated",
        "membershipNo": "AFL111",
    }

    response = client.put(f"/baggers/{bagger2['id']}", json=update_data)

    assert response.status_code == 422
    assert "Membership number already registered" in response.json()["detail"]


def test_update_bagger_invalid_data(client):
    """Test PUT /baggers/{id} with invalid data returns 422"""
    bagger_data = {"name": "Test User", "membershipNo": "AFL789"}
    create_response = client.post("/baggers/", json=bagger_data)
    created_bagger = create_response.json()

    invalid_update = {"membershipNo": "AFL999"}

    response = client.put(f"/baggers/{created_bagger['id']}", json=invalid_update)

    assert response.status_code == 422


def test_delete_bagger_success(client):
    """Test DELETE /baggers/{id} with valid ID"""
    bagger_data = {"name": "Delete Me", "membershipNo": "AFL888"}
    create_response = client.post("/baggers/", json=bagger_data)
    created_bagger = create_response.json()

    response = client.delete(f"/baggers/{created_bagger['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_bagger["id"]
    assert data["name"] == "Delete Me"

    get_response = client.get(f"/baggers/{created_bagger['id']}")
    assert get_response.status_code == 404


def test_delete_bagger_not_found(client):
    """Test DELETE /baggers/{id} with non-existent ID returns 404"""
    response = client.delete("/baggers/999")

    assert response.status_code == 404
    assert "Bagger not found" in response.json()["detail"]


def test_api_workflow(client):
    """Test complete CRUD workflow"""
    create_data = {
        "name": "Workflow Test",
        "membershipNo": "AFL999",
        "emailAddress": "workflow@example.com",
    }
    create_response = client.post("/baggers/", json=create_data)
    assert create_response.status_code == 200
    bagger = create_response.json()

    get_response = client.get(f"/baggers/{bagger['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Workflow Test"

    update_data = {
        "name": "Updated Workflow Test",
        "membershipNo": "AFL999",
        "emailAddress": "updated@example.com",
        "phoneNumber": "0411111111",
    }
    update_response = client.put(f"/baggers/{bagger['id']}", json=update_data)
    assert update_response.status_code == 200
    updated_bagger = update_response.json()
    assert updated_bagger["name"] == "Updated Workflow Test"
    assert updated_bagger["phoneNumber"] == "0411111111"

    list_response = client.get("/baggers/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete_response = client.delete(f"/baggers/{bagger['id']}")
    assert delete_response.status_code == 200

    final_get = client.get(f"/baggers/{bagger['id']}")
    assert final_get.status_code == 404

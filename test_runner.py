import pytest
from StockControlOOP import *
import json
from app import app, User, StockController
import time

@pytest.fixture
def stock_controller():
    return StockController()

def test_add_stock(stock_controller):
    perishable_item = Perishables(10, "Apples")
    liquid_item = Liquid(20, "Soda")
    non_perishable_item = NonPerishables(30, "Canned Beans")
    frozen_item = Frozen(15, "Ice Cream")

    stock_controller.add_stock(perishable_item)
    stock_controller.add_stock(liquid_item)
    stock_controller.add_stock(non_perishable_item)
    stock_controller.add_stock(frozen_item)

    # You should assert that the items have been added to the respective warehouses.
    assert stock_controller.north_warehouse.search_stock("Apples") == 10
    assert stock_controller.south_warehouse.search_stock("Soda") == 20
    assert stock_controller.east_warehouse.search_stock("Canned Beans") == 30
    assert stock_controller.west_warehouse.search_stock("Ice Cream") == 15

def test_get_stock(stock_controller):
    # Add some items to the warehouses.
    perishable_item = Perishables(5, "Strawberries")
    liquid_item = Liquid(10, "Orange Juice")
    non_perishable_item = NonPerishables(15, "Pasta")
    frozen_item = Frozen(8, "Frozen Pizza")

    stock_controller.add_stock(perishable_item)
    stock_controller.add_stock(liquid_item)
    stock_controller.add_stock(non_perishable_item)
    stock_controller.add_stock(frozen_item)

    # Check if the total stock includes all items.
    total_stock = stock_controller.get_stock()
    assert any(item.name == "Strawberries" for item in total_stock)
    assert any(item.name == "Orange Juice" for item in total_stock)
    assert any(item.name == "Pasta" for item in total_stock)
    assert any(item.name == "Frozen Pizza" for item in total_stock)

def test_search_stock(stock_controller):
    perishable_item = Perishables(5, "Bananas")
    liquid_item = Liquid(10, "Milk")
    non_perishable_item = NonPerishables(15, "Cereal")
    frozen_item = Frozen(8, "Frozen Vegetables")

    stock_controller.add_stock(perishable_item)
    stock_controller.add_stock(liquid_item)
    stock_controller.add_stock(non_perishable_item)
    stock_controller.add_stock(frozen_item)

    # Check if we can search for items in the stock.
    assert stock_controller.search_stock("Bananas") == 5
    assert stock_controller.search_stock("Milk") == 10
    assert stock_controller.search_stock("Cereal") == 15
    assert stock_controller.search_stock("Frozen Vegetables") == 8

def test_remove_stock(stock_controller):
    perishable_item = Perishables(5, "Strawberries")
    liquid_item = Liquid(10, "Orange Juice")
    non_perishable_item = NonPerishables(15, "Pasta")
    frozen_item = Frozen(8, "Frozen Pizza")

    stock_controller.add_stock(perishable_item)
    stock_controller.add_stock(liquid_item)
    stock_controller.add_stock(non_perishable_item)
    stock_controller.add_stock(frozen_item)

    # Remove items from the stock.
    stock_controller.remove_stock(perishable_item)
    stock_controller.remove_stock(liquid_item)
    stock_controller.remove_stock(non_perishable_item)
    stock_controller.remove_stock(frozen_item)

    # Ensure that items are removed from the warehouses.
    assert stock_controller.north_warehouse.search_stock("Strawberries") == 0
    assert stock_controller.south_warehouse.search_stock("Orange Juice") == 0
    assert stock_controller.east_warehouse.search_stock("Pasta") == 0
    assert stock_controller.west_warehouse.search_stock("Frozen Pizza") == 0

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_and_login(client):
    # Test user registration
    response = client.post('/register', data=json.dumps({
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    }), content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "testuser"
    assert data["email"] == "testuser@example.com"

    # Test user login
    response = client.post('/login', data=json.dumps({
        "username": "testuser",
        "password": "testpassword"
    }), content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "name" in data
    assert "email" in data
    
def test_add_item(client):
    # Test adding an item
    response = client.put('/items?name=test_item&quantity=10&item_type=0')
    assert response.status_code == 302

def test_get_items(client):
    # Test getting items
    response = client.get('/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_delete_item(client):
    # Test deleting an item
    response = client.delete('/items?name=test_item&quantity=10&item_type=0')
    assert response.status_code == 302

def test_logout(client):
    # Test user logout
    response = client.post('/logout')
    assert response.status_code == 200
    
def test_failed_login(client):
    # Test failed login with incorrect password
    response = client.post('/login', data=json.dumps({
        "username": "testuser",
        "password": "incorrect_password"
    }), content_type='application/json')

    assert response.status_code == 401
    

# Run the tests with pytest
if __name__ == '__main__':
    pytest.main()
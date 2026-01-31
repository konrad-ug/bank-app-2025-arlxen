import pytest
import requests
import json
import threading
import time
from app.api import app


# Test configuration
API_BASE_URL = "http://localhost:5000"
TEST_PORT = 5000


@pytest.fixture(scope="session")
def flask_app():
    """Start Flask app in background for tests"""
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    
    # Start Flask app in a separate thread
    def run_app():
        app.run(port=TEST_PORT, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    yield app
    
    # Cleanup is automatic as daemon thread


@pytest.fixture
def api_client(flask_app):
    """Provide API client for making requests"""
    return requests.Session()


@pytest.fixture
def sample_account_data():
    """Sample account data for testing"""
    return {
        "name": "James",
        "surname": "Hetfield",
        "pesel": "89092909825"
    }


class TestAccountCRUD:
    def test_create_account(self, api_client, sample_account_data):
        """Test creating an account via API"""
        response = api_client.post(
            f"{API_BASE_URL}/api/accounts",
            json=sample_account_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Account created"
    
    def test_create_account_missing_fields(self, api_client):
        """Test creating account with missing fields returns 400"""
        incomplete_data = {"name": "John"}
        response = api_client.post(
            f"{API_BASE_URL}/api/accounts",
            json=incomplete_data
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Missing required fields" in data["error"]
    
    def test_get_all_accounts(self, api_client, sample_account_data):
        """Test getting all accounts"""
        # First create an account
        api_client.post(f"{API_BASE_URL}/api/accounts", json=sample_account_data)
        
        # Then get all accounts
        response = api_client.get(f"{API_BASE_URL}/api/accounts")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check structure of account data
        account = next((acc for acc in data if acc["pesel"] == sample_account_data["pesel"]), None)
        assert account is not None
        assert account["name"] == sample_account_data["name"]
        assert account["surname"] == sample_account_data["surname"]
        assert account["pesel"] == sample_account_data["pesel"]
        assert "balance" in account
    
    def test_get_account_count(self, api_client, sample_account_data):
        """Test getting account count"""
        # Get initial count
        response = api_client.get(f"{API_BASE_URL}/api/accounts/count")
        assert response.status_code == 200
        initial_count = response.json()["count"]
        
        # Create an account
        api_client.post(f"{API_BASE_URL}/api/accounts", json=sample_account_data)
        
        # Check count increased
        response = api_client.get(f"{API_BASE_URL}/api/accounts/count")
        assert response.status_code == 200
        new_count = response.json()["count"]
        assert new_count == initial_count + 1
    
    def test_get_account_by_pesel(self, api_client, sample_account_data):
        """Test getting account by pesel"""
        # Create an account first
        api_client.post(f"{API_BASE_URL}/api/accounts", json=sample_account_data)
        
        # Get account by pesel
        response = api_client.get(f"{API_BASE_URL}/api/accounts/{sample_account_data['pesel']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_account_data["name"]
        assert data["surname"] == sample_account_data["surname"]
        assert data["pesel"] == sample_account_data["pesel"]
        assert "balance" in data
    
    def test_get_account_by_pesel_not_found(self, api_client):
        """Test getting account by non-existent pesel returns 404"""
        non_existent_pesel = "99999999999"
        response = api_client.get(f"{API_BASE_URL}/api/accounts/{non_existent_pesel}")
        
        assert response.status_code == 404
        data = response.json()
        assert "Account not found" in data["error"]
    
    def test_update_account(self, api_client, sample_account_data):
        """Test updating account via PATCH"""
        # Create an account first
        api_client.post(f"{API_BASE_URL}/api/accounts", json=sample_account_data)
        
        # Update account
        update_data = {"name": "John", "surname": "Doe"}
        response = api_client.patch(
            f"{API_BASE_URL}/api/accounts/{sample_account_data['pesel']}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Account updated"
        
        # Verify the update
        response = api_client.get(f"{API_BASE_URL}/api/accounts/{sample_account_data['pesel']}")
        updated_account = response.json()
        assert updated_account["name"] == "John"
        assert updated_account["surname"] == "Doe"
        assert updated_account["pesel"] == sample_account_data["pesel"]  # pesel shouldn't change
    
    def test_update_account_partial(self, api_client, sample_account_data):
        """Test partial update (only name)"""
        # Create an account first
        api_client.post(f"{API_BASE_URL}/api/accounts", json=sample_account_data)
        
        # Update only name
        update_data = {"name": "Johnny"}
        response = api_client.patch(
            f"{API_BASE_URL}/api/accounts/{sample_account_data['pesel']}",
            json=update_data
        )
        
        assert response.status_code == 200
        
        # Verify the update - name changed, surname unchanged
        response = api_client.get(f"{API_BASE_URL}/api/accounts/{sample_account_data['pesel']}")
        updated_account = response.json()
        assert updated_account["name"] == "Johnny"
        assert updated_account["surname"] == sample_account_data["surname"]  # Should remain unchanged
    
    def test_update_account_not_found(self, api_client):
        """Test updating non-existent account returns 404"""
        non_existent_pesel = "99999999999"
        update_data = {"name": "John"}
        response = api_client.patch(
            f"{API_BASE_URL}/api/accounts/{non_existent_pesel}",
            json=update_data
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Account not found" in data["error"]
    
    def test_delete_account(self, api_client, sample_account_data):
        """Test deleting account"""
        # Create an account first
        api_client.post(f"{API_BASE_URL}/api/accounts", json=sample_account_data)
        
        # Delete the account
        response = api_client.delete(f"{API_BASE_URL}/api/accounts/{sample_account_data['pesel']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Account deleted"
        
        # Verify account is deleted
        response = api_client.get(f"{API_BASE_URL}/api/accounts/{sample_account_data['pesel']}")
        assert response.status_code == 404
    
    def test_delete_account_not_found(self, api_client):
        """Test deleting non-existent account returns 404"""
        non_existent_pesel = "99999999999"
        response = api_client.delete(f"{API_BASE_URL}/api/accounts/{non_existent_pesel}")
        
        assert response.status_code == 404
        data = response.json()
        assert "Account not found" in data["error"]
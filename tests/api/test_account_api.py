import pytest
import json
from app.api import app, reset_registry


@pytest.fixture
def client():
    """Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_registry():
    """Reset registry before each test"""
    reset_registry()


@pytest.fixture
def sample_account_data():
    """Sample account data for testing"""
    return {
        "name": "James",
        "surname": "Hetfield",
        "pesel": "89092909825"
    }


class TestAccountAPI:
    def test_create_account(self, client, sample_account_data):
        """Test creating an account via API"""
        response = client.post(
            '/api/accounts',
            data=json.dumps(sample_account_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "Account created"
    
    def test_create_account_missing_fields(self, client):
        """Test creating account with missing fields returns 400"""
        incomplete_data = {"name": "John"}
        response = client.post(
            '/api/accounts',
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Missing required fields" in data["error"]
    
    def test_get_all_accounts_empty(self, client):
        """Test getting all accounts when registry is empty"""
        response = client.get('/api/accounts')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_get_all_accounts_with_data(self, client, sample_account_data):
        """Test getting all accounts after creating one"""
        # First create an account
        client.post(
            '/api/accounts',
            data=json.dumps(sample_account_data),
            content_type='application/json'
        )
        
        # Then get all accounts
        response = client.get('/api/accounts')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check structure of account data
        account = next((acc for acc in data if acc["pesel"] == sample_account_data["pesel"]), None)
        assert account is not None
        assert account["name"] == sample_account_data["name"]
        assert account["surname"] == sample_account_data["surname"]
        assert account["pesel"] == sample_account_data["pesel"]
        assert "balance" in account
    
    def test_get_account_count(self, client, sample_account_data):
        """Test getting account count"""
        # Get initial count
        response = client.get('/api/accounts/count')
        assert response.status_code == 200
        initial_count = json.loads(response.data)["count"]
        
        # Create an account
        client.post(
            '/api/accounts',
            data=json.dumps(sample_account_data),
            content_type='application/json'
        )
        
        # Check count increased
        response = client.get('/api/accounts/count')
        assert response.status_code == 200
        new_count = json.loads(response.data)["count"]
        assert new_count == initial_count + 1
    
    def test_get_account_by_pesel(self, client, sample_account_data):
        """Test getting account by pesel"""
        # Create an account first
        client.post(
            '/api/accounts',
            data=json.dumps(sample_account_data),
            content_type='application/json'
        )
        
        # Get account by pesel
        response = client.get(f'/api/accounts/{sample_account_data["pesel"]}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == sample_account_data["name"]
        assert data["surname"] == sample_account_data["surname"]
        assert data["pesel"] == sample_account_data["pesel"]
        assert "balance" in data
    
    def test_get_account_by_pesel_not_found(self, client):
        """Test getting account by non-existent pesel returns 404"""
        non_existent_pesel = "99999999999"
        response = client.get(f'/api/accounts/{non_existent_pesel}')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Account not found" in data["error"]
    
    def test_update_account(self, client, sample_account_data):
        """Test updating account via PATCH"""
        # Create an account first
        client.post(
            '/api/accounts',
            data=json.dumps(sample_account_data),
            content_type='application/json'
        )
        
        # Update account
        update_data = {"name": "John", "surname": "Doe"}
        response = client.patch(
            f'/api/accounts/{sample_account_data["pesel"]}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Account updated"
        
        # Verify the update
        response = client.get(f'/api/accounts/{sample_account_data["pesel"]}')
        updated_account = json.loads(response.data)
        assert updated_account["name"] == "John"
        assert updated_account["surname"] == "Doe"
        assert updated_account["pesel"] == sample_account_data["pesel"]  # pesel shouldn't change
    
    def test_update_account_partial(self, client, sample_account_data):
        """Test partial update (only name)"""
        # Create an account first
        client.post(
            '/api/accounts',
            data=json.dumps(sample_account_data),
            content_type='application/json'
        )
        
        # Update only name
        update_data = {"name": "Johnny"}
        response = client.patch(
            f'/api/accounts/{sample_account_data["pesel"]}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        # Verify the update - name changed, surname unchanged
        response = client.get(f'/api/accounts/{sample_account_data["pesel"]}')
        updated_account = json.loads(response.data)
        assert updated_account["name"] == "Johnny"
        assert updated_account["surname"] == sample_account_data["surname"]  # Should remain unchanged
    
    def test_update_account_not_found(self, client):
        """Test updating non-existent account returns 404"""
        non_existent_pesel = "99999999999"
        update_data = {"name": "John"}
        response = client.patch(
            f'/api/accounts/{non_existent_pesel}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Account not found" in data["error"]
    
    def test_delete_account(self, client, sample_account_data):
        """Test deleting account"""
        # Create an account first
        client.post(
            '/api/accounts',
            data=json.dumps(sample_account_data),
            content_type='application/json'
        )
        
        # Delete the account
        response = client.delete(f'/api/accounts/{sample_account_data["pesel"]}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Account deleted"
        
        # Verify account is deleted
        response = client.get(f'/api/accounts/{sample_account_data["pesel"]}')
        assert response.status_code == 404
    
    def test_delete_account_not_found(self, client):
        """Test deleting non-existent account returns 404"""
        non_existent_pesel = "99999999999"
        response = client.delete(f'/api/accounts/{non_existent_pesel}')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "Account not found" in data["error"]
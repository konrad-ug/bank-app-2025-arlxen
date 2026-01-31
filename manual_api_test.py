#!/usr/bin/env python3
"""
Manual API testing script
Run this after starting the Flask app to test endpoints manually.
"""

import requests
import json


API_BASE_URL = "http://localhost:5000"


def test_create_account():
    """Test creating an account"""
    print("=== Testing POST /api/accounts ===")
    
    account_data = {
        "name": "James",
        "surname": "Hetfield",
        "pesel": "89092909825"
    }
    
    response = requests.post(f"{API_BASE_URL}/api/accounts", json=account_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_get_all_accounts():
    """Test getting all accounts"""
    print("=== Testing GET /api/accounts ===")
    
    response = requests.get(f"{API_BASE_URL}/api/accounts")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_get_account_count():
    """Test getting account count"""
    print("=== Testing GET /api/accounts/count ===")
    
    response = requests.get(f"{API_BASE_URL}/api/accounts/count")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_get_account_by_pesel():
    """Test getting account by PESEL"""
    print("=== Testing GET /api/accounts/<pesel> ===")
    
    pesel = "89092909825"
    response = requests.get(f"{API_BASE_URL}/api/accounts/{pesel}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_update_account():
    """Test updating an account"""
    print("=== Testing PATCH /api/accounts/<pesel> ===")
    
    pesel = "89092909825"
    update_data = {"name": "John", "surname": "Doe"}
    
    response = requests.patch(f"{API_BASE_URL}/api/accounts/{pesel}", json=update_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_get_nonexistent_account():
    """Test getting account that doesn't exist (should return 404)"""
    print("=== Testing GET /api/accounts/<nonexistent_pesel> ===")
    
    pesel = "99999999999"
    response = requests.get(f"{API_BASE_URL}/api/accounts/{pesel}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_delete_account():
    """Test deleting an account"""
    print("=== Testing DELETE /api/accounts/<pesel> ===")
    
    pesel = "89092909825"
    response = requests.delete(f"{API_BASE_URL}/api/accounts/{pesel}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


if __name__ == "__main__":
    print("Manual API Testing")
    print("Make sure the Flask app is running on http://localhost:5000")
    print("=" * 50)
    
    try:
        # Test the endpoints in order
        test_create_account()
        test_get_all_accounts()
        test_get_account_count()
        test_get_account_by_pesel()
        test_update_account()
        test_get_account_by_pesel()  # Check if update worked
        test_get_nonexistent_account()  # Test 404
        test_delete_account()
        test_get_account_by_pesel()  # Should return 404 now
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to Flask app.")
        print("Make sure to start the app with: flask --app app/api.py --debug run")
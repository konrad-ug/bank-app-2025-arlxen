[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name:

surname:

group:

## How to start the app

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the microservice:
```bash
flask --app app/api.py --debug run
```
or
```bash
python -m flask --app app/api.py --debug run
```

The API will be available at `http://localhost:5000`

### API Endpoints:
- `POST /api/accounts` - Create a new personal account
- `GET /api/accounts` - Get all accounts
- `GET /api/accounts/count` - Get number of accounts
- `GET /api/accounts/<pesel>` - Get account by PESEL
- `PATCH /api/accounts/<pesel>` - Update account (name and/or surname)
- `DELETE /api/accounts/<pesel>` - Delete account

## How to execute tests

### Unit tests:
```bash
pytest tests/unit/
```

### API integration tests:
```bash
pytest tests/api/
```

### All tests:
```bash
pytest
```
# 🐓roosteratbug

一个分享bug的平台。分享常见的bug，并让其他工程师能够查看和修复它们，以提高工作效率。

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn backend.main:app --reload
```

3. generate data:
### linux
```bash
export OPENAI_API_KEY=your_deepseek_api_key
export OPENAI_BASE_URL=https://api.deepseek.com/v1
python generate_data.py
```
### windows
```bash
cp .env2 .env
```
edit .env file

OPENAI_BASE_URL = "https://api.deepseek.com/v1"
OPENAI_API_KEY = "your_deepseek_api_key"
```bash
python generate_data.py
```

## Database

The application uses SQLite as the database. The database schema is defined in the `models.py` file.

## Authentication

## API Endpoints

- `GET /bugs/`: Get all bugs (with pagination)
- `GET /bugs/{bug_id}`: Get a specific bug by ID
- `POST /bugs/`: Create a new bug
- `PUT /bugs/{bug_id}`: Update an existing bug
- `DELETE /bugs/{bug_id}`: Delete a bug
- `GET /bugs/search/?query=keyword`: Search bugs by title or description

## Bug Schema

```json
{
  "title": "string",
  "description": "string",
  "solution": "string",
  "severity": "string"
}
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Open the page
share_front/tail.html
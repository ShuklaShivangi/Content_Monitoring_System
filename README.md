# Content Monitoring System
 
## Overview

This is a Django backend system that:

* Fetches content from an external API
* Matches it against user-defined keywords
* Generates flags with scores
* Allows manual review (relevant / irrelevant)
* Prevents re-showing irrelevant results unless content changes

---

## Setup & Run

```bash
git clone https://github.com/ShuklaShivangi/Content_Monitoring_System.git
cd content_monitoring_system

python -m venv venv
venv\Scripts\activate

pip install django djangorestframework requests

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

Access:

* Admin: http://127.0.0.1:8000/admin/
* API: http://127.0.0.1:8000/

---

## Data Source

Uses public API:
https://jsonplaceholder.typicode.com/posts

Content is fetched dynamically when `/scan/` is triggered.

---

## API Endpoints

### Create Keyword

POST /keywords/

```json
{
  "name": "sunt"
}
```

### Run Scan

POST /scan/

### List Flags

GET /flags/

### Update Flag

PATCH /flags/{id}/

```json
{
  "status": "irrelevant"
}
```

---

## Matching Logic

* Exact match in title → 100
* Partial match in title → 70
* Match in body → 40

---

## Suppression Logic

* If a flag is marked **irrelevant**, it is not recreated
* If the content is updated later, it can appear again

Implementation:

* `reviewed_at` stored in Flag
* `last_updated` stored in ContentItem
* New flag is created only if:

```
content.last_updated > reviewed_at
```

---

## Sample Requests (curl)

```bash
# Create keyword
curl -X POST http://127.0.0.1:8000/keywords/ -H "Content-Type: application/json" -d "{\"name\": \"sunt\"}"

# Run scan
curl -X POST http://127.0.0.1:8000/scan/

# List flags
curl http://127.0.0.1:8000/flags/

# Update flag
curl -X PATCH http://127.0.0.1:8000/flags/1/ -H "Content-Type: application/json" -d "{\"status\": \"irrelevant\"}"
```

---

## Notes / Assumptions

* Limited API fetch to 10 items per scan
* Scan runs synchronously (no background jobs)
* Matching logic is intentionally simple
* Django admin used for quick testing

---

## Tech Stack

* Django
* Django REST Framework
* SQLite
* Requests

---

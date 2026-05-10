# Simple Social 📸

A simple social media backend built with **FastAPI** — my project for learning async APIs, authentication, file uploads, and database integration.

---

## What it does

- Upload images and videos with captions
- View a feed of all posts from all users
- Delete your own posts
- User registration, login, and authentication via JWT

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Database | SQLite + SQLAlchemy (async) |
| Auth | fastapi-users (JWT) |
| File Storage | ImageKit |
| Frontend | Streamlit |
| Server | Uvicorn |

---

## Project Structure

```
simple_social/
├── app/
│   ├── app.py        # FastAPI routes
│   ├── db.py         # Database models and session
│   ├── schemas.py    # Pydantic schemas
│   ├── users.py      # Auth configuration
│   ├── images.py     # ImageKit setup
│   └── frontend.py   # Streamlit UI
├── main.py           # Entry point
├── pyproject.toml
└── test.db
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/simple_social.git
cd simple_social
```

### 2. Set up the environment

```bash
uv venv
uv pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL=your_imagekit_url_endpoint
SECRET=your_jwt_secret
```

### 4. Run the backend

```bash
uv run main.py
```

API will be available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

### 5. Run the frontend

```bash
uv run streamlit run app/frontend.py
```

Frontend at `http://localhost:8501`

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/jwt/login` | Login and get JWT token | No |
| POST | `/upload` | Upload an image or video | Yes |
| GET | `/feed` | Get all posts | Yes |
| DELETE | `/posts/{post_id}` | Delete your own post | Yes |

---

## What I Learned

- Building async REST APIs with FastAPI
- JWT authentication with fastapi-users
- SQLAlchemy async sessions and ORM relationships
- Handling file uploads and integrating with a third-party storage service (ImageKit)
- Connecting a Streamlit frontend to a FastAPI backend

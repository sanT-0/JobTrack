# JobTrack — Job Application & Interview Management System

A production-grade, portfolio-ready full-stack web application designed for developers and professionals to track job opportunities, interview stages, application statuses, and career milestones in one modern, unified interface.

Built with **React**, **FastAPI**, **SQLAlchemy**, and **MySQL**.

---

## 🌟 Highlights & Key Features

- **End-to-End Authentication**: JWT Bearer token authentication with bcrypt password hashing and user isolation.
- **Application Lifecycle Management**: Track applications through every stage: `Applied`, `Shortlisted`, `Interview`, `Offer`, `Rejected`, and `Withdrawn`.
- **Search & Multi-Field Filtering**: Fast client-side search by company and position, plus status and job type dropdown filters with pagination.
- **Upcoming Interviews Tracker**: Automatically detects and surfaces future interviews sorted by proximity.
- **Real-Time Analytics Dashboard**: Visual summary metrics showing application distributions and quick links.
- **User Profile Management**: Update personal information and change passwords securely.
- **Modern Dark UI Design**: Glassmorphism aesthetic, responsive layouts for mobile and desktop, with micro-animations and status badges.
- **Thoroughly Tested**: 36 automated unit and integration tests covering authentication, application CRUD, security isolation, and dashboard calculations.
- **Dockerized**: Complete containerized deployment setup with `docker-compose`.

---

## 🛠️ Architecture & Tech Stack

```
   ┌────────────────────────────────────────────────────────┐
   │                     Client Tier                        │
   │   React 19 + Vite 8 + React Router 7 + Vanilla CSS     │
   └───────────────────────────┬────────────────────────────┘
                               │ HTTP / JSON (Axios Interceptors)
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │                     API Tier                           │
   │   FastAPI + Pydantic v2 + Python-Jose + Bcrypt         │
   │   (Repository & Service Layer Pattern)                 │
   └───────────────────────────┬────────────────────────────┘
                               │ SQLAlchemy 2.0 ORM
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │                    Database Tier                       │
   │   MySQL 8.0 / PyMySQL (Production)                     │
   │   SQLite In-Memory with StaticPool (Automated Tests)   │
   └────────────────────────────────────────────────────────┘
```

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Driver**: [PyMySQL](https://github.com/PyMySQL/PyMySQL) + Cryptography
- **Security & Validation**: Pydantic v2, Python-Jose (JWT), Bcrypt
- **Testing**: [Pytest](https://docs.pytest.org/), HTTPX

### Frontend
- **Framework**: [React 19](https://react.dev/)
- **Build Tool**: [Vite](https://vite.dev/)
- **Routing**: [React Router](https://reactrouter.com/)
- **Styling**: Vanilla CSS Design System with CSS variables and glassmorphism styling
- **HTTP Client**: Axios with JWT request and 401 response interceptors

---

## 📁 Repository Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI API route controllers (auth, applications, dashboard, users)
│   │   ├── core/            # Configuration (pydantic-settings) & security (JWT, bcrypt)
│   │   ├── database/        # SQLAlchemy engine, sessionmaker, and Base
│   │   ├── models/          # Declarative ORM models (User, Application)
│   │   ├── repositories/    # Data access layer (UserRepository, ApplicationRepository)
│   │   ├── schemas/         # Pydantic request & response schemas
│   │   ├── services/        # Business logic layer (AuthService, ApplicationService)
│   │   └── tests/           # Comprehensive Pytest suite
│   ├── Dockerfile           # Production container definition
│   ├── requirements.txt     # Python dependencies
│   └── seed.py              # Development seed script with demo data
│
├── frontend/
│   ├── src/
│   │   ├── assets/          # Static icons and branding
│   │   ├── components/      # Common UI components (Navbar, Modal, Spinner, StatusBadge, Form)
│   │   ├── context/         # AuthContext provider
│   │   ├── hooks/           # useAuth custom hook
│   │   ├── layouts/         # AppLayout (protected) & AuthLayout (public)
│   │   ├── pages/           # DashboardPage, ApplicationsPage, ApplicationDetailPage, ProfilePage, Auth
│   │   ├── services/        # Axios API client & endpoints
│   │   ├── utils/           # Date formatting and currency helpers
│   │   ├── App.jsx          # Router and application root
│   │   └── index.css        # Core design system and CSS variables
│   ├── Dockerfile           # Multi-stage container build (Vite + Nginx)
│   ├── nginx.conf           # SPA fallback routing & reverse proxy
│   └── package.json
│
├── docker-compose.yml       # 1-command startup for MySQL, Backend, Frontend
└── README.md
```

---

## 🚀 Quickstart Guide

### Option A: Running with Docker Compose (Recommended)

To run the entire stack (MySQL 8.0, FastAPI Backend, and React Frontend) with a single command:

```bash
docker compose up --build
```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **MySQL**: `localhost:3307` (container port remains `3306`)

---

### Option B: Running Locally for Development

#### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- MySQL Server 8.0 (running locally or via Docker)

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Copy .env.example to .env and adjust credentials:
cp .env.example .env

# Run database seed (optional demo user + sample applications)
python seed.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🔑 Demo Account Credentials

If you populate the database using `python backend/seed.py`:

- **Email**: `demo@jobtrack.dev`
- **Password**: `demo1234`

---

## 🧪 Running Automated Tests

JobTrack includes an extensive Pytest suite that runs on an isolated in-memory SQLite database without requiring a running MySQL instance:

```bash
cd backend
pytest app/tests -v
```

### Test Coverage Highlights:
- **Authentication**: Registration, duplicate email prevention, password length validation, login, token generation, user info retrieval (`/api/auth/me`), and unauthorized access blocking.
- **Applications CRUD**: User-scoped create, read, update, delete operations; input validation; pagination metadata; search queries; status & job type filters.
- **Data Isolation**: Strict ownership checks ensuring User A cannot read, modify, or delete User B's job records.
- **Dashboard**: Metric counts by status, upcoming interview filtering (future dates only), and sorting verification.

---

## 📖 API Documentation Overview

| Method | Endpoint | Description | Protected |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register a new user | No |
| `POST` | `/api/auth/login` | Login and receive JWT access token | No |
| `GET` | `/api/auth/me` | Retrieve authenticated user profile | Yes |
| `GET` | `/api/applications` | List applications (search, filter, paginate) | Yes |
| `POST` | `/api/applications` | Create a new job application | Yes |
| `GET` | `/api/applications/{id}` | Get application details | Yes |
| `PUT` | `/api/applications/{id}` | Update application details or status | Yes |
| `DELETE`| `/api/applications/{id}` | Delete an application | Yes |
| `GET` | `/api/dashboard/stats` | Aggregate counts for user's applications | Yes |
| `GET` | `/api/dashboard/upcoming-interviews` | List upcoming scheduled interviews | Yes |
| `GET` | `/api/users/me` | Fetch user profile settings | Yes |
| `PUT` | `/api/users/me` | Update full name or change password | Yes |

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

---

## 🔒 Security Best Practices

1. **Password Hashing**: Uses `bcrypt` with automatic salting and length checks.
2. **Stateless JWT Authorization**: Cryptographically signed tokens with configurable expiration.
3. **Data Protection**: Sensitive fields (e.g. `password_hash`) are excluded from Pydantic response models.
4. **Parameter Sanitization & Prepared Statements**: SQLAlchemy ORM query compilation protects against SQL injection attacks.
5. **CORS Hardening**: Strict origin whitelisting configured in `app/core/config.py`.

---

## 📄 License

This project is licensed under the MIT License.

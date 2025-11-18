# Leadership Coach

> An AI-powered leadership development platform that helps professionals assess competencies, receive personalized development plans, and track their growth journey.

[![Next.js](https://img.shields.io/badge/Next.js-15.4-black?style=flat&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.1-61DAFB?style=flat&logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=flat&logo=openai)](https://openai.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org/)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**Leadership Coach** is a full-stack AI-powered platform designed for the Masterschool AI Software Engineering Capstone Project. It combines modern web technologies with OpenAI's latest models to deliver personalized leadership development experiences.

The application guides users through a comprehensive leadership assessment questionnaire, analyzes their competencies across multiple dimensions (communication, decision-making, team building, etc.), and generates customized development plans with actionable steps, curated resources, and timeline tracking.

### Why Leadership Coach?

- **Personalized Learning**: AI-generated plans tailored to individual competency gaps and career goals
- **Evidence-Based**: Uses proven leadership frameworks and authoritative resources
- **Progress Tracking**: Multi-plan history and timeline management
- **Export-Ready**: Professional PDF reports for sharing with mentors or managers
- **Secure & Private**: JWT authentication, secure session management, and data protection

---

## Key Features

### Core Functionality

- **🔐 User Authentication**: Secure JWT-based authentication with session management and auto-refresh
- **📝 Leadership Assessment**: Multi-step questionnaire covering 7+ leadership competencies
- **🤖 AI-Powered Plan Generation**:
  - Leverages OpenAI's GPT-4 with web search capabilities
  - Structured output with typed validation
  - Curated resources with authoritative links
- **📊 Competency Scoring**: Algorithmic analysis of assessment responses
- **📄 PDF Export**: Professional development plan PDFs (powered by WeasyPrint)
- **📈 Plan History**: View and compare multiple development plans over time
- **⏱️ Session Management**: Inactivity warnings, auto-logout, and token refresh
- **🌓 Dark Mode**: Full theme support with next-themes

### User Experience

- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Real-Time Feedback**: Loading states, progress indicators, and toast notifications
- **Accessible UI**: Built with Radix UI primitives and shadcn/ui components
- **Intuitive Navigation**: Contextual navigation with plan history dropdown

---

## Tech Stack

### Frontend

- **Framework**: [Next.js 15](https://nextjs.org/) (App Router, React 19)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 4.x with custom animations
- **UI Components**: [shadcn/ui](https://ui.shadcn.com/) (Radix UI primitives)
- **State Management**: React Context API (SessionContext, QuestionnaireContext)
- **HTTP Client**: Axios with interceptors
- **Forms**: react-hook-form + Zod validation
- **Icons**: Lucide React
- **Notifications**: Sonner (toast library)

### Backend

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.116
- **Language**: Python 3.12
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL via [Supabase](https://supabase.com/)
- **Authentication**: JWT tokens (python-jose) + bcrypt
- **AI Integration**:
  - [OpenAI Python SDK](https://github.com/openai/openai-python) 1.0+
  - GPT-4 with structured outputs (Pydantic AI)
  - Web search tool for resource curation
- **PDF Generation**: [WeasyPrint](https://weasyprint.org/) 66.0
- **Package Management**: [uv](https://github.com/astral-sh/uv) (modern Python package manager)
- **Server**: Uvicorn (ASGI)

### DevOps & Tools

- **Version Control**: Git & GitHub
- **Linting**: ESLint (frontend), isort (backend)
- **Environment Management**: dotenv
- **Database Migrations**: Automatic schema management via SQLModel

---

## Architecture

### System Design

```text
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│   Next.js   │────────▶│   FastAPI    │────────▶│ PostgreSQL │
│   Frontend  │  HTTP   │   Backend    │         │  Supabase  │
│  (Port 3000)│◀────────│ (Port 8000)  │◀────────│            │
└─────────────┘         └──────────────┘         └────────────┘
       │                        │
       │                        │
       ▼                        ▼
┌─────────────┐         ┌──────────────┐
│ SessionCtx  │         │  OpenAI API  │
│ ThemeCtx    │         │   GPT-5-MINI +    │
│ RouterCtx   │         │  Web Search  │
└─────────────┘         └──────────────┘
```

### Data Flow

1. **Authentication**: User logs in → Backend issues JWT → Frontend stores in httpOnly cookie
2. **Assessment**: User completes questionnaire → Answers saved to database → Competency scores calculated
3. **Plan Generation**: User selects focus areas → Backend calls OpenAI API → Structured plan returned → Saved to database
4. **PDF Export**: User requests PDF → Backend converts markdown → WeasyPrint generates PDF → Returned as download

### Feature-Based Backend Structure

The backend follows a modular feature-based architecture:

```bash
backend/
├── features/
│   ├── auth/              # Authentication & JWT
│   ├── development_plans/ # AI plan generation & PDF
│   ├── results/           # Competency scoring
│   ├── user_answers/      # Questionnaire responses
│   └── ...
├── entities/              # SQLModel database models
├── database/              # Session management, migrations
├── routers.py             # Centralized router registration
└── main.py                # FastAPI app, CORS, lifespan
```

Each feature module contains:

- `controller.py`: FastAPI route definitions
- `service.py`: Business logic
- `models.py`: Pydantic request/response schemas

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

### Required

- **Node.js**: v18+ and npm (for frontend)
- **Python**: 3.12 (required for backend compatibility)
- **PostgreSQL**: 14+ (or Supabase account)
- **Git**: For cloning the repository

### Recommended

- **[uv](https://github.com/astral-sh/uv)**: Modern Python package manager (faster than pip)

  ```bash
  # Install on macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **[Homebrew](https://brew.com/)**: For installing native dependencies (macOS)

### macOS Users: Native Dependencies for PDF Export

WeasyPrint requires system libraries for PDF rendering:

```bash
brew install pango cairo gdk-pixbuf libffi
```

For other platforms, refer to the [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).

---

## Installation & Setup

### 1. Clone the Repository

```bash
# HTTPS
git clone https://github.com/Anca-Afloroaei/Leadership_Coach.git

# SSH (recommended)
git clone git@github.com:Anca-Afloroaei/Leadership_Coach.git

cd Leadership_Coach
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
uv sync

# Alternative: Use pip if uv is not available
# python -m venv .venv
# source .venv/bin/activate
# pip install -e .
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install Node.js dependencies
npm install
```

---

## Environment Variables

### Backend Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# Database (Supabase)
SUPABASE_PASSWORD=your_supabase_password
DATABASE_URL=postgresql://postgres:your_password@db.your-project.supabase.co:5432/postgres
SUPABASE_URL=https://your-project.supabase.co

# OpenAI API
OPENAI_API_KEY=sk-proj-...your-api-key...

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development  # or "production"
```

#### How to Obtain Credentials

1. **Supabase**:
   - Sign up at [supabase.com](https://supabase.com/)
   - Create a new project
   - Navigate to Project Settings → Database
   - Copy the connection string and credentials

2. **OpenAI API Key**:
   - Sign up at [platform.openai.com](https://platform.openai.com/)
   - Navigate to API Keys section
   - Create a new secret key
   - **Important**: Ensure you have billing enabled and credits available

3. **JWT Secret**:
   - Generate a secure random string:

     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```

### Frontend Configuration

Create a `.env.local` file in the `frontend/` directory:

```bash
# API Base URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

For production, update this to your deployed backend URL.

---

## Running the Application

### Development Mode

#### Terminal 1: Start Backend

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --app-dir .
```

Backend will be available at: <http://localhost:8000>

- API docs (Swagger): <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health/db>

#### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at: <http://localhost:3000>

### Production Build

#### Backend-Commands

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Frontend-Commands

```bash
cd frontend
npm run build
npm run start
```

---

## Project Structure

```bash
Leadership_Coach/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── routers.py                 # Centralized router registration
│   ├── config.py                  # Pydantic settings from .env
│   ├── database/
│   │   └── core.py                # SQLModel engine, sessions, migrations
│   ├── entities/                  # Database models
│   │   ├── user.py
│   │   ├── development_plan.py
│   │   ├── user_answers.py
│   │   └── ...
│   ├── features/                  # Feature modules
│   │   ├── auth/
│   │   │   ├── controller.py      # /auth/login, /auth/register
│   │   │   ├── service.py         # JWT creation, password hashing
│   │   │   └── models.py          # LoginRequest, TokenResponse
│   │   ├── development_plans/
│   │   │   ├── controller.py      # /dev-plans endpoints
│   │   │   ├── service.py         # AI plan generation, PDF export
│   │   │   └── models.py          # GeneratePlanRequest, PlanResponse
│   │   ├── results/
│   │   │   ├── controller.py      # /results endpoints
│   │   │   └── service.py         # Competency scoring algorithm
│   │   └── user_answers/
│   │       ├── controller.py      # /user-answers endpoints
│   │       └── service.py         # Answer storage & retrieval
│   ├── utils/
│   │   └── security.py            # bcrypt utilities
│   ├── pyproject.toml             # Python dependencies (uv)
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── app/                   # Next.js 15 App Router
│   │   │   ├── layout.tsx         # Root layout with providers
│   │   │   ├── page.tsx           # Landing page
│   │   │   ├── login/
│   │   │   ├── signup/
│   │   │   ├── questionnaire/     # Multi-step assessment
│   │   │   ├── results/[answers_id]/
│   │   │   │   ├── page.tsx       # Competency results view
│   │   │   │   └── plan/
│   │   │   │       └── page.tsx   # Development plan generation
│   │   │   └── devplans/[answers_id]/
│   │   │       └── page.tsx       # Plan history view
│   │   ├── components/            # Reusable UI components
│   │   │   ├── ui/                # shadcn/ui primitives
│   │   │   ├── NavBar.tsx
│   │   │   ├── AuthGuard.tsx
│   │   │   └── ...
│   │   ├── contexts/
│   │   │   ├── SessionContext.tsx # Auth state, activity tracking
│   │   │   └── QuestionnaireContext.tsx
│   │   ├── lib/
│   │   │   └── api/               # API client functions
│   │   │       ├── results.ts
│   │   │       └── devplans.ts
│   │   ├── services/
│   │   │   ├── auth.ts            # Session management
│   │   │   └── api.ts             # Axios instance
│   │   ├── middleware.ts          # Route protection
│   │   └── types/                 # TypeScript interfaces
│   ├── package.json
│   └── README.md
│
├── CLAUDE.md                      # Claude Code AI assistant instructions
├── HANDOVER.md                    # Development notes & known issues
├── README.md                      # This file
└── .gitignore
```

---

## API Documentation

The backend exposes a RESTful API documented with FastAPI's automatic OpenAPI schema.

### Interactive API Docs

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### Key Endpoints

#### Authentication

- `POST /auth/register` - Create new user account
- `POST /auth/login` - Login and receive JWT token
- `POST /auth/logout` - Invalidate session
- `POST /auth/refresh` - Refresh access token
- `GET /auth/validate` - Validate current session

#### Questionnaire & Results

- `POST /user-answers` - Submit questionnaire answers
- `GET /user-answers` - Get user's answer history
- `GET /user-answers/{record_id}` - Get specific answer record
- `GET /results/{record_id}` - Get competency scores for assessment

#### Development Plans

- `POST /dev-plans/generate` - Generate AI development plan

  ```json
  {
    "user_answers_record_id": "uuid",
    "focus_areas": ["communication", "decision-making"],
    "duration_days": 90
  }
  ```

- `GET /dev-plans/{record_id}` - Get latest plan for assessment
- `GET /dev-plans/{record_id}/all` - Get all plans for assessment
- `GET /dev-plans/{plan_id}/pdf` - Download plan as PDF
- `GET /dev-plans/user/all` - Get all plans for current user

#### Health Checks

- `GET /health` - API health status
- `GET /health/db` - Database connectivity check

---

## Database Schema

### Key Tables

### users

- `id` (UUID, PK)
- `email` (unique)
- `hashed_password`
- `created_at`, `updated_at`

### user_answers

- `id` (UUID, PK)
- `user_id` (FK → users)
- `answers` (JSONB)
- `created_at`

### development_plans

- `id` (UUID, PK)
- `user_id` (FK → users)
- `user_answers_record_id` (FK → user_answers)
- `plan_markdown` (TEXT)
- `focus_areas` (TEXT[])
- `action_items` (TEXT[])
- `resources` (TEXT[])
- `start_date`, `end_date`, `duration_days`
- `created_at`

### results

- `id` (UUID, PK)
- `user_answers_record_id` (FK → user_answers)
- `competency_scores` (JSONB)
- `overall_score` (FLOAT)
- `created_at`

### Database Migrations

Schema changes are handled automatically via `database/core.py::_ensure_development_plan_schema()` on application startup. For production, consider using Alembic for versioned migrations.

---

## Testing

### Backend Testing

```bash
cd backend
source .venv/bin/activate

# Run health checks
curl http://localhost:8000/health
curl http://localhost:8000/health/db

# Check duplicate plans (diagnostic script)
python -m backend.check_duplicate_plans
```

### Frontend Testing

```bash
cd frontend

# Linting
npm run lint

# Type checking
npx tsc --noEmit
```

### Manual Testing Checklist

- [ ] User registration and login flow
- [ ] Session timeout and auto-refresh
- [ ] Questionnaire completion and answer saving
- [ ] Competency score calculation
- [ ] Development plan generation with focus areas
- [ ] PDF export functionality
- [ ] Plan history navigation
- [ ] Dark mode toggle
- [ ] Responsive design on mobile

---

## Deployment

### Backend Deployment (Render/Railway/Fly.io)

1. Set environment variables in platform dashboard
2. Use `uvicorn main:app --host 0.0.0.0 --port $PORT` as start command
3. Ensure `pyproject.toml` dependencies include production dependencies
4. Configure CORS settings in `main.py` for frontend domain

### Frontend Deployment (Vercel/Netlify)

1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `.next`
4. Configure environment variables:
   - `NEXT_PUBLIC_API_BASE_URL` → deployed backend URL

### Database (Supabase)

- Already hosted via Supabase
- Ensure connection pooling is enabled for production
- Set up database backups in Supabase dashboard

---

## Future Enhancements

### Planned Features

- [ ] **Progress Tracking Dashboard**: Visual charts showing competency improvement over time
- [ ] **Peer Feedback Integration**: 360-degree feedback collection from colleagues
- [ ] **Goal Setting Module**: SMART goal creation with milestone tracking
- [ ] **Email Reminders**: Scheduled nudges for action item completion
- [ ] **Admin Panel**: User management and analytics dashboard
- [ ] **Multi-Language Support**: Internationalization (i18n) for global users
- [ ] **Mobile App**: React Native version for iOS/Android
- [ ] **AI Coaching Chat**: Conversational interface for real-time coaching
- [ ] **Resource Library**: Curated articles, videos, and courses
- [ ] **Badges & Gamification**: Achievement system to motivate users

### Technical Improvements

- [ ] Implement Alembic for database migrations
- [ ] Add comprehensive unit and integration tests (pytest, Jest)
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Implement caching layer (Redis) for API responses
- [ ] Add rate limiting and API throttling
- [ ] Enhance error monitoring (Sentry integration)
- [ ] Optimize OpenAI API costs with prompt caching
- [ ] Add WebSocket support for real-time plan generation updates

---

## Contributing

Contributions are welcome! This project is part of a capstone submission, but feedback and suggestions are appreciated.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Style

- **Backend**: Follow PEP 8, use isort for import sorting
- **Frontend**: Follow ESLint rules, use TypeScript strict mode
- **Commits**: Use conventional commit messages (feat, fix, docs, etc.)

---

## License

This project is created as part of the Masterschool AI Software Engineering program. All rights reserved.

For academic or educational use, please contact the author for permission.

---

## Acknowledgments

### Technologies & Tools

- [OpenAI](https://openai.com/) for GPT-4 API and web search capabilities
- [Vercel](https://vercel.com/) for Next.js framework and hosting solutions
- [Supabase](https://supabase.com/) for PostgreSQL database and authentication
- [shadcn/ui](https://ui.shadcn.com/) for beautiful, accessible UI components
- [FastAPI](https://fastapi.tiangolo.com/) for modern Python backend framework

### Inspiration

- Leadership competency frameworks from Harvard Business Review and DDI
- Modern full-stack architecture patterns from Vercel and FastAPI teams
- AI-powered coaching insights from research in personalized learning

### Educational Support

- **Masterschool**: For providing the AI Software Engineering program
- **Mentors & Peers**: For valuable feedback and guidance throughout development

---

## Contact & Support

**Developer**: Anca (Masterschool AI Engineering Capstone Project)

For questions, feedback, or collaboration inquiries:

- GitHub Issues: [Create an issue](https://github.com/Anca-Afloroaei/Leadership_Coach/issues)
- Email: [To email click here](mailto:anca.afloroaei@gmail.com)

---

### Built with ❤️ using Next.js, FastAPI, and OpenAI

#### Empowering leaders to grow through AI-driven insights

[⬆ Back to Top](#leadership-coach)

</div>

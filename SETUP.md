# Battery Test Application - Setup Guide

## Prerequisites

1. Python 3.8 or higher
2. PostgreSQL 12 or higher
3. Supabase account (for database hosting)
4. Git (for version control)

## Environment Setup

1. **Clone the repository and navigate to the project directory**
   ```bash
   git clone <repository-url>
   cd battery_test_application
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Database Configuration

1. **Create a Supabase Project**
   - Go to [Supabase](https://supabase.com)
   - Create a new project
   - Go to Project Settings -> Database
   - In the "Connection Info" section, find the "Connection Strings"
   - Use the "Direct Connection" string (NOT pooler connections)
   - Note down the following details:
     - Project URL
     - API Key (anon public)
     - Database Password
     - JWT Secret

2. **Configure Environment Variables**
   Create a `.env` file in the root directory with the following content:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   SUPABASE_JWT_SECRET=your_jwt_secret

   # Backend Configuration
   BACKEND_CORS_ORIGINS=["http://localhost:8501"]
   API_V1_STR=/api/v1
   PROJECT_NAME=battery_test_application

   # Security
   SECRET_KEY=your_generated_secret_key  # Generate using: openssl rand -hex 32
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Database
   # Use the Direct Connection string from Supabase
   # Replace your-password and your-project-ref with actual values
   DATABASE_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres
   # Note: Make sure to URL-encode any special characters in your password

   # Monitoring
   ENABLE_METRICS=true
   ```

   > **Important**: Use the Direct Connection string because:
   > - The application implements its own connection pooling via SQLAlchemy
   > - We need full SQL functionality for migrations
   > - Direct connections work best with SQLAlchemy ORM
   > - The pooling is handled efficiently by our application layer

3. **Initialize the Database**
   ```bash
   # From the project root directory
   python scripts/init_db.py
   ```

## Running the Application

1. **Start the Application (Both Backend and Frontend)**
   ```bash
   # From the project root directory
   python scripts/run.py
   ```
   This will start:
   - FastAPI backend on http://localhost:8000
   - Streamlit frontend on http://localhost:8501

2. **Access the Application**
   - Frontend Dashboard: http://localhost:8501
   - API Documentation: http://localhost:8000/docs
   - API Health Check: http://localhost:8000/health
   - Metrics: http://localhost:8000/metrics

## Directory Structure Overview

```
battery_test_application/
├── backend/
│   ├── alembic/          # Database migrations
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── db/           # Database models
│   │   ├── schemas/      # Pydantic models
│   │   └── services/     # Business logic
│   └── tests/            # Backend tests
├── frontend/
│   ├── pages/            # Streamlit pages
│   └── components/       # UI components
└── scripts/              # Utility scripts
```

## Common Issues and Solutions

1. **Database Connection Issues**
   - Verify Supabase credentials in `.env`
   - Check if the database URL is correctly formatted
   - Ensure the database password is URL-encoded

2. **CORS Errors**
   - Verify BACKEND_CORS_ORIGINS in `.env` includes your frontend URL
   - Check if the frontend is using the correct API base URL

3. **Port Conflicts**
   - If ports 8000 or 8501 are in use, you can modify them:
     - Backend: Change the port in `scripts/run.py`
     - Frontend: Use `streamlit run frontend/Home.py --server.port 8502`

## Development Workflow

1. **Making Database Changes**
   ```bash
   # Create a new migration
   cd backend
   alembic revision --autogenerate -m "description"

   # Apply migrations
   alembic upgrade head
   ```

2. **Running Tests**
   ```bash
   # Run backend tests
   pytest backend/tests
   ```

3. **Monitoring**
   - Access Prometheus metrics at http://localhost:8000/metrics
   - Monitor application health at http://localhost:8000/health

## Security Considerations

1. **Environment Variables**
   - Never commit `.env` file to version control
   - Use strong, unique values for SECRET_KEY
   - Rotate API keys periodically

2. **Database Access**
   - Use connection pooling (already configured)
   - Implement proper database user permissions
   - Enable SSL for database connections

3. **API Security**
   - All endpoints are CORS-protected
   - JWT authentication is implemented
   - Rate limiting is enabled

## Deployment Considerations

1. **Production Environment**
   - Use production-grade WSGI server (e.g., Gunicorn)
   - Enable HTTPS
   - Configure proper logging
   - Set up monitoring alerts

2. **Database**
   - Regular backups
   - Connection pooling
   - Query optimization

3. **Frontend**
   - Static file serving
   - CDN integration
   - Caching strategies 
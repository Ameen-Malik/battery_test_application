# Battery Testing Application

A comprehensive application for managing battery testing processes, built with FastAPI, Streamlit, and Supabase.

## 🚀 Quick Start Guide

### Step 1: Prerequisites

Before you begin, make sure you have the following installed:
- [Python 3.8 or higher](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- A text editor (like [VS Code](https://code.visualstudio.com/))
- A [Supabase](https://supabase.com) account (free tier works fine)

### Step 2: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/battery_test_application.git

# Navigate to the project directory
cd battery_test_application
```

### Step 3: Set Up Python Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 5: Set Up Supabase

1. Go to [Supabase](https://supabase.com) and create an account
2. Create a new project
3. Once the project is created, go to:
   - Project Settings → Database
   - Look for "Connection Info" section
   - Find "Connection Strings"
   - Copy the "Direct Connection" string (NOT the pooler connections)

### Step 6: Configure Environment Variables

1. Create a new file named `.env` in the project root directory
2. Copy the content from `.env.example`
3. Fill in your Supabase details:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   SUPABASE_JWT_SECRET=your_jwt_secret

   # Backend Configuration
   API_V1_STR=/api/v1
   PROJECT_NAME=battery_test_application

   # Security
   # Generate using: openssl rand -hex 32
   SECRET_KEY=your_generated_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Database
   # Use the Direct Connection string from Supabase (NOT pooler connections)
   # Make sure to URL-encode any special characters in the password
   DATABASE_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres

   # Monitoring
   ENABLE_METRICS=true
   ```

### Step 7: Initialize the Database

```bash
# Run the database initialization script
python scripts/init_db.py
```

### Step 8: Start the Application

```bash
# Run both backend and frontend
python scripts/run.py
```

The application will start and you can access:
- Frontend: http://localhost:8501
- API Documentation: http://localhost:8000/docs
- API Health Check: http://localhost:8000/health

## 📱 Features

- Test setup and configuration
- OCV/CCV reading collection
- Real-time test progress tracking
- CSV report generation
- Test status dashboard
- Data retention management

## 🏗️ Project Structure

```
battery_test_application/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── db/             # Database models
│   │   ├── schemas/        # Pydantic models
│   │   └── services/       # Business logic
│   └── tests/              # Backend tests
├── frontend/               # Streamlit frontend
│   ├── pages/             # Streamlit pages
│   └── components/        # UI components
└── scripts/               # Utility scripts
```

## 🔧 Common Issues & Solutions

### 1. Database Connection Issues
- Double-check your Supabase credentials in `.env`
- Ensure your database URL is correctly formatted
- Make sure to URL-encode special characters in your database password

### 2. Application Won't Start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if ports 8000 and 8501 are available
- Make sure your virtual environment is activated

### 3. CORS Errors
- CORS origins are hardcoded in the application to include `http://localhost:8501` and `http://127.0.0.1:8501`
- If you need to add additional origins, you'll need to update the `BACKEND_CORS_ORIGINS` list in `backend/app/core/config.py`
- Check if frontend is using correct API base URL
- If using a custom domain, ensure it's added to the CORS origins list in the config file

## 🛠️ Development

### Running Tests
```bash
pytest backend/tests
```

### Database Migrations
```bash
# Create a new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Need Help?

If you encounter any issues:
1. Check the Common Issues section above
2. Review the detailed setup guide in `SETUP.md`
3. Open an issue in the repository
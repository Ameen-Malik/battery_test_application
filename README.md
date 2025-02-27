# Battery Testing Application MVP

A comprehensive application for managing battery testing processes, built with FastAPI, Streamlit, and Supabase.

## Features

- Test setup and configuration
- OCV/CCV reading collection
- Real-time test progress tracking
- CSV report generation
- Test status dashboard
- Data retention management

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Testing**: pytest
- **Monitoring**: Prometheus

## Project Structure

```
battery_test_application/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── db/             # Database models and migrations
│   │   ├── schemas/        # Pydantic models
│   │   └── services/       # Business logic
│   └── tests/              # Backend tests
├── frontend/               # Streamlit frontend
│   ├── pages/             # Streamlit pages
│   ├── components/        # Reusable components
│   └── utils/             # Utility functions
└── scripts/               # Utility scripts
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/battery_test_application.git
   cd battery_test_application
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Supabase credentials and other configuration

5. Initialize the database:
   ```bash
   cd backend
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

7. Start the Streamlit frontend (in a new terminal):
   ```bash
   cd frontend
   streamlit run Home.py
   ```

## Development

### Running Tests
```bash
pytest backend/tests
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
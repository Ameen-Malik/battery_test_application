# Changelog

All notable changes to the Battery Test Application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Added missing `pydantic-settings` package to requirements.txt
- Updated pydantic to version 2.0 or higher for compatibility
- Fixed CORS configuration issues:
  - Hardcoded CORS origins in config.py instead of using environment variables
  - Removed BACKEND_CORS_ORIGINS from .env file
  - Added localhost variations to CORS origins list
- Added robust boolean environment variable parsing
- Added explicit env_file configuration in Settings

### Security
- Added proper environment variable validation and sanitization
- Updated environment variable handling to ensure proper validation
- Enhanced CORS configuration validation to prevent security misconfigurations
- Improved input sanitization for CORS origins

### Added
- Comprehensive setup guide (SETUP.md) with:
  - Detailed installation instructions
  - Environment configuration guide
  - Common issues and solutions
  - Development workflow documentation
  - Security considerations
  - Deployment guidelines
- Added version constraints for critical dependencies:
  - pydantic>=2.0
  - pydantic-settings>=2.0

### Changed
- Removed version numbers from requirements.txt to use latest package versions
- Clarified database connection string usage in setup guide:
  - Specified use of Direct Connection string from Supabase
  - Added explanation for connection type choice
  - Improved database configuration instructions
- Enhanced README.md with beginner-friendly instructions:
  - Added step-by-step Quick Start Guide
  - Included platform-specific commands (Windows/macOS/Linux)
  - Added visual organization with emojis
  - Expanded common issues and solutions section
  - Added links to all required external resources
  - Improved code block formatting and section headers
- Updated environment variable documentation:
  - Added proper formatting examples
  - Included validation requirements
  - Improved error messages

### Added
- Initial project setup and structure
- FastAPI backend implementation
  - Database models for tests, banks, cycles, and readings
  - Pydantic schemas for data validation
  - API endpoints for CRUD operations
  - Async database operations with SQLAlchemy
  - Database migrations with Alembic
  - CORS middleware configuration
  - Prometheus metrics integration
  - Health check endpoints

- Streamlit frontend implementation
  - Dashboard with test overview
  - Test setup form with validation
  - OCV/CCV reading input interface
  - Report generation and CSV export
  - Real-time test progress tracking
  - Interactive data visualization

- Database Schema
  - Tests table for managing test records
  - Banks table for test bank configuration
  - Cycles table for test cycles
  - Readings table for OCV/CCV readings
  - Cell Values table for individual cell measurements

- Configuration and Deployment
  - Environment variables configuration
  - Database initialization script
  - Application runner script for concurrent backend/frontend
  - Requirements.txt with all dependencies

### Technical Details
- Implemented async database operations for better performance
- Added data validation using Pydantic models
- Set up proper error handling and logging
- Configured CORS for frontend-backend communication
- Implemented database connection pooling
- Added Prometheus metrics for monitoring
- Created comprehensive API documentation

## [0.1.0] - 2024-02-27
- Initial release with core functionality 
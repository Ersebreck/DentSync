# DentalSync - Dental Clinic Management System

## Overview
DentalSync is an open-source dental clinic management system designed to streamline dental practice operations, enhance patient care, and improve business intelligence capabilities. The system provides comprehensive tools for patient management, appointment scheduling, treatment tracking, and clinic administration.

## Features

### Core Features
- **Patient Management**
  - Patient registration and profiles
  - Medical history tracking
  - Treatment records
  - Appointment history

- **Appointment System**
  - Intelligent scheduling
  - Calendar management
  - Conflict detection
  - Automated reminders

- **Treatment Management**
  - Standard treatment catalog
  - Treatment planning
  - History tracking
  - Cost management

- **User Management**
  - Role-based access control
  - Staff management
  - Security features
  - Authentication system

## Technology Stack

- **Backend**
  - FastAPI (Python web framework)
  - SQLAlchemy (ORM)
  - PostgreSQL (Database)
  - Alembic (Database migrations)

- **Frontend**
  - Streamlit (MVP interface)
  - React (Production interface - planned)

- **Infrastructure**
  - Docker
  - Docker Compose
  - PostgreSQL
  - PgAdmin

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dentalsync.git
cd dentalsync
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Configure your environment variables in `.env`

4. Start the application:
```bash
docker-compose up -d
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend (Streamlit): http://localhost:8501
- PgAdmin: http://localhost:5050

## Project Structure
```
DentalSync/
├── backend/              # Main backend application
│   ├── app/             # Application package
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core functionality, config
│   │   ├── db/          # Database related code
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic models
│   │   └── services/    # Business logic
│   ├── tests/           # Test files
│   ├── alembic/         # Database migrations
│   └── requirements/    # Python dependencies
├── frontend-mvp/        # Streamlit frontend
├── docker/             # Docker related files
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest
```

### Database Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head
```

## User Roles and Permissions

### Admin/Management
- Complete system access
- Business analytics
- Staff management
- Financial reports

### Dentists
- Patient records access
- Treatment planning
- Appointment schedule
- Medical history review

### Staff
- Appointment management
- Patient registration
- Basic inventory
- Communication handling

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Security

DentalSync takes security seriously. The system is designed with HIPAA compliance in mind and implements various security measures including:
- Encrypted data storage
- Secure authentication
- Role-based access control
- Audit logging
- Data backup systems

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Open an issue in the GitHub repository
- Contact the development team
- Check the documentation

## Roadmap

See our [Development Roadmap](ROADMAP.md) for detailed information about future developments and planned features.

## Acknowledgments

- All contributors and maintainers
- Open source community
- Healthcare professionals who provided valuable feedback
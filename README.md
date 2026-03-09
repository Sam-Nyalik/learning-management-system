# Workbook Learning Platform

A comprehensive, role-based learning management system (LMS) designed for structured educational content delivery. This platform enables Directors to manage curriculum structure, Teachers to create and grade assessments, and Students to submit interactive assignments.


## Key Features

- **Role-Based Workflows**: Tailored dashboards for Directors, Teachers, and Students.
- **Curriculum Management**: Hierarchical organization of content into Workbooks and Worksheets.
- **Interactive Assessment**: Real-time question submission and teacher-led grading.
- **Grade Approval System**: Built-in verification workflow for Directors to review and approve student grades.
- **Secure Authentication**: JWT-based secure login and session persistence.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Streamlit
- **Migrations**: Alembic
- **Security**: Passlib (Bcrypt), Python-JOSE

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL (running locally or remotely)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sam-Nyalik/learning-management-system.git
   cd workbook-app
   ```

2. **Configure Backend**:
   ```bash
   cd backend
   # Create a virtual environment
   python -m venv workbook_app_venv
   source workbook_app_venv/bin/activate  # Mac/Linux
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - Create a file named `.env` in the `backend/` directory (use the template provided in the documentation).
   - Run migrations:
     ```bash
     alembic upgrade head
     ```

### Running the Project

You will need two terminal windows:

- **Terminal 1 (Backend)**:
  ```bash
  cd backend
  source workbook_app_venv/bin/activate
  uvicorn app.main:app --reload
  ```

- **Terminal 2 (Frontend)**:
  ```bash
  cd frontend
  streamlit run app.py
  ```

The application will be available at `http://localhost:8501`.

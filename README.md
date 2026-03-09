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


### Screenshots
<img width="1470" height="956" alt="Screenshot 2026-03-10 at 00 10 25" src="https://github.com/user-attachments/assets/0632dea8-c7b5-49b2-bc1a-2aa2f36548b0" />
<img width="1470" height="956" alt="Screenshot 2026-03-10 at 00 10 47" src="https://github.com/user-attachments/assets/38353927-68e7-4607-a494-a94c1f30ba33" />
<img width="1470" height="956" alt="Screenshot 2026-03-10 at 00 11 43" src="https://github.com/user-attachments/assets/c686c921-2eca-417e-84aa-fc413bd48b94" />


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

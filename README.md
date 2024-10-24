# 🌟 Employee Management System

An Employee Management API built using FastAPI and PostgreSQL, featuring JWT-based authentication, role-based access control (RBAC), and efficient background processing for salary calculations.

## 🚀 Features

- **🔐 JWT Authentication:** Secure authentication using JSON Web Tokens (JWT).
- **🛡️ Role-Based Access Control:** Different access levels for Admin and Employee roles.
- **🗂️ Employee CRUD Operations:** Admins can Create, Read, Update, and Delete employee records.
- **💸 Salary Processing:** Background job handling for calculating employee salaries.
- **📊 PostgreSQL Integration:** Database management with SQLAlchemy ORM and PostgreSQL.
- **🔄 Alembic Migrations:** Seamless database migrations using Alembic.
- **⚙️ Configurable Environment:** Adjust database connections, JWT settings, and more via .env configuration.
- **🧪 Unit Testing:** Comprehensive testing with pytest for reliable API operations.

## 🛠️ Technology Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migration Tool:** Alembic
- **Authentication:** JWT
- **Background Processing:** FastAPI BackgroundTasks
- **Unit Testing:** pytest

## 🛡️ Role-Based Access Control (RBAC)

- **Admin:**
  - Full access to all employee-related operations (create, update, delete, salary calculation).

- **Employee:**
  - Limited access to view and update their own information.

## ⚙️ Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sanjaymehar/FastApiTask.git
   cd FastApiTask
   
2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    To activate:
    Windows CMD: venv/Scripts/activate.bat
    Windows PowerShell: ./venv/bin/activate
    macOS / Linux: source venv/bin/activate
   
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Configure environment variables:**
  Create a .env file in the root directory and add the following configuration:
   
    ```bash
    DB_HOST=localhost       # your database host
    DB_PORT=5432            # your database port
    DB_USER='postgres'      # your database user
    DB_PASSWORD='admin'     # your database password
    DB_NAME='fast_api_task' # your database name
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    SECRET_KEY=SECRET_KEY
   
5. **Set up PostgreSQL:**
  Ensure that PostgreSQL is running, and create a database:

6. **Run database migrations:**
   ```bash
    alembic upgrade head

7. **Start the FastAPI server:**
     ```bash
    uvicorn app.main:app --reload

## 📡 API Endpoints

### Authentication

- **🔑 Login:** `POST /user/login`
  - Authenticates the user and provides a JWT token on successful login.
  - **Request Body:**
    ```json
    {
      "username": "larry",
      "password": "admin123"
    }
    ```
  - **Response Body:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsYXJyeSIsImV4cCI6MTcyOTc1MDE3NX0.QFkmsx3uG4awMwn3y0HeXDpbiJmkFXOVaj1aIYnIyv4",
      "token_type": "bearer"
    }
    ```

- **👤 Register:** `POST /user`
  - Admins can create new employee or admin users.
  - **Request Body:**
    ```json
    {
      "username": "larry",
      "password": "admin123",
      "role": "admin"
    }
    ```
  - **Response Body:**
    ```json
    {
      "id": 3,
      "username": "larry",
      "role": "admin"
    }
    ```

### User Management

- **👥 Get All Users:** `GET /user?skip=0&limit=10`
  - Retrieve all users, including admin and employee roles.
  - **Response Body:**
    ```json
    [
      {
        "id": 1,
        "username": "ram",
        "role": "admin"
      },
      {
        "id": 2,
        "username": "siya",
        "role": "employee"
      },
      {
        "id": 3,
        "username": "larry",
        "role": "admin"
      }
    ]
    ```

### Employee Management (Admin Only)

- **➕ Create Employee:** `POST /api/v1/employee`
  - Create a new employee profile with necessary details (admin only).
  - **Request Body:**
    ```json
    {
      "employee_id": 2,
      "name": "siya",
      "designation": "manager",
      "department": "sales",
      "joining_date": "2024-10-24"
    }
    ```
  - **Response Body:**
    ```json
    {
      "id": 1,
      "employee_id": 2,
      "name": "siya",
      "designation": "manager",
      "department": "sales",
      "joining_date": "2024-10-24",
      "monthly_salary": 0
    }
    ```

- **👥 Get All Employees:** `GET /api/v1/employee?skip=0&limit=10`
  - Retrieve a list of all employees (admin only).
  - **Response Body:**
    ```json
    [
      {
        "id": 1,
        "employee_id": 2,
        "name": "siya",
        "designation": "manager",
        "department": "sales",
        "joining_date": "2024-10-24",
        "monthly_salary": 0
      }
    ]
    ```

- **📝 Update Employee:** `PUT /api/v1/employee/{employee_id}`
  - Update an employee's details using their `employee_id` (admin only).
  - **Request Body:**
    ```json
    {
      "name": "siya",
      "designation": "marketing manager",
      "department": "sales",
      "joining_date": "2024-10-24"
    }
    ```
  - **Response Body:**
    ```json
    {
      "id": 1,
      "employee_id": 2,
      "name": "siya",
      "designation": "marketing manager",
      "department": "sales",
      "joining_date": "2024-10-24",
      "monthly_salary": 0
    }
    ```

- **🗑️ Delete Employee:** `DELETE /api/v1/employee/{employee_id}`
  - Delete an employee record using their `employee_id` (admin only).
  - **Response Body:**
    ```json
    {
      "message": "Employee deleted successfully"
    }
    ```

### Salary Management (Admin Only)

- **💰 Submit Salary Data:** `POST /api/v1/salaries`
  - Admins can submit salary details (base salary and bonuses) for an employee.
  - **Request Body:**
    ```json
    {
      "employee_id": 2,
      "base_salary": 20000,
      "bonuses": 4000
    }
    ```
  - **Response Body:**
    ```json
    {
      "status": "Salary data submitted",
      "data": {
        "employee_id": 2,
        "base_salary": 20000,
        "created_at": "2024-10-24T11:22:29.194839+05:30",
        "bonuses": 4000,
        "id": 1
      }
    }
    ```

- **📜 Salary History:** `GET /api/v1/salaries/salary-history/{employee_id}`
  - Retrieve salary history for a specific employee using their `employee_id`.
  - **Response Body:**
    ```json
    {
      "employee_id": 2,
      "salary_history": [
        {
          "base_salary": 20000,
          "bonuses": 4000,
          "created_at": "2024-10-24 11:22:29"
        }
      ]
    }
    ```

## To create a new migration (when the schema changes):
```bash
   alembic revision --autogenerate -m "A description for the migration"
   ```
 
  

## 🧪 Running Tests

1. **Create Database name to Test and Change .env DB_NAME to Test:**

2. **Run test cases:**
   ```bash
   pytest -v

## 📧 Contact

For any questions, suggestions, or contributions, feel free to reach out to:

- **Author:** Sanjay Mehar
- **Email:** sanjaymeharr@gmail.com
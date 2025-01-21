# Throttling Mechanism for Authentication System

## Overview
This project implements a throttling mechanism in Python to protect an authentication system from brute force attacks. The system allows users to register, log in with valid credentials to obtain a bearer token for authentication, and enforces a throttling policy if incorrect credentials are used repeatedly.

## Features
1. **User Registration**: New users can register by providing their details.
2. **Authentication**: Users can log in using valid credentials to receive a bearer token for subsequent requests.
3. **Throttling**:
   - After 5 consecutive failed login attempts, the user is throttled for 15 minutes.
   - During the throttling period, login attempts are blocked.

## Prerequisites
- Python 3.7 or higher

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application
Run the following command to start the application:
```bash
python main:app --reload
```

### API Endpoints

#### 1. **User Registration**
   **Endpoint**: `/register`
   
   **Method**: POST
   
   **Request Body**:
   ```json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

   **Response**:
   ```json
   {
       "message": "User registered successfully."
   }
   ```

#### 2. **Login**
   **Endpoint**: `/login`
   
   **Method**: POST
   
   **Request Body**:
   ```json
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

   **Success Response**:
   ```json
   {
       "token": "your_bearer_token"
   }
   ```

   **Throttle Response** (after 5 failed attempts):
   ```json
   {
       "error": "Too many failed attempts. Please try again after 15 minutes."
   }
   ```

## Throttling Logic
1. Track login attempts for each user.
2. If a user fails to log in 5 times consecutively:
   - Block further login attempts for 15 minutes.
3. Reset the attempt counter after a successful login or after the throttling period expires.

## Dependencies
- Flask (for API development)
- PyJWT (for token generation)
- A database library (e.g., SQLite, SQLAlchemy)

Install all dependencies using the command:
```bash
pip install -r requirements.txt
```


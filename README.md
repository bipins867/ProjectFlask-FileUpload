# Flask File Management System

This is a simple Flask-based file management system with user authentication and file upload/download functionality.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

Make sure you have Python installed on your machine.

```bash
pip install -r requirements.txt
```

### Configuration

Set up your database configuration by creating a .env file with the following variables:

```bash
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASS=your_database_password
DB_NAME=your_database_name
JWT_SECRET=your_jwt_secret
```

## Running the Application

```bash
python app.py
```
The application will be accessible at http://127.0.0.1:5000/.

## API Endpoints

### * User Login:

POST /user/login
Parameters: email, password
User Sign-Up:

POST /user/signup
Parameters: email, password, is_ops_type (1 for ops user, 0 for client user)
Upload File:

POST /files/upload
Parameters: fileName, fileContent
List Files:

GET /files/download
Returns a list of available files.
Generate File Download Link:

POST /files/download
Parameters: file_id
Returns a download link.
Download File:

GET /files/download/:encoded
Download the file using the generated link.
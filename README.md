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

## * User Login:

- **METHOD:** POST
- **URL:** /user/login

### Parameters

- `email`:The email of the user.
- `password`: The password for the user.


## User Sign-Up

### Endpoint

- **Method:** POST
- **URL:** `/user/signup`

### Parameters

- `email`: The email of the user.
- `password`: The password for the user.
- `is_ops_type`: Type of user (1 for ops user, 0 for client user).



- **Upload File:**
  - *HTTP Method:* `POST`
  - *Endpoint:* `/files/upload`
  - *Parameters:*
    - `fileName`: The name of the file to be uploaded.
    - `fileContent`: The content of the file.

  This endpoint allows you to upload a file to the server.

- **List Files:**
  - *HTTP Method:* `GET`
  - *Endpoint:* `/files/download`
  - Returns a list of available files.

- **Generate File Download Link:**
  - *HTTP Method:* `POST`
  - *Endpoint:* `/files/download`
  - *Parameters:*
    - `file_id`: The ID of the file for which you want to generate a download link.
  - Returns a download link for the specified file.

- **Download File:**
  - *HTTP Method:* `GET`
  - *Endpoint:* `/files/download/:encoded`
  - Download the file using the generated link.
## Authentication

To access certain endpoints, use the x-access-token header with the JWT token obtained after logging in.

### Ops User Authorization 

SignUp,Login, Upload File


### Client User Authorization

SignUp,Login, Download File


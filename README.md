
# Welcome to Amali Backend

The Amali Backend is responsible for managing the core functionality of the Amali project. It handles the processing of athletes' and sponsors' data, facilitates communication between the web portal and mobile application, and interacts with the database for persistent storage. The backend application is built using various technologies to ensure efficient and secure data handling.

## Table of Contents
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)

## Key Features

The Amali Backend provides the following key features:

- **User Authentication and Authorization:** The backend implements user authentication and authorization mechanisms to secure access to the system. This includes user registration, login, logout, and password management.

- **API Endpoints:** The backend enables the implementation of API endpoints that expose functionality to the web portal and mobile application. These endpoints allow the frontend components to communicate with the backend and perform actions such as creating and retrieving athlete and sponsor profiles, connecting athletes, managing sponsorships, and handling notifications.

- **Database Interaction:** In developing the database models the backend implements the necessary logic to interact with the database. This includes creating, updating, and querying the database to store and retrieve athlete and sponsor information, sponsorship details, connection requests, and other relevant data.

## Technologies used

The Amali Backend utilizes the following technologies:

- **Front-end:** Next.js
- **Backend Language:** Python
- **Database:** PostgreSQL
- **Web Framework:** Django
- **Mobile:** Kotlin

## Getting Started

To get started with Amali Backend, follow these steps:

### Prerequisite

Ensure that you have Python (Version 3.9) and Django installed and properly configured in your development environment. Set up a PostgreSQL database and configure the necessary credentials.

### Installation
To run this Django project locally, please follow these steps:
- Clone the repository:
`git clone https://github.com/akirachix/Amali-Backend.git`
- Navigate to the project directory:
` cd Amali-Backend`
- Create a virtual environment:
`python -m venv <your environment name>`
- Activate the virtual environment:
  On Linux -`python manage.py source <environment name>/bin/activate`
- Install requirements:
`pip install -r requirements.txt`
- Apply migrations:
`python manage.py migrate`
- Run the development server:
`python manage.py runserver`

## Project Structure

The project structure of Amali Backend is as follows:

- `backend/`: Contains the Django project configuration files.
- `backend/app/`: Includes the Django app where the core backend logic resides.
- `backend/app/models.py`: Defines the data models used in the application.
- `backend/app/views.py`: Implements the views and API endpoints for handling HTTP requests.
- `backend/app/services.py`: Contains the service classes responsible for implementing the business logic.
- `backend/app/utils.py`: Includes utility functions and helper classes.
- `backend/app/tests/`: Includes unit tests for testing the backend functionality.
- `backend/app/migrations/`: Contains database migration files.
- `backend/manage.py`: Entry point script for managing Django commands.

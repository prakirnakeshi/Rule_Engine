# Dynamic Rule Engine Application

This project is a **Dynamic Rule Engine Application** built with **Django**. It allows users to create, modify, and evaluate rules based on user attributes for eligibility determination. The application leverages **Abstract Syntax Trees (AST)** for rule parsing and evaluation, making it flexible and efficient.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Code Structure](#code-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Create dynamic rules based on user-defined attributes.
- Modify existing rules easily through a user-friendly interface.
- Evaluate rules against user attributes for eligibility determination.
- Supports complex expressions using Abstract Syntax Trees for rule parsing.
- RESTful API endpoints for easy integration and interaction.

## Technologies Used

- **Django**: Web framework for building the application.
- **Python**: Programming language used for backend development.
- **Abstract Syntax Tree (AST)**: For parsing and evaluating rules.
- **SQLite**: Default database for storing rules and user data (can be configured to use others).
- **Django Rest Framework**: For building RESTful APIs.

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/prakirnakeshi/Rule_Engine.git
   cd Rule_Engine
2. Create a virtual environment:
  python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:
pip install -r requirements.txt

4. Apply migrations to set up the database:
python manage.py migrate

5.Run the development server:
python manage.py runserver

## Usage
- Use the provided forms to create and modify rules based on your requirements.
- Input user attributes and evaluate the rules to determine eligibility.

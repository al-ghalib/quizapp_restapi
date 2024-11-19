# Quizapp - RESTful API with Django

This is a simplified API implementation for a platform where students can practice MCQ-based questions, participate in exams, and track their performance. This project includes a basic database structure, API endpoints, and JSON-based responses to support the platform's core functionalities.

---

## Features

- **Retrieve Questions**: Fetch a list of questions and their choices.
- **Question Details**: View detailed information about a specific question.
- **Submit Answers**: Submit answers and receive a score for correctness.
- **User Practice History**: Track a user's practice history, including scores and attempted questions.

---

## Technology Stack

- **Backend Framework**: Django
- **Database**: SQLite 
- **API Development**: Django REST Framework (DRF)

---

## Installation

### Prerequisites
- Python 3.10+
- Virtual Environment
- `pip` for managing Python packages

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/al-ghalib/quizapp_restapi.git
   cd quizapp_restapi

2. Create and activate a virtual environment:
   ```bash
   pip install virtualenv
   virtualenv myenv
   .\myenv\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Apply migrations to set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. Run the development server:
   ```bash
   python manage.py runserver

6. Access the API at http://127.0.0.1:8000


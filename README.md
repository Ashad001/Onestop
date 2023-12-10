# Onestop-Digitilization Setup Guide (Windows)

Welcome to Python project! This guide will walk you through the process of setting up the project on a Windows machine.

## Clone the Repository

1. Fork this repository
2. Open Command Prompt or Git Bash.
3. Navigate to the directory where you want to clone the project.
4. Run the following command to clone the repository:

   ```bash
   git clone https://github.com/your-username/Onestop.git
   ```

   Replace `your-username` with your GitHub username.

## Create a Virtual Environment

1. Navigate to the project directory using Command Prompt or Git Bash:

   will be update at the end of the project

2. Create a virtual environment:

   ```bash
   python -m venv (your virtual environment name)
   ```
   For example:
   ```bash
   python -m venv venv
   ```
   
4. Activate the virtual environment:

   - Command Prompt:

     ```bash
     venv\Scripts\activate
     ```

   - Git Bash:

     ```bash
     source venv/Scripts/activate
     ```

## Install Dependencies

1. With the virtual environment active, install project dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```
   
## Run Django

1. In the Root directory run the following command:
   ```bash
   python3 Onestop/manage.py migrate
   python3 Onestop/manage.py runserver
   ```
   OR
   ```
   py Onestop/manage.py migrate
   py Onestop/manage.py runserver
   ```
2. Visit http://localhost:8000/ to access the platform.

   
## Technologies Used

1. Django: As the primary web framework for building the platform.
2. Python: To write backend logic and scripts.
3. HTML/CSS/JavaScript: For front-end development and user interface.
4. SQL: As the database system to store user data and information.

![Image](https://github.com/user-attachments/assets/fefd6798-9689-4675-95a0-79791da20adf)

# Django Project

This README provides instructions on how to set up and run this Django project locally using Pipenv.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package installer)
- pipenv (Python virtual environment management tool)

If you don't have pipenv installed, you can install it with:
```
pip install pipenv
```

## Getting Started

### 1. Clone the repository

```
git clone https://github.com/Bloul-Mohamed/coding-master-univ-lagh--backend.git  
cd coding-master-univ-lagh--backend
```

### 2. Set up the virtual environment and install dependencies

Using pipenv, create a virtual environment and install all dependencies:

```
pipenv install
```

This command will:
- Create a new virtual environment if one doesn't exist
- Install all packages listed in the Pipfile

### 3. Activate the virtual environment

```
pipenv shell
```

### 4. Set up the database

Run migrations to set up your database schema:

```
python manage.py migrate
```

### 5. Create a superuser (optional)

To access the Django admin interface, create a superuser:

```
python manage.py createsuperuser
```

### 6. Run the development server

```
python manage.py runserver
```

The server will start, typically at http://127.0.0.1:8000/

## Development Commands

- **Run tests**:
  ```
  python manage.py test
  ```

- **Create migrations after model changes**:
  ```
  python manage.py makemigrations
  ```

- **Collect static files**:
  ```
  python manage.py collectstatic
  ```

## Environment Variables

Create a `.env` file in the project root directory to store environment variables. These might include:

```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
```

## Using Pipenv for Package Management

- **Install a new package**:
  ```
  pipenv install package_name
  ```

- **Install a development package**:
  ```
  pipenv install package_name --dev
  ```

- **View the dependency graph**:
  ```
  pipenv graph
  ```

- **Update all packages**:
  ```
  pipenv update
  ```

## Troubleshooting

If you encounter issues:

1. Ensure all dependencies are installed:
   ```
   pipenv install --dev
   ```

2. Check for any missing migrations:
   ```
   python manage.py makemigrations
   ```

3. Verify your environment variables are set correctly

## Deployment

For deployment to production, additional steps are required:

1. Set appropriate environment variables (DEBUG=False, etc.)
2. Configure your web server (Nginx, Apache, etc.)
3. Set up a production-ready database (PostgreSQL, MySQL, etc.)
4. Configure static files serving

## License
univ-lagh

# Lost and Found Portal

A Django-based web application for managing lost and found items.

## Features

- User authentication and registration
- Add, edit, and delete lost/found items
- Item matching system
- User profiles and messaging
- Image upload support
- Responsive design with Bootstrap

## Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default)
- **Image Processing**: Pillow
- **Forms**: Django Crispy Forms with Bootstrap 4

## Prerequisites

- Python 3.8 or higher
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Lost-and-Found-Portal
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
# Option 1: Using the batch file
activate_venv.bat

# Option 2: Manual activation
venv\Scripts\activate

# Option 3: Git Bash
source venv/Scripts/activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
cd lostfound_project
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
Lost-and-Found-Portal/
├── lostfound_project/          # Django project directory
│   ├── lostfound_project/      # Project settings
│   ├── portal/                 # Main app
│   ├── media/                  # User uploaded files
│   └── manage.py              # Django management script
├── venv/                       # Virtual environment (not in Git)
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore file
├── activate_venv.bat          # Windows activation script
└── README.md                  # This file
```

### Common Issues & Solutions

#### Issue: Virtual environment not activating
**Solution**: Make sure you're using the correct activation command for your shell:
- Windows Command Prompt: `venv\Scripts\activate.bat`
- Windows Git Bash: `source venv/Scripts/activate`
- Linux/Mac: `source venv/bin/activate`

#### Issue: Python version mismatch
**Solution**: Ensure you're using Python 3.8+ and recreate the virtual environment:
```bash
rm -rf venv
python -m venv venv
source venv/bin/activate  # or appropriate activation command
pip install -r requirements.txt
```

#### Issue: Package installation errors
**Solution**: Update pip and try again:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Creating New Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## Support

For issues and questions, please create an issue in the repository. 
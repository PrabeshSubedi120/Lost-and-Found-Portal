# Lost and Found Portal

A modern, community-driven web application for reporting, searching, and recovering lost and found items. Built with Django and Bootstrap, this portal helps users connect and return lost belongings efficiently.

## Features
- Register, login, and manage your account
- User profile with avatar and bio
- Dashboard with stats: total items, lost, found, recovered
- Add, edit, and delete lost or found items with images, location, and contact info
- Search and filter items by name, category, and location
- Responsive, modern UI with interactive elements
- Secure authentication and permissions

## Tech Stack
- **Backend:** Django 5
- **Frontend:** Bootstrap 5, Font Awesome, Google Fonts
- **Database:** SQLite (default, easy to switch)
- **Other:** Pillow (image uploads), Crispy Forms (form styling)

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd "Lost and found Portel"
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install manually:
   ```bash
   pip install django pillow django-crispy-forms crispy-bootstrap4
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the portal:**
   Open [http://localhost:8000/](http://localhost:8000/) in your browser.

## Usage
- Register a new account or log in.
- Edit your profile and upload an avatar.
- Add lost or found items with details and images.
- Use the search and filter bar to find items by name, category, or location.
- Edit or delete your own items from their detail pages.
- View real-time stats on the dashboard.

## Folder Structure
- `lostfound_project/` - Django project root
  - `portal/` - Main app (models, views, templates, forms)
  - `media/` - Uploaded item images
  - `db.sqlite3` - SQLite database (default)
  - `manage.py` - Django management script
- `venv/` - Python virtual environment (not required for deployment)

## Credits
- **Built by Prabesh Subedi**
- UI/UX: Bootstrap, Font Awesome, Google Fonts
- Special thanks to the Django and open-source community

---

Feel free to contribute or suggest improvements! 
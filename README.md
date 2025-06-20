Secure File Sharing System – Installation & Run Guide
------------------------------------------------------

This document provides the steps to set up and run the Django-based Secure File Sharing System.

Prerequisites:
---------------------
1. Python 3.11 or newer must be installed.
   Download: https://www.python.org/downloads/

2. Git must be installed (for cloning or if required).
   Download: https://git-scm.com/downloads

3. Internet connection is required (for IPFS + Pinata access).

------------------------------------------------------

Folder Structure:
---------------------
- manage.py
- requirements.txt
- .env                    ← Contains API keys (must be configured)
- db.sqlite3              ← Default SQLite database
- /accounts               ← User auth app
- /djfsender              ← Core file-sharing app
- /djipfs                 ← Project folder
- /media                  ← Encrypted file storage
- /static                 ← CSS, JS, images
- /templates              ← HTML templates

------------------------------------------------------

Setup Instructions:
----------------------

1. Open terminal or command prompt and go to the project root folder:

   > cd Secure-File-Sharing-System

2. Create a virtual environment:

   > python -m venv .venv

3. Activate the virtual environment:

   - On Windows:
     > .venv\Scripts\activate

   - On macOS/Linux:
     > source .venv/bin/activate

4. Install all dependencies:

   > pip install -r requirements.txt

5. Create the `.env` file in the root directory (if not already included).
   Example `.env` file:

	SECRET_KEY=your-django-secret-key
	DEBUG=True
	ALLOWED_HOSTS=127.0.0.1,localhost
	ADMIN_PATH=admin
	PINETA_JWT=your_pinata_jwt_token
	PINETA_API_KEY=your_pinata_api_key
	PINETA_API_SECRET=your_pinata_api_secret

6. Run migrations (this sets up the database tables):

> python manage.py migrate

7. (Optional) Create a superuser for admin access:

> python manage.py createsuperuser

8. Start the server:

> python manage.py runserver

9. Open browser and visit:

http://127.0.0.1:8000/

------------------------------------------------------

Troubleshooting:
----------------------

- If "no such table: auth_user" → Make sure to run:
> python manage.py migrate

- If CSS or images do not load:
- Ensure static files are in the `/static` folder.
- Run server with DEBUG=True

- If Pinata upload fails:
- Double-check `.env` API keys.
- Test Pinata API separately using provided script.

------------------------------------------------------

Default Routes:
----------------------

- Home / Landing Page:         http://127.0.0.1:8000/
- Login:                       http://127.0.0.1:8000/accounts/login/
- Register:                    http://127.0.0.1:8000/accounts/register/
- Upload File:                 http://127.0.0.1:8000/upload/
- My Uploaded Files:           http://127.0.0.1:8000/my-files/
- Shared Files:                http://127.0.0.1:8000/shared/
- Admin Panel:                 http://127.0.0.1:8000/admin/

------------------------------------------------------

# Street Access

Street Access is a beginner-friendly Django e-commerce prototype for streetwear. The app includes product browsing, authentication, a cart, checkout flow, and a simple user profile page.

## Project Overview

- Built with **Django 6.x** and **SQLite**.
- Contains a single Django app: `store`.
- Uses session-based cart storage and JSON add-to-cart actions.
- Includes templates for home, shop, cart, checkout, login, signup, and profile pages.
- Uses static assets in `static/store/css`, `static/store/js`, and `static/store/images`.

## Key Features

- Home page with featured products and hero section.
- Product listing page for all available items.
- User authentication: sign up, login, logout.
- Profile page with editable user details and past orders.
- Cart page with quantity updates and item removal.
- Checkout flow that creates orders and order items.
- Live cart count badge in the header.
- Simple admin support via Django admin.

## Application Structure

- `manage.py` — Django command-line utility.
- `street_access/` — project settings and URL configuration.
  - `settings.py` — app configuration, installed apps, database, templates, and static files.
  - `urls.py` — root URL routing.
- `store/` — main application.
  - `models.py` — `Product`, `Order`, and `OrderItem` models.
  - `views.py` — view functions for app pages and cart actions.
  - `urls.py` — app-specific routes.
  - `templates/store/` — HTML templates for the site.
  - `context_processors.py` — global `cart_count` context provider.
- `static/store/` — CSS, JavaScript, and images used by templates.
- `db.sqlite3` — SQLite database file.

## Routes

- `/` — Home page
- `/products/` — Product catalog
- `/cart/` — Shopping cart
- `/checkout/` — Checkout page
- `/checkout_success/` — Order success page
- `/login/` — Login page
- `/signup/` — Sign up page
- `/profile/` — Profile and order history page
- `/admin/` — Django admin interface

## Setup

### Prerequisites

- Python 3.10+ (Python 3.14 is compatible with Django 6.x)
- `pip`

### Install dependencies

There is no `requirements.txt` file in this repository, but the app requires Django and standard Django dependencies. Run:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install django==6.0.5
```

### Database migrations

Run migrations to create the SQLite schema:

```bash
python manage.py migrate
```

### Create a superuser (optional)

To access the Django admin interface:

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Notes

- The app uses `db.sqlite3` as the default database.
- Static assets are loaded from the `static/` folder; the project is configured to serve them in development.
- Product images are referenced from `/static/store/images/`.
- Cart storage uses Django sessions, so the cart is tied to the browser session and logged-in user.

## Recommended Improvements

- Add a `requirements.txt` entry.
- Add unit tests for views and models.
- Add product management in the admin or a dedicated dashboard.
- Improve checkout form validation and payment flow.

## How it works

- `store/views.py` handles page rendering and AJAX cart actions.
- `add_to_cart/` updates the session cart and returns the updated item count.
- `checkout/` creates `Order` and `OrderItem` records when the user submits the form.
- `store/context_processors.py` exposes `cart_count` globally so the header badge updates correctly.

Enjoy exploring the Street Access Django app!
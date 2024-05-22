# Vendor Management System

## Overview
This project is a Vendor Management System built using Django. It is designed to manage vendor details, purchase orders, and track vendor performance over time. The system includes custom user authentication using JWT (JSON Web Tokens) for secure access to the API endpoints.

## Features
- Custom User Model with email as the primary identifier
- JWT-based authentication for secure access
- Vendor management: Create, read, update, and delete vendor details
- Purchase Order management: Create, read, update, and delete purchase orders
- Track and update historical performance metrics for vendors
- Admin interface customization for a cleaner user experience

## Project Structure
The project is structured as follows:

```
vendor_project/
│
├── manage.py
├── vendor_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── vendor_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── helper.py
│   ├── models.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
```

## Installation

1. **Clone the repository:**
   ```sh
   git clone <repository_url>
   cd vendor_project
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```sh
   python manage.py runserver
   ```

## Usage

### Authentication
- **Login:** `POST /api/login/`
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```

### Vendor Management
- **Create Vendor:** `POST /api/vendors/`
  ```json
  {
    "full_name": "Vendor Name",
    "contact_details": "1234567890",
    "address": "Vendor Address"
  }
  ```
- **Get All Vendors:** `GET /api/vendors/`
- **Get Vendor by ID:** `GET /api/vendors/<vendor_id>/`
- **Update Vendor:** `PUT /api/vendors/<vendor_id>/`
- **Delete Vendor:** `DELETE /api/vendors/<vendor_id>/`

### Purchase Order Management
- **Create Purchase Order:** `POST /api/purchase_orders/`
  ```json
  {
    "vendor": "vendor_id",
    "order_date": "2023-05-20T14:30:00Z",
    "delivery_date": "2023-05-27T14:30:00Z",
    "items": [{"item_id": "123", "quantity": 10}],
    "quantity": 10,
    "status": "PENDING",
    "quality_rating": 4.5,
    "issue_date": "2023-05-20T14:30:00Z",
    "acknowledgment_date": "2023-05-21T14:30:00Z"
  }
  ```
- **Get All Purchase Orders:** `GET /api/purchase_orders/`
- **Get Purchase Order by ID:** `GET /api/purchase_orders/<po_id>/`
- **Update Purchase Order:** `PUT /api/purchase_orders/<po_id>/`
- **Delete Purchase Order:** `DELETE /api/purchase_orders/<po_id>/`
- **Acknowledge Purchase Order:** `POST /api/purchase_orders/<po_id>/acknowledge`

### Vendor Performance
- **Get Vendor Performance:** `GET /api/vendors/<vendor_id>/performance`

## Custom User Model
The project uses a custom user model with email as the primary identifier instead of a username. This is managed by `CustomUser` and `CustomUserManager` classes in `models.py`.

## JWT Authentication
The project uses `rest_framework_simplejwt` for JWT-based authentication. The settings are configured in `settings.py` under the `SIMPLE_JWT` configuration.

## Admin Customization
The admin interface is customized to provide a cleaner view for managing users, vendors, and purchase orders. This is handled in `admin.py`.

## Signals
Django signals are used to update vendor performance metrics automatically when a purchase order is saved. This is implemented in `signals.py`.

## Helper Functions
Helper functions such as token generation and updating historical performance are located in `helper.py`.

## Additional Notes
- Ensure you have Python 3.8+ installed.
- Use a proper database for production (the project uses SQLite for development).
- Set `DEBUG` to `False` in production and configure `ALLOWED_HOSTS`.

## License
This project is licensed under the MIT License.

---

By following the above instructions, you should be able to set up and run the Vendor Management System on your local machine. If you have any issues or questions, please feel free to contact the repository owner.
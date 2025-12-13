# Shine Art Studio - Photography POS System

## Overview

A fully offline, production-ready desktop POS system for photography studios built with Python and CustomTkinter.

## Features

- User Authentication (Admin & Staff roles)
- Customer Management
- Photography Services Management
- Photo Frame Inventory Management
- Billing & Invoice Generation (PDF)
- Booking/Photoshoot Management
- Invoice History & Reprinting
- Role-based Access Control
- Dark Mode UI

## Tech Stack

- Python 3
- CustomTkinter (UI)
- SQLite (Database)
- ReportLab (PDF Generation)
- Fully Offline

## Installation

1. Install Python 3.8 or higher

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Default Credentials

### Admin Account

- Username: `admin`
- Password: `admin123`

### Staff Account

- Username: `staff`
- Password: `staff123`

## Project Structure

```
pos_system/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── pos_database.db        # SQLite database (auto-created)
├── auth/                  # Authentication module
│   ├── __init__.py
│   └── auth_manager.py    # User authentication & management
├── database/              # Database layer
│   ├── __init__.py
│   ├── schema.py          # Database schema & initialization
│   └── db_manager.py      # Database operations
├── services/              # Business services
│   ├── __init__.py
│   └── invoice_generator.py  # PDF invoice generation
├── ui/                    # User interface
│   ├── __init__.py
│   ├── components.py      # Shared UI components
│   ├── customer_frame.py  # Customer management
│   ├── service_frame.py   # Service management
│   ├── frame_frame.py     # Photo frame management
│   ├── billing_frame.py   # Billing & invoicing
│   ├── booking_frame.py   # Booking management
│   └── invoice_history_frame.py  # Invoice history
└── invoices/              # Generated PDF invoices (auto-created)
```

## User Roles & Permissions

### Admin

- Full access to all features
- Can delete records
- Can manage users

### Staff

- Limited access
- Cannot delete critical records
- Cannot manage users

## Database Schema

- **users** - System users with authentication
- **customers** - Customer information
- **services** - Photography services with pricing
- **photo_frames** - Frame inventory with stock tracking
- **invoices** - Invoice headers
- **invoice_items** - Invoice line items
- **bookings** - Photoshoot bookings

## Key Features

### Billing Module

- Quick customer lookup
- Add services and frames to cart
- Discount support
- Payment tracking (paid amount & balance)
- Automatic PDF invoice generation
- Stock quantity updates for frames

### Booking Module

- Track photoshoot bookings
- Advance payment tracking
- Status management (Pending/Completed/Cancelled)
- Location and description fields

### Invoice History

- Search invoices
- View detailed invoice information
- Reprint invoices as PDF

## Security

- Password hashing using SHA-256
- Role-based access control
- Session management

## Notes

- All data is stored locally in SQLite
- No internet connection required
- Invoices are saved as PDF in the `invoices` folder
- Database is automatically initialized on first run

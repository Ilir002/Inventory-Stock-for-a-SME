# 📦 Inventory-Stock-for-a-SME

This web application is dedicated to the Stefanelli Feinkostboutique as a real case.
---

## 📑 Analysis

### Problem

Many businesses track inventory manually or with fragmented tools, leading to inaccurate stock levels, lost records, and inefficient workflows. The inventory stock web application provides a centralized system to manage inventory, track changes, and maintain accurate stock data in real time.

---

### Scenario

A user logs into the inventory stock web application and accesses a dashboard displaying current inventory levels.

The user can:

* Add new stock when items are purchased or received
* Remove stock if items are sold, damaged, or incorrectly recorded
* Upload receipts as proof of stock additions
* Organize items into categories

The system automatically tracks all inventory changes and generates reports over different time periods (daily, weekly, monthly, yearly).

If stock levels fall below a defined threshold, the user is notified immediately to prevent shortages.

---

### User Stories

* As a user, I want to add new stock to the inventory, so I can keep the inventory up to date.
* As a user, I want to upload receipts corresponding to stock increases for record-keeping.
* As a user, I want to delete stock from the inventory if stock has expired or no longer needed.
* As a user, I want to receive reports to track inventory changes (daily, weekly, monthly, yearly).
* As a user, I want to manage categories by adding to customize my inventory structure.
* As a user, I want to manage categories by modifying to customize my inventory structure.
* As a user, I want to be notified when stock is below threshold, so I don’t need to monitor it manually.
* As a user, I want to be able to register and log into the web application for authentication.

---

### Use Cases

* Add new inventory items
* Update stock quantities
* Delete inventory items
* Create and manage categories
* Upload and store receipts
* Generate inventory reports
* View dashboard summaries
* Receive low-stock alerts
* Track inventory changes over time

---

## 🔧 Project Requirements

This application satisfies the following key requirements:

### 1. Interactive Web Application

Users can:

* Navigate through a dashboard
* Add, edit, and delete stock
* Manage categories
* Upload files (receipts)
* View reports and alerts

The application uses a user-friendly interface with dynamic interaction.

---

### 2. Data Validation

Examples include:

* Ensuring stock quantities are numeric and non-negative
* Validating category names (no duplicates)
* Verifying file uploads (correct format for receipts)
* Preventing invalid or incomplete form submissions

---

### 3. Data Persistence & Processing

The application stores and processes data using a structured backend system.

Stored data includes:

* Inventory items and quantities
* Categories
* Transaction history (stock changes)
* Uploaded receipts

Generated outputs:

* Inventory reports (daily, weekly, monthly, yearly)
* Low-stock alerts
* Dashboard summaries

---

## 💼 Implementation

### Technology

* Python (backend)
* NiceGUI (frontend)
* Database (e.g., SQLite / PostgreSQL)

---

### Repository Structure

```
Invetory Stock Web App/
├── app.py                 # application entry point
├── routes/                # application routes (views/controllers)
├── models/                # database models
├── templates/             # HTML templates
├── static/                # CSS, JavaScript, assets
├── utils/                 # helper functions (validation, reporting)
├── uploads/               # stored receipt files
└── README.md              # documentation
```

---

## ▶️ How to Run

1. Clone the repository
2. Open the project in your development environment
3. Install dependencies
4. Run the application:

```
python app.py
```

5. Open the browser and navigate to:

```
http://localhost:5000
```

---

## 📚 Libraries Used

* Web framework (Flask/Django)
* Database library (SQLite/PostgreSQL)
* File handling utilities for uploads

---

## 👥 Team & Contributions

All team members contributed collaboratively to the project:

| Team Member | Contribution                                   |
| ----------- | ---------------------------------------------- |
| Blenoard    | Backend logic, validation, reporting           |
| Ilir        | Inventory features, categories                 |
| Korab       | Architecture, testing, documentation           |
| Vittorio    | UI interaction                                 |


---

## 📄 License

This project is provided for educational purposes as part of the Advanced Programming module at FHNW.

MIT License.

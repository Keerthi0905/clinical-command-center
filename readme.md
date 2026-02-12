# Clinical Command Center  
### Real-Time Emergency Patient Workflow Dashboard (Flask)

---

## Overview

Clinical Command Center is a Flask-based web application that simulates a hospital patient workflow system.

It allows users to:

- Register patients  
- Track movement across departments  
- Log clinical actions  
- Archive completed visits  

All within a modern glass-style dashboard interface.

This project serves as a workflow simulation and an educational demonstration of full-stack Flask development with dynamic UI rendering.

---

## Features

### 🧾 Patient Registration

- Register patients with name, age, and priority (Routine or Emergency)
- Automatic unique patient ID generation
- Visit count tracking for repeat patients
- Initial audit trail entry on admission

---

### 🚨 Emergency Monitoring

- Visual alert indicator for emergency patients
- Real-time count of critical active patients
- Active vs discharged patient tracking

---

### 🔄 Department Workflow Management

Patients move across the following departments:

- Reception  
- Triage  
- Consultation  
- Lab  
- Pharmacy  
- Discharge  

Each transition:

- Updates patient location  
- Logs an audit entry  
- Updates the activity feed  

---

### 🧪 Clinical Logging

- Add lab orders to patient records  
- Timestamped audit trail for all actions  
- Structured order tracking  

---

### 📁 Discharge Archive

- Completed patients stored separately  
- Visit history preserved  
- Final discharge summary logged  

---

### 📡 Activity Feed

- Displays latest system actions  
- Broadcast log for key events  
- Reverse chronological order  

---

## 📂 Project Structure

```
clinical-command-center/
│
├── app.py
├── templates/
│   └── index.html
└── README.md
```

## 💡 Why This Project?

This project demonstrates:

- Backend routing and state management in Flask
- Dynamic UI rendering with Jinja2
- Workflow simulation logic
- Clean UI design with glassmorphism styling
- Structured audit logging and state transitions

## 🗺 Roadmap

- Database integration
- Authentication & role-based access
- Real-time updates with WebSockets
- REST API support
- Exportable patient reports



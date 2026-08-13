# 🚑 Ambulance Traffic System

<div align="center">

**A Smart Emergency Response Management Solution**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Database](https://img.shields.io/badge/Database-SQLite-lightblue?style=flat-square&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

</div>

---

## 🎯 Overview

The **Ambulance Traffic System** is an efficient emergency response management application that streamlines ambulance dispatching and emergency request handling. Built with Python and SQLite, it provides real-time tracking of ambulances and emergency cases with an intuitive command-line interface.

---

## ✨ Key Features

- 🚨 **Emergency Management** – Register and track patient emergencies by priority
- 🏥 **Ambulance Fleet Control** – Manage ambulance resources, drivers, and assignments
- 📍 **Real-time Status Updates** – Track ambulance and emergency status dynamically
- 💾 **Persistent Storage** – SQLite database for reliable data management
- 🎮 **User-Friendly Interface** – Simple menu-driven system for easy navigation
- 🔄 **CRUD Operations** – Create, Read, Update, Delete all ambulance and emergency records

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.x |
| **Database** | SQLite3 |
| **Interface** | CLI (Command-Line) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.x installed on your system

### Installation & Usage

1. **Clone or download the project**
   ```bash
   cd Ambulance_Traffic_System
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Choose from the menu options:**
   - `1` – Add a new ambulance
   - `2` – View all ambulances
   - `3` – Exit application
   - `4` – Update ambulance status
   - `5` – Delete ambulance
   - `6` – Register new emergency
   - `7` – View all emergencies

---

## 📊 Database Schema

### Ambulances Table
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER (PK) | Unique ambulance ID |
| driver_name | TEXT | Ambulance driver's name |
| hospital | TEXT | Home hospital assignment |
| current_location | TEXT | Current location |
| status | TEXT | Availability status |

### Emergencies Table
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER (PK) | Unique emergency ID |
| patient_name | TEXT | Patient's name |
| location | TEXT | Emergency location |
| priority | TEXT | Urgency level |
| status | TEXT | Case status |

---

## 💡 Example Workflow

```
1. Register an ambulance with driver and hospital details
2. Log an emergency case with patient info and priority
3. Update ambulance status to "En Route" when dispatched
4. Mark emergency as "Resolved" when handled
5. View all records for monitoring and analytics
```

---

## 🔮 Future Enhancements

- 📱 Mobile app integration
- 🗺️ GPS tracking and route optimization
- 🔔 Real-time notifications
- 📊 Analytics dashboard
- 🌐 Web-based interface
- 👥 Multi-user authentication

---

## 📝 License

This project is open for educational and development purposes.

---

<div align="center">

**Built with ❤️ for emergency response excellence**

</div>

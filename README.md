# 🚑 Ambulance Traffic Management System

A professional emergency response management solution built with Python & SQLite. This system intelligently manages ambulances, emergencies, and traffic information to optimize emergency response times.

## Overview

This project demonstrates real-world software engineering practices including OOP design, error handling, database management, and user interface design. Perfect for portfolio demonstrations or educational purposes.

## Features

### Core Functionality
- **Ambulance Management** - Add, view, update, and delete ambulances with real-time status tracking
- **Emergency Management** - Register emergencies with priority levels and automated status tracking
- **Traffic Information** - Log and track traffic conditions to optimize route planning
- **Smart Dispatching** - Intelligent ambulance assignment based on:
  - Availability status
  - Current location
  - Traffic conditions at ambulance location
  - Emergency priority and location

### Advanced Features
- **Auto-Assignment** - Automatically assign the best available ambulance to an emergency
- **Status Management** - Track ambulances through Available → Busy → Available states
- **Conflict Prevention** - Prevent invalid state transitions and deletions
- **Graceful Error Handling** - Comprehensive error handling with user-friendly messages

## Technical Stack

- **Language**: Python 3.7+
- **Database**: SQLite3 (built-in)
- **Architecture**: Object-Oriented Design
- **Paradigms**: MVC Pattern, CRUD Operations

## Project Structure

```
├── main.py                    # Original version (educational/reference)
├── ambulance_system.py        # Professional refactored version ⭐ USE THIS
├── ambulance.db              # SQLite database
├── requirements.txt          # Project dependencies
└── README.md                 # Documentation
```

## Installation & Usage

### Quick Start (Professional Version)

```bash
# Clone or navigate to project directory
cd Ambulance_Traffic_System

# Install dependencies (optional - only for development/testing)
pip install -r requirements.txt

# Run the professional version
python ambulance_system.py
```

### Using Original Version

```bash
# Run the original version
python main.py
```

## How It Works

### 1. Add Ambulance
- Register a new ambulance with driver name, hospital, and location
- Status automatically set to "Available"

### 2. Register Emergency
- Create emergency record with patient name, location, and priority
- Supports priorities: Low, Medium, High, Critical

### 3. Assign Ambulance
- **Manual Assignment**: Choose ambulance for emergency
- **Auto-Assignment**: System selects best ambulance based on:
  - Ambulance availability
  - Traffic conditions at ambulance location
  - Prioritize ambulances at emergency location
  - Minimum estimated delay

### 4. Track Status
- Update ambulance status: Available → Busy → Available
- Update emergency status: Pending → Assigned → Completed
- Monitor traffic conditions in real-time

## Database Schema

### Ambulances Table
```sql
CREATE TABLE ambulances (
    id INTEGER PRIMARY KEY,
    driver_name TEXT NOT NULL,
    hospital TEXT NOT NULL,
    current_location TEXT NOT NULL,
    status TEXT DEFAULT 'Available',
    created_at TIMESTAMP
)
```

### Emergencies Table
```sql
CREATE TABLE emergencies (
    id INTEGER PRIMARY KEY,
    patient_name TEXT NOT NULL,
    location TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    ambulance_id INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (ambulance_id) REFERENCES ambulances(id)
)
```

### Traffic Table
```sql
CREATE TABLE traffic (
    id INTEGER PRIMARY KEY,
    location TEXT NOT NULL,
    traffic_level TEXT NOT NULL,
    estimated_delay INTEGER NOT NULL,
    recorded_at TIMESTAMP
)
```

## Code Quality & Best Practices

✅ **Object-Oriented Design** - Separate classes for different concerns  
✅ **Error Handling** - Comprehensive try-except blocks and validation  
✅ **Input Validation** - All user inputs validated before database operations  
✅ **SQL Injection Prevention** - Parameterized queries throughout  
✅ **Database Constraints** - Foreign keys and NOT NULL constraints  
✅ **Graceful Degradation** - Handles database errors without crashing  
✅ **Meaningful Error Messages** - User-friendly feedback  
✅ **Code Documentation** - Docstrings for all classes and methods  
✅ **PEP 8 Compliance** - Follows Python style guidelines  

## Menu Options (14 Operations)

| Option | Operation |
|--------|-----------|
| 1 | Add Ambulance |
| 2 | View Ambulances |
| 3 | Update Ambulance Status |
| 4 | Delete Ambulance |
| 5 | Add Emergency |
| 6 | View Emergencies |
| 7 | Assign Ambulance to Emergency |
| 8 | Update Emergency Status |
| 9 | Add Traffic Information |
| 10 | View Traffic Information |
| 11 | Find Available Ambulances |
| 12 | Find Best Ambulance (by traffic) |
| 13 | Auto-Assign Best Ambulance |
| 14 | Exit |

## Example Workflow

```
1. Add 3 ambulances with different locations
2. Register 2 emergencies at different locations
3. Add traffic information for various routes
4. Use auto-assignment to dispatch ambulances based on:
   - Traffic conditions
   - Ambulance availability
   - Emergency location
5. Track status and completion
```

## Testing & Validation

The system includes validation for:
- Empty fields and invalid inputs
- Duplicate ambulance assignments
- Invalid status transitions
- Negative delay values
- Non-existent database records
- Database connection errors

## Portfolio Highlights

This project demonstrates:
- **Database Design** - Proper schema with relationships and constraints
- **OOP Principles** - Classes, encapsulation, separation of concerns
- **Error Handling** - Robust error management and user feedback
- **Algorithm Design** - Intelligent ambulance selection algorithm
- **Best Practices** - Security (SQL injection prevention), code organization
- **Real-World Logic** - Implements actual emergency dispatch scenarios

## Future Enhancements

Possible improvements for production:
- Web interface (Flask/Django)
- Real-time GPS tracking
- SMS/Email notifications
- User authentication
- Reporting dashboard
- Performance optimization with indexing
- API endpoints (REST/GraphQL)
- Unit tests and integration tests
- Docker containerization

## Requirements

- Python 3.7 or higher
- SQLite3 (included with Python)
- No external dependencies required for core functionality

## Installation of Development Tools (Optional)

```bash
pip install -r requirements.txt
```

This installs testing and code quality tools:
- `pytest` - Unit testing framework
- `black` - Code formatter
- `flake8` - Code linter

## Usage Examples

### Example 1: Basic Workflow
```
Enter your choice: 1
Enter driver name: John Doe
Enter hospital name: City Hospital
Enter current location: Downtown
✓ Ambulance added successfully
```

### Example 2: Emergency Registration
```
Enter your choice: 5
Enter patient name: Alice Smith
Enter emergency location: Main Street
Enter priority: High
✓ Emergency registered successfully
```

### Example 3: Auto-Assignment
```
Enter your choice: 13
Enter emergency ID for auto-assignment: 1
✓ Best ambulance (ID: 2, Driver: John Doe) assigned
  Estimated delay: 5 minutes
```

## Error Handling Examples

The system gracefully handles:
- Invalid menu choices
- Database connection failures
- Corrupted data
- Concurrent operations
- Missing records
- Keyboard interrupts (Ctrl+C)

## License

This is an open-source educational project.

## Author Notes

This project was created as a demonstration of professional Python development practices including:
- Clean code principles
- SOLID design patterns
- User-centered design
- Production-ready error handling

Perfect for:
- Portfolio projects
- Educational demonstrations
- System design interviews
- Real-world application learning

---

**Note**: This is the professional version (`ambulance_system.py`). For the original educational version, see `main.py`.

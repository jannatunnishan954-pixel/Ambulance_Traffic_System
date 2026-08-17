"""
Professional Ambulance Traffic Management System
A robust, production-ready emergency response management solution.
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


class DatabaseManager:
    """Handles all database operations with error handling."""
    
    def __init__(self, db_name: str = 'ambulance.db'):
        """Initialize database connection with error handling."""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.connection.cursor()
            print("✓ Database connected successfully")
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ambulances 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_name TEXT NOT NULL,
                hospital TEXT NOT NULL,
                current_location TEXT NOT NULL,
                status TEXT DEFAULT 'Available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS emergencies
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                location TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                ambulance_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ambulance_id) REFERENCES ambulances(id))''')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS traffic
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                traffic_level TEXT NOT NULL,
                estimated_delay INTEGER NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"✗ Table creation error: {e}")
            raise
    
    def execute_query(self, query: str, params: Tuple = None, fetch: bool = False):
        """Execute database query with error handling."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if fetch:
                return self.cursor.fetchall()
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ Query error: {e}")
            return None
    
    def close(self):
        """Close database connection gracefully."""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")


class AmbulanceManager:
    """Manages ambulance operations."""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def add_ambulance(self, driver_name: str, hospital: str, location: str) -> bool:
        """Add a new ambulance to the system."""
        if not all([driver_name.strip(), hospital.strip(), location.strip()]):
            print("✗ All fields are required and cannot be empty")
            return False
        
        query = '''INSERT INTO ambulances (driver_name, hospital, current_location, status) 
                   VALUES (?, ?, ?, 'Available')'''
        result = self.db.execute_query(query, (driver_name, hospital, location))
        
        if result:
            print("✓ Ambulance added successfully")
        return result
    
    def view_ambulances(self):
        """Display all ambulances."""
        query = "SELECT id, driver_name, hospital, current_location, status FROM ambulances"
        ambulances = self.db.execute_query(query, fetch=True)
        
        if not ambulances:
            print("✗ No ambulances found in the system")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Driver':<15} {'Hospital':<20} {'Location':<20} {'Status':<10}")
        print("="*80)
        for amb in ambulances:
            print(f"{amb[0]:<5} {amb[1]:<15} {amb[2]:<20} {amb[3]:<20} {amb[4]:<10}")
        print("="*80 + "\n")
    
    def update_ambulance_status(self, ambulance_id: int, new_status: str) -> bool:
        """Update ambulance status with validation."""
        valid_statuses = ['Available', 'Busy', 'Maintenance']
        
        if new_status not in valid_statuses:
            print(f"✗ Invalid status. Choose from: {', '.join(valid_statuses)}")
            return False
        
        query = "SELECT id FROM ambulances WHERE id = ?"
        if not self.db.execute_query(query, (ambulance_id,), fetch=True):
            print("✗ Ambulance not found")
            return False
        
        query = "UPDATE ambulances SET status = ? WHERE id = ?"
        result = self.db.execute_query(query, (new_status, ambulance_id))
        
        if result:
            print(f"✓ Ambulance status updated to '{new_status}'")
        return result
    
    def delete_ambulance(self, ambulance_id: int) -> bool:
        """Delete ambulance with safety checks."""
        query = "SELECT status FROM ambulances WHERE id = ?"
        ambulance = self.db.execute_query(query, (ambulance_id,), fetch=True)
        
        if not ambulance:
            print("✗ Ambulance not found")
            return False
        
        if ambulance[0][0] == 'Busy':
            print("✗ Cannot delete a busy ambulance")
            return False
        
        query = "SELECT id FROM emergencies WHERE ambulance_id = ? AND status = 'Assigned'"
        assigned = self.db.execute_query(query, (ambulance_id,), fetch=True)
        
        if assigned:
            print("✗ Cannot delete ambulance with assigned emergencies")
            return False
        
        query = "DELETE FROM ambulances WHERE id = ?"
        result = self.db.execute_query(query, (ambulance_id,))
        
        if result:
            print("✓ Ambulance deleted successfully")
        return result
    
    def get_available_ambulances(self) -> List[Tuple]:
        """Get list of available ambulances."""
        query = "SELECT * FROM ambulances WHERE status = 'Available'"
        return self.db.execute_query(query, fetch=True)


class EmergencyManager:
    """Manages emergency operations."""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def add_emergency(self, patient_name: str, location: str, priority: str) -> bool:
        """Register a new emergency."""
        valid_priorities = ['Low', 'Medium', 'High', 'Critical']
        
        if not all([patient_name.strip(), location.strip()]):
            print("✗ Patient name and location are required")
            return False
        
        if priority not in valid_priorities:
            print(f"✗ Invalid priority. Choose from: {', '.join(valid_priorities)}")
            return False
        
        query = '''INSERT INTO emergencies (patient_name, location, priority, status) 
                   VALUES (?, ?, ?, 'Pending')'''
        result = self.db.execute_query(query, (patient_name, location, priority))
        
        if result:
            print("✓ Emergency registered successfully")
        return result
    
    def view_emergencies(self):
        """Display all emergencies."""
        query = "SELECT id, patient_name, location, priority, status, ambulance_id FROM emergencies"
        emergencies = self.db.execute_query(query, fetch=True)
        
        if not emergencies:
            print("✗ No emergencies found")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<5} {'Patient':<15} {'Location':<20} {'Priority':<10} {'Status':<12} {'Ambulance':<10}")
        print("="*100)
        for emg in emergencies:
            amb_id = emg[5] if emg[5] else "N/A"
            print(f"{emg[0]:<5} {emg[1]:<15} {emg[2]:<20} {emg[3]:<10} {emg[4]:<12} {amb_id:<10}")
        print("="*100 + "\n")
    
    def assign_ambulance(self, emergency_id: int, ambulance_id: int) -> bool:
        """Manually assign ambulance to emergency."""
        query = "SELECT status FROM emergencies WHERE id = ?"
        emergency = self.db.execute_query(query, (emergency_id,), fetch=True)
        
        if not emergency:
            print("✗ Emergency not found")
            return False
        
        if emergency[0][0] != 'Pending':
            print("✗ Emergency must be in Pending status to assign ambulance")
            return False
        
        query = "SELECT status FROM ambulances WHERE id = ?"
        ambulance = self.db.execute_query(query, (ambulance_id,), fetch=True)
        
        if not ambulance:
            print("✗ Ambulance not found")
            return False
        
        if ambulance[0][0] != 'Available':
            print("✗ Ambulance is not available")
            return False
        
        query = "UPDATE emergencies SET ambulance_id = ?, status = 'Assigned' WHERE id = ?"
        self.db.execute_query(query, (ambulance_id, emergency_id))
        
        query = "UPDATE ambulances SET status = 'Busy' WHERE id = ?"
        result = self.db.execute_query(query, (ambulance_id,))
        
        if result:
            print(f"✓ Ambulance {ambulance_id} assigned to Emergency {emergency_id}")
        return result
    
    def update_emergency_status(self, emergency_id: int, new_status: str) -> bool:
        """Update emergency status with validation."""
        valid_statuses = ['Pending', 'Assigned', 'In Progress', 'Completed', 'Cancelled']
        
        if new_status not in valid_statuses:
            print(f"✗ Invalid status. Choose from: {', '.join(valid_statuses)}")
            return False
        
        query = "SELECT status, ambulance_id FROM emergencies WHERE id = ?"
        emergency = self.db.execute_query(query, (emergency_id,), fetch=True)
        
        if not emergency:
            print("✗ Emergency not found")
            return False
        
        current_status, ambulance_id = emergency[0]
        
        if new_status == 'Completed' and current_status != 'Assigned':
            print("✗ Only assigned emergencies can be marked as completed")
            return False
        
        query = "UPDATE emergencies SET status = ? WHERE id = ?"
        self.db.execute_query(query, (new_status, emergency_id))
        
        # Release ambulance if emergency is completed
        if new_status == 'Completed' and ambulance_id:
            query = "UPDATE ambulances SET status = 'Available' WHERE id = ?"
            self.db.execute_query(query, (ambulance_id,))
        
        if new_status == 'Completed':
            print(f"✓ Emergency marked as completed, ambulance released")
        else:
            print(f"✓ Emergency status updated to '{new_status}'")
        
        return True


class TrafficManager:
    """Manages traffic information."""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def add_traffic_info(self, location: str, traffic_level: str, estimated_delay: int) -> bool:
        """Add traffic information."""
        valid_levels = ['Low', 'Medium', 'High']
        
        if not location.strip():
            print("✗ Location is required")
            return False
        
        if traffic_level not in valid_levels:
            print(f"✗ Invalid traffic level. Choose from: {', '.join(valid_levels)}")
            return False
        
        if estimated_delay < 0:
            print("✗ Delay cannot be negative")
            return False
        
        query = '''INSERT INTO traffic (location, traffic_level, estimated_delay) 
                   VALUES (?, ?, ?)'''
        result = self.db.execute_query(query, (location, traffic_level, estimated_delay))
        
        if result:
            print("✓ Traffic information recorded")
        return result
    
    def view_traffic(self):
        """Display all traffic information."""
        query = "SELECT id, location, traffic_level, estimated_delay FROM traffic ORDER BY recorded_at DESC"
        traffic_data = self.db.execute_query(query, fetch=True)
        
        if not traffic_data:
            print("✗ No traffic data found")
            return
        
        print("\n" + "="*70)
        print(f"{'ID':<5} {'Location':<25} {'Level':<10} {'Delay (min)':<15}")
        print("="*70)
        for traffic in traffic_data:
            print(f"{traffic[0]:<5} {traffic[1]:<25} {traffic[2]:<10} {traffic[3]:<15}")
        print("="*70 + "\n")
    
    def get_traffic_delay(self, location: str) -> int:
        """Get estimated delay for a location."""
        query = '''SELECT estimated_delay FROM traffic 
                   WHERE LOWER(location) = LOWER(?) 
                   ORDER BY estimated_delay ASC LIMIT 1'''
        result = self.db.execute_query(query, (location,), fetch=True)
        return result[0][0] if result else 0


class AmbulanceTrafficSystem:
    """Main system controller."""
    
    def __init__(self):
        """Initialize the system."""
        self.db = DatabaseManager()
        self.ambulance_mgr = AmbulanceManager(self.db)
        self.emergency_mgr = EmergencyManager(self.db)
        self.traffic_mgr = TrafficManager(self.db)
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "="*50)
        print("🚑 AMBULANCE TRAFFIC MANAGEMENT SYSTEM")
        print("="*50)
        print("1.  Add Ambulance")
        print("2.  View Ambulances")
        print("3.  Update Ambulance Status")
        print("4.  Delete Ambulance")
        print("5.  Add Emergency")
        print("6.  View Emergencies")
        print("7.  Assign Ambulance to Emergency")
        print("8.  Update Emergency Status")
        print("9.  Add Traffic Information")
        print("10. View Traffic Information")
        print("11. Find Available Ambulances")
        print("12. Find Best Ambulance (by traffic)")
        print("13. Auto-Assign Best Ambulance")
        print("14. Exit")
        print("="*50)
    
    def find_best_ambulance(self) -> Optional[Tuple]:
        """Find best available ambulance based on traffic."""
        available = self.ambulance_mgr.get_available_ambulances()
        
        if not available:
            print("✗ No available ambulances found")
            return None
        
        best_ambulance = None
        lowest_delay = float('inf')
        
        for ambulance in available:
            location = ambulance[3]
            delay = self.traffic_mgr.get_traffic_delay(location)
            
            if delay < lowest_delay:
                lowest_delay = delay
                best_ambulance = ambulance
        
        return best_ambulance
    
    def auto_assign_ambulance(self, emergency_id: int) -> bool:
        """Automatically assign best ambulance to emergency."""
        query = "SELECT location, status FROM emergencies WHERE id = ?"
        emergency = self.db.execute_query(query, (emergency_id,), fetch=True)
        
        if not emergency:
            print("✗ Emergency not found")
            return False
        
        if emergency[0][1] != 'Pending':
            print("✗ Emergency must be in Pending status")
            return False
        
        emergency_location = emergency[0][0]
        available = self.ambulance_mgr.get_available_ambulances()
        
        if not available:
            print("✗ No available ambulances found")
            return False
        
        best_ambulance = None
        lowest_delay = float('inf')
        
        # Prioritize ambulances at emergency location
        for ambulance in available:
            if ambulance[3].lower() == emergency_location.lower():
                best_ambulance = ambulance
                lowest_delay = 0
                break
            
            delay = self.traffic_mgr.get_traffic_delay(ambulance[3])
            if delay < lowest_delay:
                lowest_delay = delay
                best_ambulance = ambulance
        
        if not best_ambulance:
            print("✗ No suitable ambulance found")
            return False
        
        result = self.emergency_mgr.assign_ambulance(emergency_id, best_ambulance[0])
        
        if result:
            print(f"✓ Best ambulance (ID: {best_ambulance[0]}, Driver: {best_ambulance[1]}) assigned")
            print(f"  Estimated delay: {lowest_delay} minutes")
        
        return result
    
    def run(self):
        """Main application loop."""
        print("\n✓ Ambulance Traffic Management System Started")
        
        while True:
            try:
                self.display_menu()
                choice = input("Enter your choice (1-14): ").strip()
                
                if choice == '1':
                    driver = input("Enter driver name: ").strip()
                    hospital = input("Enter hospital name: ").strip()
                    location = input("Enter current location: ").strip()
                    self.ambulance_mgr.add_ambulance(driver, hospital, location)
                
                elif choice == '2':
                    self.ambulance_mgr.view_ambulances()
                
                elif choice == '3':
                    try:
                        amb_id = int(input("Enter ambulance ID: "))
                        status = input("Enter status (Available/Busy/Maintenance): ").strip()
                        self.ambulance_mgr.update_ambulance_status(amb_id, status)
                    except ValueError:
                        print("✗ Please enter a valid ambulance ID")
                
                elif choice == '4':
                    try:
                        amb_id = int(input("Enter ambulance ID to delete: "))
                        self.ambulance_mgr.delete_ambulance(amb_id)
                    except ValueError:
                        print("✗ Please enter a valid ambulance ID")
                
                elif choice == '5':
                    patient = input("Enter patient name: ").strip()
                    location = input("Enter emergency location: ").strip()
                    priority = input("Enter priority (Low/Medium/High/Critical): ").strip()
                    self.emergency_mgr.add_emergency(patient, location, priority)
                
                elif choice == '6':
                    self.emergency_mgr.view_emergencies()
                
                elif choice == '7':
                    try:
                        emg_id = int(input("Enter emergency ID: "))
                        amb_id = int(input("Enter ambulance ID: "))
                        self.emergency_mgr.assign_ambulance(emg_id, amb_id)
                    except ValueError:
                        print("✗ Please enter valid IDs")
                
                elif choice == '8':
                    try:
                        emg_id = int(input("Enter emergency ID: "))
                        status = input("Enter status (Pending/Assigned/In Progress/Completed/Cancelled): ").strip()
                        self.emergency_mgr.update_emergency_status(emg_id, status)
                    except ValueError:
                        print("✗ Please enter a valid emergency ID")
                
                elif choice == '9':
                    location = input("Enter traffic location: ").strip()
                    level = input("Enter traffic level (Low/Medium/High): ").strip()
                    try:
                        delay = int(input("Enter estimated delay (minutes): "))
                        self.traffic_mgr.add_traffic_info(location, level, delay)
                    except ValueError:
                        print("✗ Please enter a valid delay value")
                
                elif choice == '10':
                    self.traffic_mgr.view_traffic()
                
                elif choice == '11':
                    available = self.ambulance_mgr.get_available_ambulances()
                    if available:
                        print("\n✓ Available Ambulances:")
                        for amb in available:
                            print(f"  ID: {amb[0]} | Driver: {amb[1]} | Location: {amb[3]}")
                    else:
                        print("✗ No available ambulances")
                
                elif choice == '12':
                    best = self.find_best_ambulance()
                    if best:
                        delay = self.traffic_mgr.get_traffic_delay(best[3])
                        print(f"\n✓ Best Ambulance: ID {best[0]} | Driver: {best[1]} | Location: {best[3]}")
                        print(f"  Estimated delay: {delay} minutes")
                
                elif choice == '13':
                    try:
                        emg_id = int(input("Enter emergency ID for auto-assignment: "))
                        self.auto_assign_ambulance(emg_id)
                    except ValueError:
                        print("✗ Please enter a valid emergency ID")
                
                elif choice == '14':
                    print("\n✓ Thank you for using Ambulance Traffic System. Goodbye!")
                    self.db.close()
                    break
                
                else:
                    print("✗ Invalid choice. Please enter a number between 1 and 14")
            
            except KeyboardInterrupt:
                print("\n\n✓ System shutdown initiated by user")
                self.db.close()
                break
            except Exception as e:
                print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    system = AmbulanceTrafficSystem()
    system.run()

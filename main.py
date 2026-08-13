import sqlite3
connection = sqlite3.connect('ambulance.db')
cursor=connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS ambulances 
    (id INTEGER PRIMARY KEY, 
    driver_name TEXT, 
    hospital TEXT, 
    current_location TEXT, 
    status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS emergencies
    (id INTEGER PRIMARY KEY, 
    patient_name TEXT, 
    location TEXT, 
    priority TEXT,
    status TEXT)''')
print('1. Add ambulance\n2. View ambulances\n3. Exit\n4. Update ambulance status\n5. Delete ambulance\n6. Add emergency\n7. View emergencies')
while True:
    choice=input("Enter your choice: ")
    if choice=='1':
        driver_name=input("Enter driver name: ")
        hospital=input("Enter hospital name: ")
        current_location=input("Enter current location: ")
        status='Available'
        new_ambulance=(driver_name, hospital, current_location, status)
        
        cursor.execute('''INSERT INTO ambulances (driver_name, hospital, current_location, status) VALUES (?, ?, ?, ?)''', new_ambulance)
        connection.commit()
    elif choice=='2':
        cursor.execute("SELECT * FROM ambulances")
        ambulances=cursor.fetchall()
        for item in ambulances:
            print(f"ID: {item[0]} | Driver Name: {item[1]} | Hospital: {item[2]} | Current Location: {item[3]} | Status: {item[4]}")
    elif choice=='4':
        ambulance_id=int(input("Enter ambulance ID to update: "))
        new_status=input("Enter new status: ")
        cursor.execute("UPDATE ambulances SET status=? WHERE id=?", (new_status, ambulance_id))
        connection.commit()
        print('Ambulance status updated successfully.')
    elif choice=='5':
        ambulance_id=int(input("Enter ambulance ID to delete: "))
        cursor.execute("DELETE FROM ambulances WHERE id=?", (ambulance_id,))
        connection.commit()
        print('Ambulance deleted successfully.')
    elif choice=='6':
         patient_name=input("Enter patient name: ")
         location=input("Enter emergency location: ")
         priority=input("Enter priority: ")
         status='Pending'
         new_emergency=(patient_name, location, priority, status)
         cursor.execute('''INSERT INTO emergencies (patient_name, location, priority, status) VALUES (?, ?, ?, ?)''', new_emergency)
         connection.commit()
         print('Emergency added successfully.')
    elif choice=='7':
        cursor.execute("SELECT * FROM emergencies")
        emergencies=cursor.fetchall()
        for item in emergencies:
            print(f"ID: {item[0]} | Patient Name: {item[1]} | Location: {item[2]} | Priority: {item[3]} | Status: {item[4]}")
    elif choice=='3':
            print("Exiting..")
            break
connection.close()